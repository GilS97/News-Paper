"""
Celery tasks for sending email digests to subscribed users.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import EmailSubscription, EmailLog
from articles.models import Article


@shared_task
def send_daily_digests():
    """
    Send daily email digests to users subscribed to daily emails.
    """
    subscriptions = EmailSubscription.objects.filter(
        frequency='daily',
        is_active=True
    )
    sent_count = 0

    for subscription in subscriptions:
        try:
            send_digest_email(subscription, days=1)
            sent_count += 1
        except Exception as e:
            print(f"Error sending daily digest to {subscription.user.email}: {str(e)}")

    return f"Sent {sent_count} daily digests"


@shared_task
def send_weekly_digests():
    """
    Send weekly email digests to users subscribed to weekly emails.
    """
    subscriptions = EmailSubscription.objects.filter(
        frequency='weekly_1',
        is_active=True
    )
    sent_count = 0

    for subscription in subscriptions:
        try:
            send_digest_email(subscription, days=7)
            sent_count += 1
        except Exception as e:
            print(f"Error sending weekly digest to {subscription.user.email}: {str(e)}")

    return f"Sent {sent_count} weekly digests"


@shared_task
def send_biweekly_digests():
    """
    Send email digests to users subscribed to biweekly (2x/week) emails.
    """
    subscriptions = EmailSubscription.objects.filter(
        frequency='weekly_2',
        is_active=True
    )
    sent_count = 0

    for subscription in subscriptions:
        try:
            send_digest_email(subscription, days=3)
            sent_count += 1
        except Exception as e:
            print(f"Error sending biweekly digest to {subscription.user.email}: {str(e)}")

    return f"Sent {sent_count} biweekly digests"


@shared_task
def send_triweekly_digests():
    """
    Send email digests to users subscribed to triweekly (3x/week) emails.
    """
    subscriptions = EmailSubscription.objects.filter(
        frequency='weekly_3',
        is_active=True
    )
    sent_count = 0

    for subscription in subscriptions:
        try:
            send_digest_email(subscription, days=2)
            sent_count += 1
        except Exception as e:
            print(f"Error sending triweekly digest to {subscription.user.email}: {str(e)}")

    return f"Sent {sent_count} triweekly digests"


def send_digest_email(subscription, days=1):
    """
    Send a digest email to a specific user.
    """
    user = subscription.user

    # Get user's interests
    user_interest_ids = user.user_interests.values_list('interest_id', flat=True)

    if not user_interest_ids:
        # User has no interests, skip
        return

    # Get recent articles matching user's interests
    cutoff_date = timezone.now() - timedelta(days=days)
    articles = Article.objects.filter(
        interests__in=user_interest_ids,
        created_at__gte=cutoff_date
    ).distinct().order_by('-published_at')[:10]

    if not articles.exists():
        # No new articles, skip
        return

    # Prepare email content
    subject = f"Votre digest News Paper - {articles.count()} nouveaux articles"

    # Create HTML email
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #4F46E5;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .article {{
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin: 20px 0;
                padding: 15px;
                background-color: #f9f9f9;
            }}
            .article h3 {{
                margin: 0 0 10px 0;
                color: #4F46E5;
            }}
            .article p {{
                margin: 10px 0;
                color: #666;
            }}
            .article a {{
                color: #4F46E5;
                text-decoration: none;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>News Paper Digest</h1>
            <p>Bonjour {user.first_name or user.username},</p>
            <p>Voici vos {articles.count()} derniers articles personnalisés</p>
        </div>
    """

    for article in articles:
        html_message += f"""
        <div class="article">
            <h3>{article.title}</h3>
            <p><strong>Source:</strong> {article.source.name}</p>
            {f'<p><strong>Auteur:</strong> {article.author}</p>' if article.author else ''}
            {f'<p>{article.description[:200]}...</p>' if article.description else ''}
            <p><a href="{article.url}" target="_blank">Lire l'article →</a></p>
        </div>
        """

    html_message += f"""
        <div class="footer">
            <p>Vous recevez cet email car vous êtes abonné à News Paper.</p>
            <p>Pour modifier vos préférences, connectez-vous à votre compte.</p>
        </div>
    </body>
    </html>
    """

    # Plain text version
    plain_message = f"""
    Bonjour {user.first_name or user.username},

    Voici vos {articles.count()} derniers articles personnalisés :

    """

    for article in articles:
        plain_message += f"""
    {article.title}
    Source: {article.source.name}
    {article.description[:200] if article.description else ''}...
    Lire: {article.url}

    ---
    """

    plain_message += """
    Vous recevez cet email car vous êtes abonné à News Paper.
    Pour modifier vos préférences, connectez-vous à votre compte.
    """

    try:
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )

        # Log success
        EmailLog.objects.create(
            subscription=subscription,
            status='sent',
            subject=subject,
            article_count=articles.count()
        )

        # Update last sent time
        subscription.last_sent_at = timezone.now()
        subscription.save()

    except Exception as e:
        # Log failure
        EmailLog.objects.create(
            subscription=subscription,
            status='failed',
            subject=subject,
            article_count=articles.count(),
            error_message=str(e)
        )
        raise
