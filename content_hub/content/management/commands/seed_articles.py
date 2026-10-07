"""
Management command: python manage.py seed_articles

Creates 3 sample ArticlePage objects under the root page so you can
demo the API immediately after running migrations.

Usage:
    python manage.py seed_articles
"""

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from wagtail.rich_text import RichText

from content.models import Category, ArticlePage


ARTICLES = [
    {
        "title": "Getting Started with Wagtail CMS",
        "slug": "getting-started-with-wagtail",
        "excerpt": "A quick-start guide to building headless CMS sites with Wagtail and its powerful API v2.",
        "category_name": "Technology",
        "body": [
            {
                "type": "richtext",
                "value": (
                    "<h2>What is Wagtail?</h2>"
                    "<p>Wagtail is a Django-powered CMS that ships with a built-in headless API (v2). "
                    "You define <strong>Page types</strong> as Python classes and Wagtail handles "
                    "the admin UI, versioning, workflow, and REST endpoints automatically.</p>"
                    "<h2>StreamField</h2>"
                    "<p>The <code>StreamField</code> lets editors mix block types freely — "
                    "rich text, images, pull quotes — in any order. Every block is stored as "
                    "typed JSON and returned by the API exactly as you see here.</p>"
                ),
            },
            {
                "type": "quote",
                "value": {
                    "text": "Wagtail gives you the editorial power of a traditional CMS with the flexibility of a headless architecture.",
                    "author": "Wagtail Docs",
                },
            },
        ],
    },
    {
        "title": "JWT Authentication in Django REST Framework",
        "slug": "jwt-authentication-django-rest-framework",
        "excerpt": "How to implement short-lived access tokens and long-lived refresh tokens with djangorestframework-simplejwt.",
        "category_name": "Backend",
        "body": [
            {
                "type": "richtext",
                "value": (
                    "<h2>Why JWT?</h2>"
                    "<p>JSON Web Tokens are stateless — the server doesn't need to query a "
                    "session store on every request. The access token is signed and self-contained; "
                    "the server just verifies the signature.</p>"
                    "<h2>Token Lifecycle</h2>"
                    "<ul>"
                    "<li><strong>POST /api/token/</strong> — exchange credentials for an "
                    "access token (5 min) and a refresh token (1 day).</li>"
                    "<li><strong>POST /api/token/refresh/</strong> — swap the refresh token "
                    "for a new access token without re-entering credentials.</li>"
                    "</ul>"
                    "<p>Keep the access token in memory (never localStorage) and the refresh "
                    "token in an httpOnly cookie so it's invisible to JavaScript.</p>"
                ),
            },
            {
                "type": "quote",
                "value": {
                    "text": "Never store tokens in localStorage — XSS attacks can read anything JavaScript can.",
                    "author": "OWASP",
                },
            },
        ],
    },
    {
        "title": "Next.js SSG with a Headless CMS",
        "slug": "nextjs-ssg-headless-cms",
        "excerpt": "Using generateStaticParams and the Wagtail API to pre-render every article page at build time.",
        "category_name": "Frontend",
        "body": [
            {
                "type": "richtext",
                "value": (
                    "<h2>Static Site Generation (SSG)</h2>"
                    "<p>Next.js can pre-render pages at <em>build time</em> by fetching data "
                    "once during <code>next build</code>. The result is a set of static HTML "
                    "files — fast to serve, no server needed per request.</p>"
                    "<h2>generateStaticParams</h2>"
                    "<p>In the App Router, <code>generateStaticParams()</code> returns all "
                    "the slug values that should be pre-built. Next.js renders one HTML file "
                    "per slug. The Wagtail <code>/api/v2/pages/find/</code> endpoint resolves "
                    "a URL path back to a page object, making slug-based routing trivial.</p>"
                    "<h2>StreamField in React</h2>"
                    "<p>Each block in the API response has a <code>type</code> field. "
                    "A simple <code>switch</code> on <code>block.type</code> renders the "
                    "right component — <code>richtext</code> → <code>dangerouslySetInnerHTML</code>, "
                    "<code>image</code> → <code>&lt;img&gt;</code>, "
                    "<code>quote</code> → <code>&lt;blockquote&gt;</code>.</p>"
                ),
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the database with 3 sample ArticlePages and their categories."

    def handle(self, *args, **options):
        # Find the root page to attach articles under
        try:
            root_page = Page.objects.get(depth=1)
            # Try to find a sensible parent — the default home page at depth 2
            home_page = Page.objects.filter(depth=2).first()
            if not home_page:
                home_page = root_page
        except Page.DoesNotExist:
            self.stderr.write("No root page found. Have you run migrations?")
            return

        created_count = 0

        for data in ARTICLES:
            # Skip if slug already exists
            if ArticlePage.objects.filter(slug=data["slug"]).exists():
                self.stdout.write(f'  skip  "{data["title"]}" (already exists)')
                continue

            # Get or create category
            category, _ = Category.objects.get_or_create(
                name=data["category_name"],
                defaults={"slug": data["category_name"].lower()},
            )

            # Build StreamField value
            body_value = []
            for block in data["body"]:
                if block["type"] == "richtext":
                    body_value.append(("richtext", RichText(block["value"])))
                else:
                    body_value.append((block["type"], block["value"]))

            article = ArticlePage(
                title=data["title"],
                slug=data["slug"],
                excerpt=data["excerpt"],
                category=category,
                body=body_value,
            )

            home_page.add_child(instance=article)
            # Publish immediately
            article.save_revision().publish()

            self.stdout.write(f'  ✓  "{data["title"]}"')
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone — {created_count} article(s) created, "
                f"{len(ARTICLES) - created_count} skipped."
            )
        )
