/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images-dynamic-arcteryx.imgix.net',
      },
    ],
  },
};

module.exports = nextConfig;
