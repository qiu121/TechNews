import requests
import json
import os
import time
import hashlib
import base64
import hmac
from datetime import datetime, timedelta
from typing import Tuple, List

# 环境变量获取
FEISHU_WEBHOOK_URL = os.getenv('FEISHU_WEBHOOK_URL')
FEISHU_SIGNING_KEY = os.getenv('FEISHU_SIGNING_KEY')  # 签名密钥
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# https://newsapi.org/docs/endpoints/everything
NEWS_API_URL = 'https://newsapi.org/v2/everything'

current_time = datetime.now()
yesterday = (current_time - timedelta(days=1)).strftime('%Y-%m-%d')


def get_tech_news() -> List[Tuple[str, str, str]]:
    params = {
        'q': 'tech',
        'language': 'zh',
        'sortBy': 'popularity',
        'pageSize': '15',
        'from': yesterday,
        'to': yesterday,
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    full_url = response.request.url
    print(full_url)

    data = response.json()

    # 检查 API 响应状态
    if data.get('status') != 'ok':
        print(json.dumps(data, ensure_ascii=False, indent=2))  # 打印标准 JSON 格式
        print(f"🚫 错误信息: {data.get('message', '未知错误')}")
        return []
    print(f"totalResults: {data.get('totalResults', 'N/A')}")

    # 解析 articles 数组
    articles = data.get('articles', [])
    news_list = []

    for article in articles:
        title = article.get('title', '无标题')
        description = article.get('description', '无描述')
        url = article.get('url', '')
        news_list.append((title, description, url))

    return news_list


def calculate_signature(timestamp: str, secret: str) -> str:
    # 计算签名字符串：timestamp + "\n" + 密钥
    to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    return base64.b64encode(hmac_code).decode('utf-8')


def send_news_to_feishu(news_list: List[Tuple[str, str, str]]) -> dict:
    # 获取当前时间戳
    timestamp = str(int(time.time()))
    # 计算签名
    sign = calculate_signature(timestamp, FEISHU_SIGNING_KEY)

    headers = {'Content-Type': 'application/json'}

    # 构建要推送到飞书的消息内容
    content = [
        [
            {
                "tag": "a",
                "text": f"📢 {news[0]}",
                "href": news[2]
            }
        ] for news in news_list
    ]

    data = {
        "timestamp": f'{timestamp}',
        "sign": f'{sign}',
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "🌐 今日科技资讯",
                    "content": content
                }
            }
        }
    }
    response = requests.post(FEISHU_WEBHOOK_URL, headers=headers, data=json.dumps(data))
    return response.json()


def main():
    tech_news = get_tech_news()
    for news in tech_news:
        print(f'📢 {news[0]}')
        print(f'📝 {news[1]}')
        print(f'📎 {news[2]}')
        print()

    if tech_news:
        send_news_to_feishu(tech_news)


if __name__ == "__main__":
    main()
