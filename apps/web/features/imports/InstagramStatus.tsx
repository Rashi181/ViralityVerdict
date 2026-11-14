"use client";
import { useEffect, useState } from "react";
import { request } from "../../lib/api";
export function InstagramStatus() { const [detail, setDetail] = useState("Checking Instagram connection…"); useEffect(() => { request<{detail:string}>("/instagram/status").then(x => setDetail(x.detail)).catch(e => setDetail(e.message)); }, []); return <section className="panel"><h2>Instagram connection</h2><p>{detail}</p></section>; }
