import json
import time
from typing import Any, List, Dict
from .signature import calculate_signature

import requests


def send_news(news_list: List[Dict[str, str]],
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
