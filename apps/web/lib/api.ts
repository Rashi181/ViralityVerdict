export type HealthResponse = {
  status: "ok";
  service: string;
  version: string;
};

export type User = { id: string; email: string; display_name: string };

// Local development uses Next's same-origin proxy. A deployed environment
// supplies its HTTPS API origin via NEXT_PUBLIC_API_BASE_URL.
export const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${apiBaseUrl}/health`, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`API health request failed (${response.status})`);
  }

  return response.json() as Promise<HealthResponse>;
}

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...options,
    credentials: "include",
    // Do not attach a JSON content type to bodyless POSTs such as the
    // read-only Instagram sync. Besides being unnecessary, it forces a CORS
    // preflight in local Chrome development.
    headers: {
      ...(options.body && !(options.body instanceof FormData) ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(body.detail ?? `Request failed (${response.status})`);
  }
  return response.status === 204 ? (undefined as T) : response.json() as Promise<T>;
}
