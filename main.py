import requests
import json
import os
import time
import hashlib
import base64
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, List, Dict, Tuple

from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

# 环境变量获取
FEISHU_WEBHOOK_URL = os.getenv('FEISHU_WEBHOOK_URL', '')
FEISHU_SIGNING_KEY = os.getenv('FEISHU_SIGNING_KEY', '')

FEISHU_AI_WEBHOOK_URL = os.getenv('FEISHU_AI_WEBHOOK_URL', '')
FEISHU_AI_SIGNING_KEY = os.getenv('FEISHU_AI_SIGNING_KEY', '')

NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

# 获取当前时间，并设置为本地时区
current_time = datetime.now(timezone.utc).astimezone()
# 格式化为 年-月-日 时:分:秒 时区格式
print(current_time.strftime('%Y-%m-%d %H:%M:%S %Z %z'))
yesterday = (current_time - timedelta(days=1)).strftime('%Y-%m-%d')

newsapi = NewsApiClient(api_key=NEWS_API_KEY)


def get_tech_news() -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    # https://newsapi.org/docs/endpoints/everything
    try:
        data = newsapi.get_everything(q='科技 OR 技术 OR IT OR 互联网 OR 软件 OR AI OR 人工智能',
                                      from_param=yesterday,
                                      to=yesterday,
                                      language='zh',
                                      sort_by='popularity')
    except NewsAPIException as e:
        err_data = e.args[0]
        print("🚫 API 请求错误:")
        print(json.dumps(err_data, ensure_ascii=False, indent=2))  # 打印标准 JSON 格式
        return [], []

    # 检查 API 响应状态
    if data.get('status') != 'ok':
        print(json.dumps(data, ensure_ascii=False, indent=2))  # 打印标准 JSON 格式
        print(f"🚫 错误信息: {data.get('message', '未知错误')}")
        return [], []
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

    return filter_news(news_list)


def filter_news(news_list: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """过滤新闻，根据科技和AI关键字分组"""
    tech_keywords = ['科技', '技术', '互联网', 'IT', '软件']
    ai_keywords = ['AI', '人工智能']

    def filter_articles(keywords: List[str], exclude_keywords: List[str]) -> List[Dict[str, str]]:
        filtered_articles = [
            article for article in news_list if
            any(keyword in article['title'] or keyword in article['description']
                for keyword in keywords)
            and not
            any(exclude_keyword in article['title'] or exclude_keyword in article['description']
                for exclude_keyword in exclude_keywords)
        ]
        return filtered_articles

    # 过滤新闻
    filtered_tech_news = filter_articles(tech_keywords, ai_keywords)
    filtered_ai_news = filter_articles(ai_keywords, tech_keywords)

    print(f"🔍 共找到 {len(filtered_tech_news)} 条符合条件的科技资讯：")
    print(f"🔍 共找到 {len(filtered_tech_news)} 条符合条件的AI资讯：")
    return filtered_tech_news[:15], filtered_ai_news[:15]


def calculate_signature(timestamp: str, secret: str) -> str:
    # 计算签名字符串：timestamp + "\n" + 密钥
    to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    return base64.b64encode(hmac_code).decode('utf-8')


def send_news_to_feishu(news_list: List[Dict[str, str]],
                        webhook_url: str, signing_key: str, title: str) -> Dict[str, Any]:
    try:
        # 获取当前时间戳
        timestamp = str(int(time.time()))
        # 计算签名
        sign = calculate_signature(timestamp, signing_key)
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
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            }
        }
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        print(title)
        print(f'📎 {response.request.url}')
        print(f'🔄 请求方法: {response.request.method}')
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))  # 打印标准 JSON 格式

        return response.json()
    except requests.RequestException as e:
        print("🚫 发送到飞书失败: %s", e)
        return {}


def main():
    tech_news, ai_news = get_tech_news()

    # 设置资讯和对应的标识符
    news_categories = [("🌐 今日科技资讯", tech_news), ("🤖 今日AI资讯", ai_news)]
    for title, news_list in news_categories:
        for news in news_list:
            print(f'{title} - {news["title"]}')
            print(f'📝 {news["description"]}')
            print(f'📎 {news["url"]}')
            print(f'🖼️ {news["urlToImage"]}')
            print(f'🕛 {news["publishedAt"]}')
            print()

    # 推送科技资讯到飞书机器人
    if tech_news:
        pass
        send_news_to_feishu(tech_news, FEISHU_WEBHOOK_URL, FEISHU_SIGNING_KEY, "🌐 今日科技资讯")

    # 推送AI资讯到另一个飞书机器人
    if ai_news:
        pass
        send_news_to_feishu(ai_news, FEISHU_AI_WEBHOOK_URL, FEISHU_AI_SIGNING_KEY, "🤖 今日AI资讯")


if __name__ == "__main__":
    main()
