# -*- coding:UTF-8 -*-
import os
import sys
import subprocess

# 自动检测并安装缺失的第三方库
required_packages = {
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'lxml': 'lxml'
}

def install_package(package_name):
    print(f"正在安装缺失的库: {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"{package_name} 安装成功！")
    except subprocess.CalledProcessError:
        print(f"错误: 无法安装 {package_name}，请手动安装。")
        sys.exit(1)

for import_name, install_name in required_packages.items():
    try:
        __import__(import_name)
    except ImportError:
        install_package(install_name)

import requests
from bs4 import BeautifulSoup
import time
import re
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from bqg_api import (
    CHAPTER_URL_PREFIX,
    apibi_chapter_token,
    fetch_chapter_text_api,
    fetch_chapter_titles_api,
    parse_apibi_chapter_token,
    parse_book_id_from_url,
    try_fetch_book_api,
)
from text_clean import clean_chapter_text

# v1.3 Phase 12 / CFG-01：并发可配置；CLI 与 BQUGE_MAX_WORKERS 见 README「并发」
DEFAULT_MAX_WORKERS = 10
MAX_WORKERS_CAP = 64
MAX_WORKERS_ENV = "BQUGE_MAX_WORKERS"


def _parse_env_max_workers() -> int | None:
    """从环境变量读取并发数；缺省/非法则返回 None（由 resolve 用默认值 10）。"""
    s = (os.environ.get(MAX_WORKERS_ENV) or "").strip()
    if not s:
        return None
    try:
        n = int(s, 10)
    except ValueError:
        print(
            f"警告: {MAX_WORKERS_ENV}={s!r} 非有效整数，将使用默认 {DEFAULT_MAX_WORKERS} 线程。",
            file=sys.stderr,
        )
        return None
    if n < 1:
        print(
            f"警告: {MAX_WORKERS_ENV}={n} 小于 1，将使用默认 {DEFAULT_MAX_WORKERS} 线程。",
            file=sys.stderr,
        )
        return None
    if n > MAX_WORKERS_CAP:
        print(
            f"提示: {MAX_WORKERS_ENV}={n} 已超过上限，将使用 {MAX_WORKERS_CAP} 线程。",
            file=sys.stderr,
        )
        return MAX_WORKERS_CAP
    return n


def _clamp_cli_workers(n: int) -> int:
    if n < 1:
        raise ValueError(
            f"并发线程数须为 1~{MAX_WORKERS_CAP} 的整数，当前: {n}"
        )
    if n > MAX_WORKERS_CAP:
        print(
            f"提示: 并发数已限制为上限 {MAX_WORKERS_CAP}（原值 {n}），以免请求过高。",
            file=sys.stderr,
        )
        return MAX_WORKERS_CAP
    return n


def resolve_max_workers(cli_override: int | None) -> int:
    """确定线程池大小：显式 CLI 优先，其次环境变量，最后 DEFAULT_MAX_WORKERS。"""
    if cli_override is not None:
        return _clamp_cli_workers(cli_override)
    env_n = _parse_env_max_workers()
    if env_n is not None:
        return env_n
    return DEFAULT_MAX_WORKERS


"""
类说明: 下载《笔趣看》网小说
目标 URL: https://m.bqg92.com/ (或其他同类笔趣阁站点)
优化内容: 
1. 替换 urllib 为 requests
2. 增加多线程并发下载
3. 修复写入时遇到 'h' 截断内容的严重 BUG
4. 优化 HTML 解析逻辑
"""

def _env_raw_text() -> bool:
    v = (os.environ.get("BQUGE_RAW_TEXT") or "").strip().lower()
    return v in ("1", "true", "yes", "on")


class NovelDownloader:
    def __init__(self, target_url: str, raw_text: object = None, max_workers: int | None = None):
        self.target_url = target_url
        self._opt_max_workers = max_workers
        # 使用 Session 保持连接，提高性能
        self.session = requests.Session()
        # 新站：apibi.cc API（与 m.bqg92.com / *bqg655.cc 书号一致时可走此路径）
        self._use_api = False
        self._api_book_id = None
        if raw_text is None:
            self._raw_text = _env_raw_text()
        else:
            self._raw_text = bool(raw_text)
        
        # 随机 User-Agent 列表
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        ]
        
        self.session.headers.update({
            # 模拟最新的浏览器，并添加常用请求头以显得更真实
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            # 移除手动设置的 Accept-Encoding，让 requests 自动处理压缩，避免解压失败导致乱码
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        self.novel_name = "下载的小说"

        book_id = parse_book_id_from_url(target_url)
        if book_id:
            meta = try_fetch_book_api(self.session, book_id)
            if meta and meta.get("title"):
                self._use_api = True
                self._api_book_id = book_id
                self.novel_name = str(meta["title"]).strip() or self.novel_name
                print(f"已连接 apibi 书库: 《{self.novel_name}》(id={book_id})，将使用 API 下载正文。")

    def get_download_url(self):
        """
        获取小说章节目录和链接
        """
        if self._use_api and self._api_book_id:
            titles = fetch_chapter_titles_api(self.session, self._api_book_id)
            if titles:
                chapters = []
                for i, title in enumerate(titles, start=1):
                    chapters.append((title, apibi_chapter_token(self._api_book_id, i)))
                print(f"API 目录共 {len(chapters)} 章")
                return chapters
            print("API 未返回章节目录，回退到网页解析…")
            self._use_api = False

        return self._get_chapters_from_page()

    def _get_chapters_from_page(self):
        """从目录页 HTML 解析章节链接（传统笔趣阁结构及 /kan/ 等）。"""
        try:
            response = self.session.get(self.target_url, timeout=15)
            print(f"HTTP状态码: {response.status_code}")

            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, "html.parser")

            info_div = soup.find("div", class_="info")
            if info_div and info_div.find("h2"):
                self.novel_name = info_div.find("h2").get_text().strip()
            else:
                title_tag = soup.find("title")
                if title_tag:
                    title = title_tag.get_text()
                    self.novel_name = title.split("_")[0] if "_" in title else title
                else:
                    self.novel_name = "未知小说"
                    print("警告: 无法找到网页标题，可能被反爬拦截。")
                    print(f"响应内容预览: {response.text[:500]}")
                    return []

            print(f"正在分析小说: 《{self.novel_name}》")

            if soup.title:
                print(f"页面标题: {soup.title.get_text().strip()}")

            book_id = parse_book_id_from_url(self.target_url)
            if not book_id:
                print("错误: 无法从URL中解析小说ID")
                return []

            def matches_chapter_href(href: str) -> bool:
                if not href.endswith(".html"):
                    return False
                if f"/book/{book_id}/" in href:
                    return bool(re.search(r"/\d+\.html$", href))
                if f"/kan/{book_id}/" in href:
                    return bool(re.search(r"/\d+\.html$", href))
                return False

            all_links = soup.find_all("a", href=True)

            seen_urls = set()
            temp_chapters = []

            for link in all_links:
                href = link.get("href")
                title = link.get_text().strip()

                if not href or not title:
                    continue

                if not href.startswith("http"):
                    if not href.startswith("/"):
                        href = "/" + href
                    domain = "https://m.bqg92.com"
                    if self.target_url.startswith("http"):
                        parsed_uri = requests.utils.urlparse(self.target_url)
                        domain = "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)
                    href = domain + href

                if matches_chapter_href(href):
                    if href not in seen_urls:
                        seen_urls.add(href)
                        temp_chapters.append((title, href))

            def get_sort_key(item):
                url = item[1]
                match = re.search(r"/(\d+)\.html", url)
                return int(match.group(1)) if match else 0

            temp_chapters.sort(key=get_sort_key)
            chapters = temp_chapters

            if not chapters:
                print("未找到符合规则的章节链接，可能目录结构已变或需使用书号走 API。")

            return chapters

        except Exception as e:
            print(f"获取目录失败: {e}")
            return []

    def _finalize_chapter_text(self, text: str) -> str:
        return clean_chapter_text(text, self._raw_text)

    def get_chapter_content(self, url: str, retries=3):
        """
        下载单个章节内容 (支持分页)
        """
        if url.startswith(CHAPTER_URL_PREFIX):
            time.sleep(random.uniform(0.05, 0.2))
            parsed = parse_apibi_chapter_token(url)
            if not parsed:
                return "无法解析此章节地址"
            bid, ch_idx = parsed
            for attempt in range(retries):
                text = fetch_chapter_text_api(self.session, bid, ch_idx)
                if text is not None:
                    return self._finalize_chapter_text(text)
                time.sleep(0.5 * (attempt + 1))
            return "无法解析此章节内容"

        # 模拟真实用户行为：随机等待一小段时间，避免请求过于密集
        time.sleep(random.uniform(0.1, 0.3))

        full_content = ""
        current_url = url
        page_count = 0
        
        while current_url and page_count < 50: # 限制最大页数防止死循环
            page_count += 1
            page_text = ""
            success = False
            
            for i in range(retries):
                try:
                    # 添加 Referer 伪装成从目录页访问
                    req_headers = {'Referer': self.target_url}
                    response = self.session.get(current_url, headers=req_headers, timeout=10)
                    response.encoding = response.apparent_encoding
                    soup = BeautifulSoup(response.text, "lxml")

                    content_div = (
                        soup.find(id="content")
                        or soup.find(id="rtext")
                        or soup.find("div", id="txt")
                        or soup.find("div", class_="readcontent")
                        or soup.find("article", class_="readtext")
                        or soup.find(class_="showtxt")
                    )
                    
                    if content_div:
                        # 处理换行符，将 <br> 替换为换行
                        text = content_div.get_text('\n', strip=True)
                        # 去除常见的广告文本
                        text = text.replace('\xa0', ' ').replace('app2();', '').replace('read3();', '')
                        page_text = text
                        success = True
                        break
                    
                    if i == retries - 1:
                         # 最后一次重试也失败，或者没找到 content
                         pass

                except requests.RequestException:
                    if i == retries - 1:
                        pass # 失败
                    time.sleep(1) # 重试前等待
            
            if not success:
                if not full_content:
                    return "无法解析此章节内容"
                break # 如果部分页面失败，返回已获取的内容
                
            full_content += page_text + "\n"
            
            # 检查是否有下一页
            # 寻找包含“下一页”文本的链接
            next_link = soup.find('a', string=re.compile('下一页'))
            if next_link:
                next_href = next_link.get('href')
                # 简单的判断：如果 href 是 _\d+.html 这种形式，通常是分页
                # 或者是下一章? 通常下一章是 “下一章”
                # 这里我们假设 “下一页” 就是本章分页
                if next_href and '_' in next_href and '.html' in next_href:
                    # 处理路径
                    if not next_href.startswith('http'):
                        # 解析当前URL的base
                        # current: https://.../book/36560/123.html
                        # next: 123_2.html -> https://.../book/36560/123_2.html
                        # next: /book/36560/123_2.html -> full
                        
                        if next_href.startswith('/'):
                             # 绝对路径
                             parsed = requests.utils.urlparse(current_url)
                             domain = f"{parsed.scheme}://{parsed.netloc}"
                             current_url = domain + next_href
                        else:
                             # 相对路径
                             base_url = current_url.rsplit('/', 1)[0]
                             current_url = f"{base_url}/{next_href}"
                    else:
                        current_url = next_href
                else:
                    current_url = None # 没有下一页或者不符合规则
            else:
                current_url = None

        if not full_content:
            return "下载失败"
        return self._finalize_chapter_text(full_content)

    def _empty_catalog_diagnostics(self) -> str:
        """无章节时打印的可操作说明（MAIN-02 / Phase 9）。"""
        lines = [
            "未找到可下载的章节目录，程序退出。",
            "",
            f"· 目标地址: {self.target_url}",
        ]
        bid = parse_book_id_from_url(self.target_url)
        if not bid and self._use_api and self._api_book_id:
            bid = self._api_book_id
        if bid:
            lines.append(f"· 解析书号: {bid}")
        if self._use_api and self._api_book_id:
            lines.append("· 已使用 apibi 书库；若 API 无目录已自动尝试回退到 HTML 目录页。")
        else:
            lines.append("· 使用 HTML 目录页解析章链（未走 apibi 或 apibi 未返回书信息）。")
        api_base = (os.environ.get("BQUGE_API_BASE") or "").strip()
        if api_base:
            lines.append(f"· BQUGE_API_BASE: {api_base}")
        lines.extend(
            [
                "",
                "可能原因: 书号/URL 错误；站点或 apibi 目录结构变更；网络不稳定、被限流/封锁。",
                "建议: 在浏览器打开 `https://m.bqg92.com/book/<书号>/` 确认有章节；检查环境变量 BQUGE_API_BASE；换网络/代理后重试。",
            ]
        )
        return "\n".join(lines)

    def run(self):
        print("\n\t\t欢迎使用小说下载小工具 (优化版)\n")
        print("*************************************************************************")
        
        chapters = self.get_download_url()
        if not chapters:
            print(self._empty_catalog_diagnostics())
            # 退出代码 1，通知 GitHub Actions 任务失败
            sys.exit(1)

        total_chapters = len(chapters)
        print(f"共发现 {total_chapters} 章，准备开始下载...")
        
        # 获取脚本所在目录，确保文件保存在脚本同级目录下
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 清洗文件名，去除非法字符 (如 /, \, :, *, ?, ", <, >, |) 以避免文件路径错误
        safe_novel_name = re.sub(r'[\\/*?:"<>|]', '_', self.novel_name)
        file_path = os.path.join(script_dir, f"{safe_novel_name}.txt")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"已删除旧文件: {file_path}")

        # 准备用于保存结果的列表，因为多线程是乱序的，我们需要按顺序写入
        # 这里为了简单，我们可以先下载所有内容存入内存（如果小说非常大，建议分批写入）
        # 或者更稳妥的方式：单线程写入，多线程下载。
        
        # 使用字典存储下载结果 index -> content
        results = {}
        
        start_time = time.time()
        
        # 建议线程数不要过高，以免被网站封 IP
        max_workers = resolve_max_workers(self._opt_max_workers)
        print(f"正在使用 {max_workers} 个线程并发下载，请稍候...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_index = {
                executor.submit(self.get_chapter_content, url): index 
                for index, (title, url) in enumerate(chapters)
            }
            
            finished_count = 0
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                content = future.result()
                results[index] = content
                
                finished_count += 1
                # 简易进度条
                percent = (finished_count / total_chapters) * 100
                sys.stdout.write(f"\r已下载: {percent:.2f}% ({finished_count}/{total_chapters})")
                sys.stdout.flush()

        print("\n正在将内容按顺序写入文件...")
        
        # 按顺序写入（首章前不输出多余空行，见 Phase 5 / UAT P2）
        with open(file_path, "a", encoding="utf-8") as f:
            for i in range(total_chapters):
                title = chapters[i][0]
                content = results.get(i, "下载失败")
                if not isinstance(content, str):
                    content = str(content)
                content = content.rstrip() + "\n" if content.strip() else content
                if i == 0:
                    f.write(f"{title}\n")
                else:
                    f.write(f"\n\n{title}\n")
                f.write("-" * 20 + "\n")
                f.write(content)
                if not content.endswith("\n"):
                    f.write("\n")
                if i < total_chapters - 1:
                    f.write("\n")

        end_time = time.time()
        print(f"\n《{self.novel_name}》下载完成！")
        print(f"保存路径: {os.path.abspath(file_path)}")
        print(f"耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    import argparse

    from url_input import normalize_target_url

    def _parse_workers_cli(s: str) -> int:
        try:
            n = int(s, 10)
        except ValueError as e:
            raise argparse.ArgumentTypeError("并发数须为整数") from e
        if n < 1:
            raise argparse.ArgumentTypeError(
                f"并发数须为 1~{MAX_WORKERS_CAP} 的整数，当前: {n}"
            )
        if n > MAX_WORKERS_CAP:
            print(
                f"提示: 并发数已限制为 {MAX_WORKERS_CAP}（原值 {n}）",
                file=sys.stderr,
            )
            return MAX_WORKERS_CAP
        return n

    parser = argparse.ArgumentParser(
        description="笔趣阁类站点小说多线程下载；并发默认与历史行为一致为 10 线程。",
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="书号或目录页 URL（可省略，改为交互输入）",
    )
    parser.add_argument(
        "--raw-text",
        action="store_true",
        help="不应用营销水印行清洗，仅换行/去 BOM；亦可设 BQUGE_RAW_TEXT=1",
    )
    parser.add_argument(
        "-j",
        "--workers",
        type=_parse_workers_cli,
        default=None,
        dest="max_workers",
        metavar="N",
        help=f"并发下载线程数；默认 {DEFAULT_MAX_WORKERS}。也可用环境变量 {MAX_WORKERS_ENV}。",
    )
    args = parser.parse_args()

    input_str = args.url
    if not input_str:
        input_str = input(
            "请输入小说目录下载地址或ID (例如: https://m.bqg92.com/book/3953/ 或 3953):\n"
        )

    if not input_str or not str(input_str).strip():
        print("地址/ID不能为空")
        sys.exit(1)

    target_url = str(input_str).strip()
    was_digit = target_url.isdigit()
    target_url = normalize_target_url(target_url)
    if was_digit:
        print(f"检测到输入为ID，已自动补全为: {target_url}")

    try:
        dl = NovelDownloader(
            target_url, raw_text=args.raw_text, max_workers=args.max_workers
        )
        dl.run()
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
