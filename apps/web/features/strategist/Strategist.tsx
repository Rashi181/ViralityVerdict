"use client";
import {useEffect,useState} from "react";
import {request} from "../../lib/api";
type Data={status:string;tools:Record<string,number|boolean>;limitations:string[]};
export function Strategist(){const[data,setData]=useState<Data>();useEffect(()=>{void request<Data>("/strategist/tools").then(setData).catch(()=>{})},[]);if(!data)return null;return <section className="panel"><h2>Verdict strategist</h2><p>Status: {data.status}</p><p>Authenticated read tools: {Object.entries(data.tools).map(([name,value])=>`${name}: ${value}`).join(" · ")}</p>{data.limitations.map(x=><p className="error" key={x}>{x}</p>)}</section>}
