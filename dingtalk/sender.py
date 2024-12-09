import json
import time
from typing import Any, List, Dict
from .signature import calculate_signature

import requests


def send_to_dingtalk(news_list: List[Dict[str, str]],
                          webhook_url: str, signing_key: str, title: str) -> Dict[str, Any]:
    try:
        # 获取当前时间戳
        timestamp = str(round(time.time() * 1000))
        # 计算签名
        sign = calculate_signature(timestamp, signing_key)
        headers = {'Content-Type': 'application/json'}

        params = {
            "timestamp": timestamp,
            "sign": sign,
        }

        # 构建钉钉消息内容
        text_content = "\n".join(
            [f"- [{news['title']}]({news['url']})" for news in news_list]
        )
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"# {title}\n\n{text_content}"
            }
        }

        response = requests.post(webhook_url, headers=headers, data=json.dumps(data), params=params)
        print(title)
        print(f'📎 {response.request.url}')
        print(f'🔄 请求方法: {response.request.method}')
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))  # 打印标准 JSON 格式

        return response.json()
    except requests.RequestException as e:
        print("🚫 发送到钉钉失败: %s", e)
        return {}
