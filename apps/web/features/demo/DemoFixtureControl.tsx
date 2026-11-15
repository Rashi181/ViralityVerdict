"use client";

import { useEffect, useState } from "react";
import { request } from "../../lib/api";

type DemoStatus = { available: boolean; detail: string };
type DemoLoad = { status: "loaded" | "already_loaded"; media_count: number; aggregate_count: number; limitations: string[] };

export function DemoFixtureControl() {
  const [status, setStatus] = useState<DemoStatus>();
  const [result, setResult] = useState<DemoLoad>();
  const [error, setError] = useState<string>();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    void request<DemoStatus>("/demo/status").then(setStatus).catch(() => undefined);
  }, []);

  if (!status?.available) return null;

  async function loadFixture() {
    setLoading(true);
    setError(undefined);
    try {
      setResult(await request<DemoLoad>("/demo/load-fixture", { method: "POST" }));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not load the demonstration data.");
    } finally {
      setLoading(false);
    }
  }

  return <section className="panel demo-fixture-control">
    <p className="insight-kicker">Local demonstration mode</p>
    <h2>Load the judge-demo workspace</h2>
    <p>This loads a local, synthetic dataset into only your signed-in workspace. It is not a CSV upload, is not a live Meta sync, and can never be presented as real audience data.</p>
    <button className="button" type="button" onClick={() => void loadFixture()} disabled={loading}>
      {loading ? "Loading demonstration data…" : result ? "Demonstration data loaded" : "Load synthetic demonstration data"}
    </button>
    {result && <p className="demo-fixture-result">{result.status === "already_loaded" ? "Already loaded:" : "Loaded:"} {result.media_count} synthetic posts and {result.aggregate_count} aggregate audience fields. Open Creator intelligence to inspect the evidence and hypotheses.</p>}
    {error && <p className="form-error">{error}</p>}
  </section>;
}
