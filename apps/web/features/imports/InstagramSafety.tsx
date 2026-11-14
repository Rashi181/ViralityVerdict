"use client";

import { useEffect, useState } from "react";
import { request } from "../../lib/api";

type Safety = { requested_scopes: string[]; denied_scopes: string[]; allowed_http_methods: string[]; publishing: string };

export function InstagramSafety() {
  const [safety, setSafety] = useState<Safety>();
  useEffect(() => { request<Safety>("/instagram/safety").then(setSafety).catch(() => undefined); }, []);
  if (!safety) return null;
  return <section className="panel"><h2>Account safety promise</h2><p>Verdict is read-only. It requests: {safety.requested_scopes.join(", ")}.</p><p>Verdict allows Meta requests by: {safety.allowed_http_methods.join(", ")} only.</p><p>Publishing is {safety.publishing.replaceAll("_", " ")}. No post, delete, comment, message, or account-edit permission is requested.</p><details><summary>Permissions Verdict permanently rejects</summary><p>{safety.denied_scopes.join(", ")}</p></details></section>;
}
