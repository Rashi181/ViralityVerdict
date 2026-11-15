import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  async rewrites() {
    // Keep browser calls same-origin in local development. Chromium can block
    // localhost:3000 -> localhost:8000 cross-port requests as private-network
    // traffic even when ordinary CORS headers are correct.
    if (process.env.NODE_ENV !== "development") return [];
    return [{ source: "/api/v1/:path*", destination: "http://127.0.0.1:8000/api/v1/:path*" }];
  },
};

export default nextConfig;
