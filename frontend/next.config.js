if (process.env.NODE_ENV !== 'production') {
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
}

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimize: process.env.NODE_ENV !== 'production',
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'image.tmdb.org',
        pathname: '/t/p/**',
      },
    ],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NODE_ENV === 'production' ? '/api/v1' : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'),
  },
};

module.exports = nextConfig;
