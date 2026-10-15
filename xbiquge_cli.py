"""Two-step GitHub Actions entrypoint for xbiquge.info."""
import argparse
import json
import re
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import local
import requests
from xbiquge import search, catalog, chapter

_tls = local()
def session():
    if not hasattr(_tls, "session"):
        _tls.session = requests.Session()
        _tls.session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; BiQuGe-Downloader/2.0)", "Accept-Language": "zh-CN,zh;q=0.9"})
    return _tls.session

def fetch(url):
    for attempt in range(3):
        try:
            return chapter(session(), url)
        except (requests.RequestException, ValueError):
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["search", "download"])
    p.add_argument("--keyword", default="")
    p.add_argument("--url", default="")
    p.add_argument("--workers", type=int, default=5)
    p.add_argument("--output", default="output")
    args = p.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    if args.mode == "search":
        books = search(session(), args.keyword)
        (out / "candidates.json").write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")
        for i, book in enumerate(books, 1):
            print(f"{i}. {book['title']} | {book['author']} | {book['status']} | {book['url']}")
        if not books:
            raise SystemExit("没有找到候选书籍")
        return
    if not 1 <= args.workers <= 10:
        p.error("--workers 必须在 1~10 之间")
    name, chapters = catalog(session(), args.url)
    print(f"《{name}》找到 {len(chapters)} 章")
    results = [None] * len(chapters)
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch, url): i for i, (_, url) in enumerate(chapters)}
        for future in as_completed(futures):
            i = futures[future]
            try:
                results[i] = future.result()
            except Exception as exc:
                failures.append({"index": i + 1, "title": chapters[i][0], "error": str(exc)})
    safe = re.sub(r'[\\/*?:"<>|\x00-\x1f]', "_", name).strip()[:100] or "novel"
    txt = out / (safe + ".txt")
    with txt.open("w", encoding="utf-8") as f:
        for i, (title, _) in enumerate(chapters):
            if results[i] is not None:
                f.write(f"{title}\n\n{results[i]}\n\n")
    report = {"title": name, "source": args.url, "total": len(chapters), "downloaded": len(chapters) - len(failures), "failures": failures}
    report_file = out / "report.json"
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    archive = out / (safe + ".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(txt, txt.name)
        z.write(report_file, report_file.name)
    print(f'ZIP: {archive}；成功 {report["downloaded"]}/{report["total"]}')
    if failures:
        raise SystemExit(f"{len(failures)} 章下载失败；已生成部分内容和报告")

if __name__ == "__main__":
    main()
