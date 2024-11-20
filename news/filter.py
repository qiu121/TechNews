from typing import List, Dict, Tuple


def filter_news(news_list: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """过滤新闻，根据科技和AI关键字分组"""
    tech_keywords = ['科技', '技术', '互联网', 'IT', '软件']
    ai_keywords = ['AI', '人工智能', 'AGI', 'AIGC', '机器学习', '深度学习', '自然语言处理', '计算机视觉', '自动驾驶',
                   '生成式AI', '大模型', '智能体', '算法', '强化学习', '神经网络', 'GPT', 'Transformer']

    def filter_articles(keywords: List[str], exclude_keywords: List[str]) -> List[Dict[str, str]]:
        filtered_articles = [
            article for article in news_list if
            any(keyword in (article.get('title') or '') or keyword in (article.get('description') or '')
                for keyword in keywords)
            and not
            any(exclude_keyword in (article.get('title') or '') or exclude_keyword in (article.get('description') or '')
                for exclude_keyword in exclude_keywords)
        ]
        return filtered_articles

    # 过滤新闻
    filtered_tech_news = filter_articles(tech_keywords, ai_keywords)
    filtered_ai_news = filter_articles(ai_keywords, tech_keywords)

    print(f"🔍 共找到 {len(filtered_tech_news)} 条符合条件的科技资讯：")
    print(f"🔍 共找到 {len(filtered_ai_news)} 条符合条件的AI资讯:")
    return filtered_tech_news[:15], filtered_ai_news[:15]
