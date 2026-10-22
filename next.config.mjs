const backendBase = (
  process.env.BACKEND_URL || 
  process.env.NEXT_PUBLIC_API_URL || 
  "http://127.0.0.1:8000"
).replace(/\/$/, "");

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    optimizePackageImports: ["@phosphor-icons/react"],
  },
  async rewrites() {
    return [
      {
        source: "/api/backend/:path*",
        destination: `${backendBase}/api/:path*`,
      },
      {
        source: "/static/:path*",
        destination: `${backendBase}/static/:path*`,
      },
    ];
  },
};

export default nextConfig;

