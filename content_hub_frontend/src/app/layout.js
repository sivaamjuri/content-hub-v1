export const metadata = {
  title: 'Content Hub',
  description: 'A headless CMS demo with Wagtail and Next.js',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}