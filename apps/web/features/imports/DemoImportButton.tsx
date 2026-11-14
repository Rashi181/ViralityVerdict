"use client";
import { useState } from "react";
import { request } from "../../lib/api";
export function DemoImportButton() {
  const [message, setMessage] = useState<string>();
  return <section className="panel"><h2>Demo data</h2><p>This creates synthetic demo data only. It is not Instagram data.</p><button onClick={async () => { try { await request("/imports/demo", { method: "POST" }); setMessage("Synthetic demo import saved."); } catch (e) { setMessage(e instanceof Error ? e.message : "Import failed"); } }}>Load synthetic demo</button>{message && <p role="status">{message}</p>}</section>;
}
