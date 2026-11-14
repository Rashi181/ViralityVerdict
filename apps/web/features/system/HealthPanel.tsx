"use client";

import { useEffect, useState } from "react";
import { getHealth, type HealthResponse } from "../../lib/api";

export function HealthPanel() {
  const [health, setHealth] = useState<HealthResponse>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    getHealth().then(setHealth).catch((reason: unknown) => {
      setError(reason instanceof Error ? reason.message : "API health request failed");
    });
  }, []);

  return (
    <section aria-labelledby="api-status" className="panel">
      <h2 id="api-status">API connection</h2>
      {health ? (
        <dl>
          <dt>Status</dt><dd>{health.status}</dd>
          <dt>Service</dt><dd>{health.service}</dd>
          <dt>Version</dt><dd>{health.version}</dd>
        </dl>
      ) : error ? <p className="error">Unavailable: {error}</p> : <p>Checking API health…</p>}
    </section>
  );
}
