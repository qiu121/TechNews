import json
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Tuple
from .filter import filter_news
from config import NEWS_API_KEY

from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException


# 获取当前时间，并设置为本地时区
current_time = datetime.now(timezone.utc).astimezone()
# 格式化为 年-月-日 时:分:秒 时区格式
print(current_time.strftime('%Y-%m-%d %H:%M:%S %Z %z'))
yesterday = (current_time - timedelta(days=1)).strftime('%Y-%m-%d')

newsapi = NewsApiClient(api_key=NEWS_API_KEY)


def get_tech_news() -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    # https://newsapi.org/docs/endpoints/everything
    try:
        data = newsapi.get_everything(q='科技 OR IT OR 互联网 OR AI OR 人工智能',
                                      from_param=yesterday,
                                      to=yesterday,
                                      language='zh',
                                      sort_by='relevancy')
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
