"use client";
import {useEffect,useState} from "react";
import {request} from "../../lib/api";
type Data={status:string;limitations:string[];handoff:{steps:string[];requires_creator_approval:boolean}};
export function PublishingEligibility(){const[data,setData]=useState<Data>();useEffect(()=>{void request<Data>("/publishing/eligibility").then(setData).catch(()=>{})},[]);if(!data)return null;return <section className="panel"><h2>Publishing</h2><p>Status: {data.status}</p>{data.limitations.map(x=><p className="error" key={x}>{x}</p>)}<h3>Manual handoff</h3>{data.handoff.steps.map(x=><p key={x}>{x}</p>)}</section>}
