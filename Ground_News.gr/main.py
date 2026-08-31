import asyncio
import sys
from analyzer import group_similar_articles
from fetcher import fetch_greek_news
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from summarize import generate_all_summaries_async

console = Console()


def get_bias_color(bias_name):
    """Returns a Rich color style based on the political bias label."""
    bias_lower = bias_name.lower()
    if "left" in bias_lower:
        return "bold red"
    elif "right" in bias_lower:
        return "bold blue"
    elif "center" in bias_lower or "state" in bias_lower:
        return "bold green"
    return "bold yellow"


def display_story_card(story):
    """Renders a visually appealing story card in the terminal using Rich."""
    # 1. Format the Bias Distribution Badges
    bias_badges = []
    for bias, count in story["bias_distribution"].items():
        color = get_bias_color(bias)
        bias_badges.append(f"[{color}]{bias}: {count}[/]")
    bias_line = " | ".join(bias_badges)

    # 2. Render Gemini Summary as Formatted Markdown
    summary_md = Markdown(story["summary"])

    # 3. Format Source Links
    sources_text = ""
    for art in story["articles"]:
        color = get_bias_color(art["bias"])
        sources_text += f"• [[{color}]{art['bias']}[/]] [bold]{art['source']}[/]: {art['title']}\n"
        if art.get("url"):
            sources_text += f"  [dim cyan]{art['url']}[/dim cyan]\n"

    console.print(
        Panel(
            summary_md,
            title=f"[bold white]📰 STORY #{story['topic_id']}: {story['main_title']}[/bold white]",
            subtitle=f"[dim]Total Coverage: {story['article_count']} article(s) | Media Spectrum: {bias_line}[/dim]",
            border_style="cyan",
            expand=True,
        )
    )

    console.print(
        Panel(
            sources_text.strip(),
            title="[bold]🔗 Outlets & Sources[/bold]",
            border_style="dim white",
            expand=True,
        )
    )
    console.print()


def display_grand_totals(total_bias_counts):
    """Renders the total media spectrum coverage as a Rich Table."""
    table = Table(
        title="📊 OVERALL MEDIA SPECTRUM TOTALS",
        header_style="bold magenta",
        border_style="bright_blue",
    )
    table.add_column("Political Spectrum Bias", style="bold white")
    table.add_column("Total Articles Captured", justify="right")

    for bias, count in total_bias_counts.items():
        color = get_bias_color(bias)
        table.add_row(f"[{color}]{bias}[/]", str(count))

    console.print(table)
    console.print()


def main():
    """Main interactive terminal loop."""
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]🇬🇷 GREEK NEWS GROUND-TRUTH AGGREGATOR[/bold cyan]\n"
            "[dim]Powered by TF-IDF Clustering & Google Gemini[/dim]",
            border_style="bold blue",
        )
    )

    while True:
        try:
            query = console.input(
                "\n[bold green]Enter news topic in Greek[/bold green] [dim](or 'q' to quit)[/dim]: "
            ).strip()

            if not query:
                continue

            if query.lower() in ["q", "quit", "exit"]:
                console.print("[bold yellow]Goodbye![/bold yellow]\n")
                sys.exit(0)

            with console.status(
                f"[bold green]Fetching articles for '{query}'...[/bold green]"
            ):
                # Hard limit to top 20 articles max
                raw_articles = fetch_greek_news(query)[:20]

            if not raw_articles:
                console.print(
                    "[bold red]❌ No articles found. Try another query.[/bold red]\n"
                )
                continue

            with console.status(
                "[bold blue]Clustering articles by similarity...[/bold blue]"
            ):
                # Hard limit to top 5 clusters max
                clusters = group_similar_articles(raw_articles)[:5]

            with console.status(
                "[bold magenta]Generating Ground News summaries in parallel via Gemini...[/bold magenta]"
            ):
                # 3. Running async generation concurrently
                summaries = asyncio.run(generate_all_summaries_async(clusters))

            console.rule("[bold cyan]GROUND NEWS RESULTS[/bold cyan]")
            console.print()

            for story in summaries:
                display_story_card(story)

            # Calculate and print Grand Total Table
            total_bias_counts = {}
            for art in raw_articles:
                bias = art.get("bias", "Unknown / Unmapped")
                total_bias_counts[bias] = total_bias_counts.get(bias, 0) + 1

            display_grand_totals(total_bias_counts)

        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Exiting program...[/bold yellow]")
            sys.exit(0)


if __name__ == "__main__":
    main()