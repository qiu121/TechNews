from typing import List, Dict, Tuple


def filter_news(news_list: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """过滤新闻，根据科技和AI关键字分组"""
    tech_keywords = ['科技', '技术', '互联网', 'IT', '软件']
    ai_keywords = ['AI', '人工智能', 'AGI', 'AIGC', '机器学习', '深度学习', '自然语言处理', '计算机视觉', '自动驾驶',
                   '生成式AI', '大模型', '智能体', '算法', '强化学习', '神经网络', 'GPT', 'Transformer']

    def filter_articles(keywords: List[str], exclude_keywords: List[str]) -> List[Dict[str, str]]:
        """过滤符合条件的新闻文章"""
        filtered_articles = []
        for article in news_list:
            # 获取标题和描述，处理 None 值
            title = article.get('title') or ''
            description = article.get('description') or ''

            # 判断是否包含关键字或排除关键字
            matches_keywords = any(keyword in title or keyword in description for keyword in keywords)
            matches_exclude = any(exclude_keyword in title or exclude_keyword in description
                                  for exclude_keyword in exclude_keywords)

            # 满足条件时，将文章添加到结果列表
            if matches_keywords and not matches_exclude:
                filtered_articles.append(article)

        return filtered_articles

    # 过滤新闻
    filtered_tech_news = filter_articles(tech_keywords, ai_keywords)
    filtered_ai_news = filter_articles(ai_keywords, tech_keywords)

    print(f"🔍 共找到 {len(filtered_tech_news)} 条符合条件的科技资讯：")
    print(f"🔍 共找到 {len(filtered_ai_news)} 条符合条件的AI资讯:")
    return filtered_tech_news[:15], filtered_ai_news[:15]
