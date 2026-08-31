from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import MEDIA_BIAS_MAP

def get_media_bias(source_name, url=""):
    '''Looks up political bias based on domain name or source string.'''
    source_lower = source_name.lower()
    url_lower = url.lower()

    for domain, bias in MEDIA_BIAS_MAP.items():
        if domain in source_lower or domain in url_lower:
            return bias
            
    return "Unknown / Unmapped"


def calculate_source_distribution(articles):
    '''
    Calculates the breakdown of political biases across a list of articles.
    Returns a dictionary with counts per bias category.
    '''
    distribution = {}
    for article in articles:
        bias = article.get("bias", "Unknown / Unmapped")
        distribution[bias] = distribution.get(bias, 0) + 1
    return distribution


def group_similar_articles(articles, similarity_threshold=0.25):
    '''
    Groups articles covering the same story using TF-IDF and Cosine Similarity.
    Also tags each article with its media bias and attaches the source distribution.
    '''
    if not articles:
        return []

    # Tag each article with its media bias
    for article in articles:
        article["bias"] = get_media_bias(article["source"], article.get("url", ""))

    corpus = [f"{art['title']} {art['description']}" for art in articles]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    clusters = []
    visited = set()

    for i in range(len(articles)):
        if i in visited:
            continue

        current_cluster = [articles[i]]
        visited.add(i)

        for j in range(i + 1, len(articles)):
            if j not in visited:
                if similarity_matrix[i][j] >= similarity_threshold:
                    current_cluster.append(articles[j])
                    visited.add(j)

        clusters.append({
            "topic_id": len(clusters) + 1,
            "main_title": current_cluster[0]["title"],
            "article_count": len(current_cluster),
            "bias_distribution": calculate_source_distribution(current_cluster),
            "articles": current_cluster,
        })

    return clusters
