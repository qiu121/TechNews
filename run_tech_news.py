from config import (FEISHU_WEBHOOK_URL, FEISHU_SIGNING_KEY,
                    DINGTALK_WEBHOOK_URL, DINGTALK_SIGNING_KEY)
from news import get_tech_news
from dingtalk import send_to_dingtalk
from feishu import send_to_feishu


def send_tech_news():
    tech_news, _ = get_tech_news()

    title = "🌐 今日科技资讯"
    for news in tech_news:
        print(f'{title} - {news["title"]}')
        print(f'📝 {news["description"]}')
        print(f'📎 {news["url"]}')
        print(f'🖼️ {news["urlToImage"]}')
        print(f'🕛 {news["publishedAt"]}')
        print()

    if tech_news:
        pass
        # 推送科技资讯
        send_to_feishu(tech_news, FEISHU_WEBHOOK_URL, FEISHU_SIGNING_KEY, title)
        send_to_dingtalk(tech_news, DINGTALK_WEBHOOK_URL, DINGTALK_SIGNING_KEY, title)


if __name__ == "__main__":
    send_tech_news()
