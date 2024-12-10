from config import (FEISHU_WEBHOOK_URL, FEISHU_SIGNING_KEY,
                    FEISHU_AI_SIGNING_KEY, FEISHU_AI_WEBHOOK_URL,
                    DINGTALK_WEBHOOK_URL, DINGTALK_SIGNING_KEY,
                    DINGTALK_AI_WEBHOOK_URL, DINGTALK_AI_SIGNING_KEY)
from news import get_tech_news
from dingtalk import send_to_dingtalk
from feishu import send_to_feishu


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
        send_to_feishu(tech_news, FEISHU_WEBHOOK_URL, FEISHU_SIGNING_KEY, "🌐 今日科技资讯")
        send_to_dingtalk(tech_news, DINGTALK_WEBHOOK_URL, DINGTALK_SIGNING_KEY, "🌐 今日科技资讯")

    # 推送AI资讯到另一个飞书机器人
    if ai_news:
        pass
        send_to_feishu(ai_news, FEISHU_AI_WEBHOOK_URL, FEISHU_AI_SIGNING_KEY, "🤖 今日AI资讯")
        send_to_dingtalk(ai_news, DINGTALK_AI_WEBHOOK_URL, DINGTALK_AI_SIGNING_KEY, "🤖 今日AI资讯")


if __name__ == "__main__":
    main()
