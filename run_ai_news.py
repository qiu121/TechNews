from config import (FEISHU_AI_WEBHOOK_URL, FEISHU_AI_SIGNING_KEY,
                    DINGTALK_AI_WEBHOOK_URL, DINGTALK_AI_SIGNING_KEY)
from news import get_tech_news
from dingtalk import send_to_dingtalk
from feishu import send_to_feishu


def send_ai_news():
    _, ai_news = get_tech_news()

    title = "🤖 今日AI资讯"
    for news in ai_news:
        print(f'{title} - {news["title"]}')
        print(f'📝 {news["description"]}')
        print(f'📎 {news["url"]}')
        print(f'🖼️ {news["urlToImage"]}')
        print(f'🕛 {news["publishedAt"]}')
        print()

    if ai_news:
        pass
        # 推送AI资讯
        send_to_feishu(ai_news, FEISHU_AI_WEBHOOK_URL, FEISHU_AI_SIGNING_KEY, title)
        send_to_dingtalk(ai_news, DINGTALK_AI_WEBHOOK_URL, DINGTALK_AI_SIGNING_KEY, title)


if __name__ == "__main__":
    send_ai_news()
