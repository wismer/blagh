/** @type {import('next').NextConfig} */
const nextConfig = {
  // For development: proxy API calls to Flask backend
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8080/api/:path*',
      },
    ];
  },

  // Optional: Configure for static export if deploying to Cloudflare Pages
  // Uncomment when ready to deploy:
  // output: 'export',
  // images: { unoptimized: true },

  // Cache control headers for Cloudflare
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/posts/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, s-maxage=3600, stale-while-revalidate=86400',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
