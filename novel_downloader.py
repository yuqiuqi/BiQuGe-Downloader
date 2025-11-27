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

"""
类说明: 下载《笔趣看》网小说
目标 URL: https://k.biqu68.com/ (或其他同类笔趣阁站点)
优化内容: 
1. 替换 urllib 为 requests
2. 增加多线程并发下载
3. 修复写入时遇到 'h' 截断内容的严重 BUG
4. 优化 HTML 解析逻辑
"""

class NovelDownloader:
    def __init__(self, target_url: str):
        self.target_url = target_url
        # 使用 Session 保持连接，提高性能
        self.session = requests.Session()
        
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
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        self.novel_name = "下载的小说"
        
    def get_download_url(self):
        """
        获取小说章节目录和链接
        """
        try:
            response = self.session.get(self.target_url, timeout=10)
            # 自动识别编码
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 获取小说标题
            info_div = soup.find('div', class_='info')
            if info_div and info_div.find('h2'):
                 self.novel_name = info_div.find('h2').get_text().strip()
            else:
                # 备选方案，从 title 获取
                title = soup.find('title').get_text()
                self.novel_name = title.split('_')[0] if '_' in title else title

            print(f"正在分析小说: 《{self.novel_name}》")

            chapters = []
            
            # 提取所有链接并根据URL特征过滤
            # 假设章节链接包含 book_id (从target_url提取)
            import re
            
            # 从 target_url 提取 book_id (例如 36560)
            # https://k.biqu68.com/book/36560/
            book_id_match = re.search(r'/book/(\d+)', self.target_url)
            if not book_id_match:
                print("错误: 无法从URL中解析小说ID")
                return []
            
            book_id = book_id_match.group(1)
            pattern = re.compile(f'/book/{book_id}/\d+(\_\d+)?\.html')
            
            # 查找所有链接
            all_links = soup.find_all('a', href=True)
            
            seen_urls = set()
            temp_chapters = []

            for link in all_links:
                href = link.get('href')
                title = link.get_text().strip()
                
                if not href or not title:
                    continue

                # 补全 URL
                if not href.startswith('http'):
                     if not href.startswith('/'):
                         href = '/' + href
                     domain = "https://k.biqu68.com"
                     if self.target_url.startswith('http'):
                         # 提取域名
                         parsed_uri = requests.utils.urlparse(self.target_url)
                         domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                     href = domain + href

                # 检查是否是章节链接 (简单的判断: 包含 book_id 且以 .html 结尾)
                # 这里排除分页链接 (通常分页链接带有 _2.html, 但目录页通常只列出第一页)
                # 如果目录页直接列出分页链接，我们需要处理
                if f"/book/{book_id}/" in href and href.endswith('.html'):
                    # 排除掉类似 index.html 或者其他非章节页面
                    # 章节通常是纯数字ID
                    if re.search(r'/\d+\.html$', href): 
                        if href not in seen_urls:
                            seen_urls.add(href)
                            temp_chapters.append((title, href))

            # 排序，为了防止“最新章节”打乱顺序，我们可以尝试按ID排序
            # 提取ID进行排序
            def get_id(item):
                url = item[1]
                match = re.search(r'/(\d+)\.html', url)
                return int(match.group(1)) if match else 0
            
            temp_chapters.sort(key=get_id)
            chapters = temp_chapters

            # 如果没找到，尝试旧逻辑
            if not chapters:
                print("未找到符合规则的章节，尝试通用逻辑...")
                # ... (保留一部分旧逻辑作为fallback?) ... 
                # 这里简单处理，如果没找到直接返回空
                pass

            return chapters

        except Exception as e:
            print(f"获取目录失败: {e}")
            return []

    def get_chapter_content(self, url: str, retries=3):
        """
        下载单个章节内容 (支持分页)
        """
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
                    soup = BeautifulSoup(response.text, 'lxml')
                    
                    # 常见的正文 ID 是 content 或 showtxt
                    content_div = soup.find(id='content') or soup.find(class_='showtxt')
                    
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

        return full_content if full_content else "下载失败"

    def save_to_file(self, file_path: str, chapter_title: str, content: str):
        """
        写入文件
        """
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f"\n\n{chapter_title}\n")
                f.write("-" * 30 + "\n")
                f.write(content)
                f.write("\n")
        except Exception as e:
            print(f"写入失败: {e}")

    def run(self):
        print("\n\t\t欢迎使用小说下载小工具 (优化版)\n")
        print("*************************************************************************")
        
        chapters = self.get_download_url()
        if not chapters:
            print("未找到章节，程序结束。")
            return

        total_chapters = len(chapters)
        print(f"共发现 {total_chapters} 章，准备开始下载...")
        
        # 获取脚本所在目录，确保文件保存在脚本同级目录下
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, f"{self.novel_name}.txt")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"已删除旧文件: {file_path}")

        # 准备用于保存结果的列表，因为多线程是乱序的，我们需要按顺序写入
        # 这里为了简单，我们可以先下载所有内容存入内存（如果小说非常大，建议分批写入）
        # 或者更稳妥的方式：单线程写入，多线程下载。
        
        # 使用字典存储下载结果 index -> content
        results = {}
        
        start_time = time.time()
        
        # 开启线程池下载
        # 建议线程数不要过高，以免被网站封 IP
        max_workers = 10 
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
        
        # 按顺序写入
        with open(file_path, 'a', encoding='utf-8') as f:
            for i in range(total_chapters):
                title = chapters[i][0]
                content = results.get(i, "下载失败")
                f.write(f"\n\n{title}\n")
                f.write("-" * 20 + "\n")
                f.write(content)
                f.write("\n\n")

        end_time = time.time()
        print(f"\n《{self.novel_name}》下载完成！")
        print(f"保存路径: {os.path.abspath(file_path)}")
        print(f"耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    # 优先从命令行参数获取 URL (适配 GitHub Actions)
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
    else:
        input_str = input("请输入小说目录下载地址或ID (例如: https://k.biqu68.com/book/3953/ 或 3953):\n")

    if not input_str:
        print("地址/ID不能为空")
    else:
        target_url = input_str.strip()
        
        # 如果是纯数字，补全为笔趣阁URL
        if target_url.isdigit():
             target_url = f"https://k.biqu68.com/book/{target_url}/"
             print(f"检测到输入为ID，已自动补全为: {target_url}")
        # 简单的补全 http
        elif not target_url.startswith('http'):
            target_url = 'https://' + target_url
            
        dl = NovelDownloader(target_url)
        dl.run()
