"use client";

import React from "react";

const modules = [
  { title: "Patient workspace", value: "Prototype ready", status: "Available", tone: "border-emerald-500/40 text-emerald-300" },
  { title: "Clinical decision support", value: "Advisory only", status: "Simulation", tone: "border-amber-500/40 text-amber-300" },
  { title: "Medical imaging", value: "Evaluation required", status: "Not validated", tone: "border-amber-500/40 text-amber-300" },
  { title: "RAG knowledge layer", value: "Connector isolated", status: "Sandbox", tone: "border-cyan-500/40 text-cyan-300" },
  { title: "Emergency workflow", value: "Drafts only", status: "Non-actuating", tone: "border-amber-500/40 text-amber-300" },
  { title: "Robot and nano control", value: "Disabled", status: "Safety lock", tone: "border-rose-500/40 text-rose-300" },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl px-6 py-12 lg:px-10">
        <header className="max-w-4xl">
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-cyan-300">Tabeeby Healthcare OS</p>
          <h1 className="text-4xl font-semibold tracking-tight text-white sm:text-6xl">A safe foundation for connected healthcare software.</h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">This release is a research and integration prototype. It provides observable workflows and explicit safety boundaries; it does not diagnose, prescribe, dispatch emergency services, control robots, or perform medical procedures.</p>
        </header>

        <section className="mt-12 rounded-3xl border border-cyan-500/20 bg-slate-900/80 p-6 shadow-2xl shadow-cyan-950/30 sm:p-8" aria-labelledby="release-status">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 id="release-status" className="text-xl font-semibold text-white">Release status</h2>
              <p className="mt-1 text-sm text-slate-400">Local prototype • simulation-first • human review required</p>
            </div>
            <span className="inline-flex w-fit rounded-full border border-amber-400/40 bg-amber-400/10 px-3 py-1 text-sm text-amber-200">Not for clinical use</span>
          </div>
          <div className="mt-6 grid gap-4 sm:grid-cols-3">
            <Metric label="External actions" value="0 attempted" />
            <Metric label="Live actuation" value="Disabled" />
            <Metric label="Audit posture" value="Reviewable" />
          </div>
        </section>

        <section className="mt-10" aria-labelledby="modules">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <h2 id="modules" className="text-2xl font-semibold text-white">Module readiness</h2>
              <p className="mt-1 text-sm text-slate-400">Capabilities are labeled according to the implementation currently shipped.</p>
            </div>
          </div>
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
            {modules.map((module) => <DashboardCard key={module.title} {...module} />)}
          </div>
        </section>

        <footer className="mt-12 border-t border-slate-800 pt-6 text-sm leading-6 text-slate-500">Before any production or clinical deployment, connect validated identity, storage, interoperability, monitoring, regulatory, and qualified human commissioning processes.</footer>
      </div>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4"><p className="text-xs uppercase tracking-wide text-slate-500">{label}</p><p className="mt-2 text-lg font-semibold text-slate-100">{value}</p></div>;
}

function DashboardCard({ title, value, status, tone }: { title: string; value: string; status: string; tone: string }) {
  return <article className={`rounded-2xl border bg-slate-900/70 p-6 transition-colors hover:bg-slate-900 ${tone}`}><div className="flex items-center justify-between gap-3"><h3 className="text-lg font-semibold text-slate-100">{title}</h3><span className="text-xs font-medium uppercase tracking-wide">{status}</span></div><p className="mt-4 text-2xl font-semibold">{value}</p></article>;
}
