/**
 * Article Detail Page — [slug]
 *
 * SSG with dynamic routes:
 * - generateStaticParams() pre-fetches all slugs at build time
 * - Each slug gets a pre-rendered static HTML page
 * - StreamField body rendered as typed React components
 *   (switches on block.type: 'richtext' | 'image' | 'quote')
 */

import { getArticleBySlug, getAllArticleSlugs } from '@/lib/api';

// Pre-render all article slugs at build time — SSG
export async function generateStaticParams() {
  const slugs = await getAllArticleSlugs();
  return slugs.map((slug) => ({ slug }));
}

// Render each StreamField block based on its type
function StreamFieldBlock({ block }) {
  switch (block.type) {
    case 'richtext':
      return (
        <div
          className="richtext"
          dangerouslySetInnerHTML={{ __html: block.value }}
          style={{ lineHeight: 1.7, marginBottom: 24 }}
        />
      );

    case 'image':
      return (
        <figure style={{ margin: '24px 0' }}>
          <img
            src={block.value?.meta?.download_url}
            alt={block.value?.title || ''}
            style={{ maxWidth: '100%', borderRadius: 8 }}
          />
          {block.value?.title && (
            <figcaption style={{ color: '#6B7280', fontSize: 13, marginTop: 6 }}>
              {block.value.title}
            </figcaption>
          )}
        </figure>
      );

    case 'quote':
      return (
        <blockquote
          style={{
            borderLeft: '3px solid #2D6EFF',
            paddingLeft: 20,
            margin: '24px 0',
            fontStyle: 'italic',
            color: '#374151',
          }}
        >
          <p style={{ fontSize: 18, marginBottom: 4 }}>{block.value.text}</p>
          {block.value.author && (
            <cite style={{ fontSize: 13, color: '#6B7280' }}>
              — {block.value.author}
            </cite>
          )}
        </blockquote>
      );

    default:
      return null;
  }
}

export default async function ArticlePage({ params }) {
  const article = await getArticleBySlug(params.slug);

  if (!article) {
    return (
      <main style={{ maxWidth: 800, margin: '0 auto', padding: '40px 20px' }}>
        <h1>Article not found</h1>
        <a href="/">← Back to articles</a>
      </main>
    );
  }

  return (
    <main style={{ maxWidth: 720, margin: '0 auto', padding: '40px 20px' }}>
      <a href="/" style={{ color: '#2D6EFF', fontSize: 14, textDecoration: 'none' }}>
        ← Back to articles
      </a>

      <div style={{ marginTop: 24 }}>
        {article.category && (
          <span
            style={{
              background: '#EEF3FF',
              color: '#2D6EFF',
              fontSize: 11,
              fontWeight: 600,
              padding: '3px 10px',
              borderRadius: 20,
              display: 'inline-block',
              marginBottom: 12,
            }}
          >
            {article.category.name}
          </span>
        )}

        <h1 style={{ fontSize: 30, fontWeight: 700, lineHeight: 1.25, marginBottom: 12 }}>
          {article.title}
        </h1>

        {article.excerpt && (
          <p style={{ fontSize: 17, color: '#6B7280', marginBottom: 32 }}>
            {article.excerpt}
          </p>
        )}

        {/* Render StreamField blocks — each typed differently */}
        <div>
          {article.body?.map((block, i) => (
            <StreamFieldBlock key={block.id || i} block={block} />
          ))}
        </div>
      </div>
    </main>
  );
}
