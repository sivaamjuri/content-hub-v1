/**
 * Homepage — Article Listing
 *
 * Uses Next.js SSG (Static Site Generation):
 * - getStaticProps fetches all articles from Wagtail API v2 at BUILD TIME
 * - Pages are pre-rendered as static HTML — fast, no server needed per request
 * - React renders the JSON response from /api/v2/pages/
 */

import { getArticles } from '@/lib/api';
import Link from 'next/link';

// SSG — runs at build time, not on every request
export async function generateStaticParams() {
  return [];
}

// Fetch data from Wagtail API v2 at build time
async function fetchArticles() {
  try {
    return await getArticles();
  } catch {
    return [];
  }
}

export default async function HomePage() {
  const articles = await fetchArticles();

  return (
    <main style={{ maxWidth: 800, margin: '0 auto', padding: '40px 20px' }}>
      <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8 }}>
        Content Hub
      </h1>
      <p style={{ color: '#6B7280', marginBottom: 40 }}>
        Headless CMS powered by Wagtail · React frontend consuming{' '}
        <code>/api/v2/pages/</code>
      </p>

      {articles.length === 0 ? (
        <p style={{ color: '#9CA3AF' }}>
          No articles yet. Add some from the Wagtail admin at{' '}
          <a href="http://localhost:8000/cms/">localhost:8000/cms/</a>
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {articles.map((article) => (
            <Link
              key={article.id}
              href={`/articles/${article.meta.slug}`}
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div
                style={{
                  border: '1px solid #E5E7EB',
                  borderRadius: 10,
                  padding: '20px 24px',
                  cursor: 'pointer',
                }}
              >
                <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 6 }}>
                  <h2 style={{ fontSize: 17, fontWeight: 600, margin: 0 }}>
                    {article.title}
                  </h2>
                  {article.category && (
                    <span
                      style={{
                        background: '#EEF3FF',
                        color: '#2D6EFF',
                        fontSize: 11,
                        fontWeight: 600,
                        padding: '2px 8px',
                        borderRadius: 20,
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {article.category.name}
                    </span>
                  )}
                </div>
                {article.excerpt && (
                  <p style={{ color: '#6B7280', fontSize: 14, margin: 0 }}>
                    {article.excerpt}
                  </p>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
