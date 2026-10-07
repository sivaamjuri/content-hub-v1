# Content Hub

A headless CMS demo built with **Wagtail + Django REST Framework** (backend) and **Next.js 14** (frontend).

Demonstrates:
- Wagtail Page types with `StreamField` (richtext / image / quote blocks)
- Wagtail Snippets (`Category`) managed from the CMS admin
- Wagtail API v2 headless endpoints (`/api/v2/pages/`)
- JWT authentication via `djangorestframework-simplejwt`
- Layered DRF permission classes (`AllowAny`, `IsAuthenticated`, `IsAdminUser`)
- Next.js App Router SSG — `generateStaticParams` + dynamic `[slug]` route
- CORS configured for local development

---

## Project layout

```
content_hub/          ← Django / Wagtail backend
  content/
    models.py         ← Category snippet + ArticlePage (StreamField)
    serializers.py    ← DRF serializers
    views.py          ← DRF APIViews with permission classes
    urls.py           ← /api/articles/ and /api/categories/
    management/commands/seed_articles.py
  content_hub/
    settings/base.py  ← DRF + JWT + CORS settings
    urls.py           ← Wagtail API v2 + JWT token endpoints
  requirements.txt

content_hub_frontend/ ← Next.js 14 frontend
  src/
    lib/api.js        ← Wagtail API + JWT fetch helpers
    app/
      page.js         ← Homepage — article listing (SSG)
      articles/[slug]/page.js  ← Article detail (SSG + StreamField renderer)
  next.config.js
  .env.local
```

---

## Backend setup

```bash
cd content_hub

# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Create a superuser (for the Wagtail admin)
python manage.py createsuperuser
# Username: admin   Password: <your choice>

# 4. Seed sample articles (optional but recommended for demo)
python manage.py seed_articles

# 5. Start the dev server
python manage.py runserver
```

Backend is now running at **http://localhost:8000**

| URL | Description |
|-----|-------------|
| `/cms/` | Wagtail CMS admin |
| `/django-admin/` | Django admin |
| `/api/v2/pages/?type=content.ArticlePage&fields=title,excerpt,slug,category` | All articles (public) |
| `/api/v2/pages/find/?html_path=/articles/getting-started-with-wagtail/` | Single article by slug |
| `/api/v2/images/` | Images (public) |
| `POST /api/token/` | Get JWT access + refresh tokens |
| `POST /api/token/refresh/` | Refresh access token |
| `GET /api/articles/` | Article list (public, DRF) |
| `GET /api/categories/` | Category list (requires JWT) |
| `POST /api/categories/` | Create category (requires admin JWT) |

---

## Frontend setup

```bash
cd content_hub_frontend

# 1. Install Node dependencies
npm install

# 2. Start the dev server (reads NEXT_PUBLIC_API_URL from .env.local)
npm run dev
```

Frontend is now running at **http://localhost:3000**

To build static pages:
```bash
npm run build   # pre-renders every article at build time via generateStaticParams
npm start       # serve the built output
```

---

## API demo (curl)

```bash
# Get all articles
curl http://localhost:8000/api/v2/pages/?type=content.ArticlePage&fields=title,excerpt,slug,category

# Get one article by slug
curl "http://localhost:8000/api/v2/pages/find/?html_path=/articles/jwt-authentication-django-rest-framework/&fields=title,body,category,excerpt"

# Get JWT token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "<your password>"}'

# Use token to list categories
curl http://localhost:8000/api/categories/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Key concepts for interview discussion

### StreamField
`ArticlePage.body` is a `StreamField` with three block types:
- `richtext` — formatted HTML via `RichTextBlock`
- `image` — Wagtail image reference via `ImageChooserBlock`
- `quote` — structured data (text + author) via `StructBlock`

The API serialises each block as `{"type": "richtext", "value": "...", "id": "..."}`.  
The React frontend switches on `block.type` to render the right component.

### Permission layers
```python
# Public — anyone can read articles
class ArticleListView(APIView):
    permission_classes = [AllowAny]

# Authenticated users can read; only admins can create categories
class CategoryListView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]
```

### SSG with Next.js App Router
```js
// generateStaticParams runs at build time — fetches all slugs from Wagtail
export async function generateStaticParams() {
  const slugs = await getAllArticleSlugs();
  return slugs.map((slug) => ({ slug }));
}

// Each slug gets a pre-rendered static HTML file — no server needed per request
export default async function ArticlePage({ params }) {
  const article = await getArticleBySlug(params.slug);
  // ...
}
```

---

## Pushing to GitHub

```bash
# From the repo root
git init
git add .
git commit -m "feat: Wagtail headless CMS + Next.js SSG demo"
git remote add origin https://github.com/<your-username>/content-hub.git
git push -u origin main
```

> **Tip:** Add `db.sqlite3` and `content_hub_frontend/.env.local` to `.gitignore` before pushing.
