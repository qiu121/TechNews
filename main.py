import requests
import json
import os
import time
import hashlib
import base64
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, List, Dict

# 环境变量获取
FEISHU_WEBHOOK_URL = os.getenv('FEISHU_WEBHOOK_URL')
FEISHU_SIGNING_KEY = os.getenv('FEISHU_SIGNING_KEY')  # 签名密钥
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

NEWS_API_URL = 'https://newsapi.org/v2/everything'

# 获取当前时间，并设置为本地时区
current_time = datetime.now(timezone.utc).astimezone()
# 格式化为 年-月-日 时:分:秒 时区格式
print(current_time.strftime('%Y-%m-%d %H:%M:%S %Z %z'))
yesterday = (current_time - timedelta(days=1)).strftime('%Y-%m-%d')


def get_tech_news() -> List[Dict[str, str]]:
    # https://newsapi.org/docs/endpoints/everything
    
    params = {
        'q': '科技 OR 技术 OR IT OR 互联网 OR AI OR 人工智能',
        'language': 'zh',
        'sortBy': 'relevancy',
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
        news_item = {
            'title': article.get('title', '无标题'),
            'description': article.get('description', '无描述'),
            'url': article.get('url', ''),
            'urlToImage': article.get('urlToImage', ''),
            'publishedAt': article.get('publishedAt', '')
        }
        news_list.append(news_item)

    return filter_tech_news(news_list)


def filter_tech_news(news_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # 用于进一步筛选的科技关键词列表
    tech_keywords = ['科技', '技术', '互联网', 'AI', '人工智能', 'IT', '软件', '硬件']

    filtered_news = [
        article for article in news_list
        # 检查每篇文章的标题或描述中是否包含任一科技关键词
        if any(keyword in article['title'] or keyword in article['description'] for keyword in tech_keywords)
    ]

    print(f"共找到 {len(filtered_news)} 条符合条件的资讯：")
    return filtered_news


def calculate_signature(timestamp: str, secret: str) -> str:
    # 计算签名字符串：timestamp + "\n" + 密钥
    to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    return base64.b64encode(hmac_code).decode('utf-8')


def send_news_to_feishu(news_list: List[Dict[str, str]]) -> Dict[str, Any]:
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
                "text": f"📢 {news['title']}",
                "href": news['url']
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
    full_url = response.request.url
    print(full_url)
    print(f'请求方法: {response.request.method}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))  # 打印标准 JSON 格式

    return response.json()


def main():
    tech_news = get_tech_news()
    for news in tech_news:
        print(f'📢 {news["title"]}')
        print(f'📝 {news["description"]}')
        print(f'📎 {news["url"]}')
        print(f'🖼️  {news["urlToImage"]}')
        print(f'🕛 {news["publishedAt"]}')
        print()

    if tech_news:
        send_news_to_feishu(tech_news)


if __name__ == "__main__":
    main()
