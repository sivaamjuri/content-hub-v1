/**
 * Wagtail API v2 client
 * Consumed by Next.js pages via getStaticProps / getStaticPaths (SSG)
 */

const WAGTAIL_API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Fetch all published ArticlePages from Wagtail API v2.
 * Used in getStaticProps on the homepage — SSG.
 */
export async function getArticles() {
  const res = await fetch(
    `${WAGTAIL_API}/api/v2/pages/?type=content.ArticlePage&fields=title,excerpt,slug,category`
  );
  if (!res.ok) throw new Error('Failed to fetch articles');
  const data = await res.json();
  return data.items;
}

/**
 * Fetch a single ArticlePage by slug via Wagtail's find endpoint.
 * Used in getStaticProps on [slug] page — SSG.
 */
export async function getArticleBySlug(slug) {
  const res = await fetch(
    `${WAGTAIL_API}/api/v2/pages/find/?html_path=/articles/${slug}/&fields=title,body,category,excerpt`
  );
  if (!res.ok) return null;
  return res.json();
}

/**
 * Fetch all article slugs — used in getStaticPaths to pre-render every article.
 */
export async function getAllArticleSlugs() {
  const res = await fetch(
    `${WAGTAIL_API}/api/v2/pages/?type=content.ArticlePage&fields=slug`
  );
  if (!res.ok) return [];
  const data = await res.json();
  return data.items.map((item) => item.meta.slug);
}

/**
 * JWT auth — get access + refresh tokens
 * Called on login form submit
 */
export async function login(username, password) {
  const res = await fetch(`${WAGTAIL_API}/api/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error('Invalid credentials');
  return res.json(); // { access, refresh }
}

/**
 * JWT refresh — get new access token using refresh token
 * Called automatically when a 401 is received
 */
export async function refreshToken(refresh) {
  const res = await fetch(`${WAGTAIL_API}/api/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  });
  if (!res.ok) throw new Error('Session expired');
  return res.json(); // { access }
}

/**
 * Fetch categories — requires JWT auth
 * Demonstrates protected endpoint call from frontend
 */
export async function getCategories(accessToken) {
  const res = await fetch(`${WAGTAIL_API}/api/categories/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });
  if (res.status === 401) throw new Error('Unauthorized');
  return res.json();
}
