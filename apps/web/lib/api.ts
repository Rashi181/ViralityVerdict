export type HealthResponse = {
  status: "ok";
  service: string;
  version: string;
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${apiBaseUrl}/health`, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`API health request failed (${response.status})`);
  }

  return response.json() as Promise<HealthResponse>;
}
