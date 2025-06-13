import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Optional, List, Tuple

# 配置
BGMI_WEB_URL = "https://bgm.tv/anime/list/{username}/wish?orderby=date&page={page}"
API_UPDATE_URL = "https://api.bgm.tv/v0/users/-/collections/{subject_id}"
USERNAME = os.getenv("BGMI_USERNAME")
API_KEY = os.getenv("BGMI_API_KEY")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Authorization": f"Bearer {API_KEY}"
}

def format_chinese_date(date_str: str) -> str:
    """日期格式化"""
    match = re.search(r'(\d+)年(\d+)月(\d+)日', date_str)
    if match:
        y, m, d = match.groups()
        return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
    print(f" 未找到日期: {date_str}")
    return ""

def fetch_page(page: int) -> Optional[str]:
    """获取网页内容"""
    url = BGMI_WEB_URL.format(username=USERNAME, page=page)
    try:
        response = requests.get(url, headers={"User-Agent": headers["User-Agent"]}, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f" 网页请求失败 (第{page}页): {e}")
        return None

def parse_subjects(html: str) -> List[Tuple[str, str]]:
    """解析网页获取 subject_id 和格式化日期"""
    soup = BeautifulSoup(html, 'html.parser')
    subjects = []

    # 获取所有条目卡片
    items = soup.select('#browserItemList li.item')

    for item in items:
        # 提取 subject_id
        cover = item.select_one('.subjectCover')
        if not cover:
            continue
        subject_id = cover['href'].split('/')[-1]

        # 提取并格式化日期
        date_tag = item.select_one('.info.tip')
        if not date_tag:
            print(f" 条目 {subject_id} 缺少日期标签")
            continue

        raw_date = date_tag.get_text().strip()
        formatted_date = format_chinese_date(raw_date)
        if not formatted_date:
            continue

        subjects.append((subject_id, formatted_date))
        print(f"   → 条目 {subject_id} | {formatted_date}")

    return subjects

def update_to_watching(subject_id: str, date: str, dry_run: bool) -> bool:
    """更新条目状态并返回是否成功"""
    today = datetime.now().strftime("%Y-%m-%d")
    if date != today:
        return False

    if dry_run:
        print(f" [安全模式] 应更新条目 {subject_id} 为「在看」")
        return True

    try:
        response = requests.post(
            API_UPDATE_URL.format(subject_id=subject_id),
            json={"type": 3},
            headers=headers,
            timeout=10
        )
        if response.status_code == 202:
            print(f" 成功更新条目 {subject_id} 为「在看」")
            return True
        print(f" 更新失败 (HTTP {response.status_code}): {response.text}")
    except Exception as e:
        print(f" 更新异常: {e}")
    return False

def main(dry_run: bool = False):
    print(f"\n 开始同步 Bangumi「想看」列表 ({'安全模式' if dry_run else '正常模式'})")
    print(f" 当前日期: {datetime.now().strftime('%Y-%m-%d')}")
    page = 1

    while True:
        print(f"\n 正在处理第 {page} 页...")
        html = fetch_page(page)
        if not html:
            break

        subjects = parse_subjects(html)
        if not subjects:
            print(" 没有更多条目")
            break

        for subject_id, date in subjects:
            if date < datetime.now().strftime("%Y-%m-%d"):
                print(f" 遇到早于今天的条目 ({date})，终止翻页")
                return

            update_to_watching(subject_id, date, dry_run)

        page += 1

    print("\n 同步完成")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="安全模式（不实际修改）")
    args = parser.parse_args()

    if not USERNAME:
        print(" 请设置环境变量 BGMI_USERNAME")
        exit(1)

    main(dry_run=args.dry_run)
