"""
Celery tasks for fetching and processing articles from various sources.
"""
from celery import shared_task
from django.utils import timezone
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from .models import Source, Article


@shared_task
def fetch_new_articles():
    """
    Fetch new articles from all active sources.
    """
    sources = Source.objects.filter(is_active=True)
    total_fetched = 0

    for source in sources:
        try:
            if source.source_type == 'rss':
                count = fetch_from_rss(source)
            else:
                count = fetch_from_web(source)

            total_fetched += count
            source.last_fetched_at = timezone.now()
            source.save()

        except Exception as e:
            print(f"Error fetching from {source.name}: {str(e)}")

    return f"Fetched {total_fetched} new articles from {sources.count()} sources"


def fetch_from_rss(source):
    """
    Fetch articles from an RSS feed.
    """
    feed = feedparser.parse(source.url)
    count = 0

    for entry in feed.entries[:20]:  # Limit to 20 most recent entries
        try:
            # Parse published date
            published_at = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_at = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published_at = datetime(*entry.updated_parsed[:6])

            # Get image URL
            image_url = ''
            if hasattr(entry, 'media_content') and entry.media_content:
                image_url = entry.media_content[0].get('url', '')
            elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get('url', '')

            # Get description
            description = ''
            if hasattr(entry, 'summary'):
                description = entry.summary
            elif hasattr(entry, 'description'):
                description = entry.description

            # Create or update article
            article, created = Article.objects.get_or_create(
                url=entry.link,
                defaults={
                    'title': entry.title[:500],
                    'description': description[:1000] if description else '',
                    'author': entry.get('author', '')[:200],
                    'published_at': published_at,
                    'source': source,
                    'image_url': image_url,
                }
            )

            if created:
                # Add interests from source
                article.interests.set(source.interests.all())
                count += 1

        except Exception as e:
            print(f"Error processing RSS entry from {source.name}: {str(e)}")

    return count


def fetch_from_web(source):
    """
    Fetch articles from a web page (basic scraping).
    This is a simplified version. In production, you'd want more sophisticated scraping.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(source.url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        count = 0

        # Try to find article links (this is a generic approach)
        # In production, you'd have source-specific scrapers
        articles = soup.find_all('article')[:10]  # Limit to 10 articles

        for article_elem in articles:
            try:
                # Try to extract article info
                title_elem = article_elem.find(['h1', 'h2', 'h3', 'a'])
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link = article_elem.find('a')
                if not link or not link.get('href'):
                    continue

                url = link['href']
                if not url.startswith('http'):
                    # Convert relative URL to absolute
                    from urllib.parse import urljoin
                    url = urljoin(source.url, url)

                # Try to find description
                description = ''
                desc_elem = article_elem.find(['p', 'div'], class_=lambda x: x and ('desc' in x.lower() or 'summary' in x.lower()))
                if desc_elem:
                    description = desc_elem.get_text(strip=True)

                # Try to find image
                image_url = ''
                img_elem = article_elem.find('img')
                if img_elem and img_elem.get('src'):
                    image_url = img_elem['src']
                    if not image_url.startswith('http'):
                        from urllib.parse import urljoin
                        image_url = urljoin(source.url, image_url)

                # Create or get article
                article, created = Article.objects.get_or_create(
                    url=url,
                    defaults={
                        'title': title[:500],
                        'description': description[:1000],
                        'source': source,
                        'image_url': image_url,
                        'published_at': timezone.now(),
                    }
                )

                if created:
                    article.interests.set(source.interests.all())
                    count += 1

            except Exception as e:
                print(f"Error processing web article: {str(e)}")
                continue

        return count

    except Exception as e:
        print(f"Error fetching web page from {source.name}: {str(e)}")
        return 0


@shared_task
def fetch_article_content(article_id):
    """
    Fetch full content for a specific article.
    """
    try:
        article = Article.objects.get(id=article_id)

        if article.content:
            return "Article already has content"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(article.url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find main content
        content = ''
        main_content = soup.find(['article', 'main', 'div'], class_=lambda x: x and ('content' in x.lower() or 'article' in x.lower()))

        if main_content:
            # Extract text from paragraphs
            paragraphs = main_content.find_all('p')
            content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])

        article.content = content
        article.save()

        return f"Fetched content for article: {article.title}"

    except Article.DoesNotExist:
        return f"Article {article_id} not found"
    except Exception as e:
        return f"Error fetching article content: {str(e)}"
