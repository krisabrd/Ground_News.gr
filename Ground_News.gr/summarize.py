import asyncio
from google import genai
from config import GEMINI_API_KEY


def build_ground_news_prompt(cluster):
    """Formats cluster data into a structured prompt for Gemini."""
    articles_text = ""
    for idx, art in enumerate(cluster["articles"], 1):
        articles_text += (
            f"Article {idx}:\n"
            f"- Source: {art['source']} (Bias: {art['bias']})\n"
            f"- Title: {art['title']}\n"
            f"- Description: {art['description']}\n\n"
        )

    prompt = f"""
You are an objective news synthesis system modeled after Ground News.
Your goal is to take multiple news reports covering the same event from different media outlets and produce a balanced, neutral, and fact-focused summary.

Story Topic: "{cluster['main_title']}"
Media Bias Distribution for this Story: {cluster['bias_distribution']}

Articles Data:
{articles_text}

Instructions:
1. **Core Ground Summary**: Provide a 2-3 sentence purely factual summary of the core event that all sources agree on. Avoid emotional or partisan framing.
2. **Coverage Insights & Perspectives**: Briefly note how different sides (Left, Center, Right, Independent) frame or emphasize the story, if noticeable differences exist.
3. **Coverage Balance**: Briefly state if this story has balanced coverage across the media spectrum or if it skews toward a specific side.

Format the response clearly using Markdown sections. Answer in Greek.
"""
    return prompt


async def summarize_cluster_async(client, cluster):
    """Sends a single story cluster asynchronously to Gemini."""
    if not cluster or not cluster.get("articles"):
        return {
            "topic_id": cluster.get("topic_id"),
            "main_title": cluster.get("main_title"),
            "bias_distribution": cluster.get("bias_distribution", {}),
            "article_count": cluster.get("article_count", 0),
            "summary": "Δεν υπάρχουν διαθέσιμα άρθρα για σύνοψη.",
            "articles": cluster.get("articles", []),
        }

    prompt = build_ground_news_prompt(cluster)

    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        summary_text = response.text
    except Exception as e:
        summary_text = f"Σφάλμα κατά τη δημιουργία της σύνοψης: {e}"

    return {
        "topic_id": cluster["topic_id"],
        "main_title": cluster["main_title"],
        "bias_distribution": cluster["bias_distribution"],
        "article_count": cluster["article_count"],
        "summary": summary_text,
        "articles": cluster["articles"],
    }

async def generate_all_summaries_async(clustered_data):
    """Fires parallel async requests for all story clusters simultaneously."""
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Create asynchronous tasks for every cluster
    tasks = [
        summarize_cluster_async(client, cluster) for cluster in clustered_data
    ]

    # Run all tasks concurrently in parallel
    summaries = await asyncio.gather(*tasks)
    return list(summaries)
