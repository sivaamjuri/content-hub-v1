/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow images from Wagtail backend (served from localhost:8000/media/)
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/media/**',
      },
    ],
  },
};

module.exports = nextConfig;
