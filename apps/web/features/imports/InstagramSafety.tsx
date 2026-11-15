"use client";

import { useEffect, useState } from "react";
import { request } from "../../lib/api";

type Safety = { requested_scopes: string[]; denied_scopes: string[]; allowed_http_methods: string[]; publishing: string };

export function InstagramSafety() {
  const [safety, setSafety] = useState<Safety>();
  useEffect(() => { request<Safety>("/instagram/safety").then(setSafety).catch(() => undefined); }, []);
  if (!safety) return null;
  return <section className="safety-card"><p>Protection details</p><h2>Exactly what Verdict can—and cannot—do.</h2><div><article><small>Requested</small><strong>{safety.requested_scopes.join(", ")}</strong><span>Creator history, Page/Business-account discovery, and eligible aggregate insights only.</span></article><article><small>Allowed requests</small><strong>{safety.allowed_http_methods.join(", ")} only</strong><span>The client rejects every write method.</span></article><article><small>Publishing</small><strong>{safety.publishing.replaceAll("_", " ")}</strong><span>No post, delete, comment, message, or account edit access.</span></article></div><details><summary>Permissions Verdict permanently rejects</summary><p>{safety.denied_scopes.join(", ")}</p></details></section>;
}
