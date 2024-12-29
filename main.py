from news import get_tech_news
from run_tech_news import send_tech_news
from run_ai_news import send_ai_news

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
    send_tech_news()
    send_ai_news()

if __name__ == "__main__":
    main()
