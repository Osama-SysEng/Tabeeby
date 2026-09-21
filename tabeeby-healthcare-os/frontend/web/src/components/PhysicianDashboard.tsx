"use client";

import { useMemo, useState } from "react";

type PatientRow = { id: string; status: "stable" | "review" | "simulation"; lastUpdate: string };

const initialRows: PatientRow[] = [
  { id: "patient-demo-001", status: "review", lastUpdate: "No live data" },
  { id: "patient-demo-002", status: "stable", lastUpdate: "Synthetic record" },
];

export function PhysicianDashboard() {
  const [rows] = useState(initialRows);
  const reviewed = useMemo(() => rows.filter((row) => row.status === "review").length, [rows]);
  return (
    <section aria-labelledby="physician-dashboard" className="mt-10 rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div><h2 id="physician-dashboard" className="text-2xl font-semibold text-white">Physician workspace</h2><p className="mt-1 text-sm text-slate-400">Synthetic/demo records only • human review required</p></div>
        <span className="rounded-full border border-amber-400/40 px-3 py-1 text-xs text-amber-200">{reviewed} pending review</span>
      </div>
      <div className="mt-5 overflow-x-auto"><table className="w-full min-w-[520px] text-left text-sm"><thead className="text-slate-500"><tr><th className="pb-3">Patient reference</th><th className="pb-3">State</th><th className="pb-3">Last update</th></tr></thead><tbody>{rows.map((row) => <tr key={row.id} className="border-t border-slate-800"><td className="py-4 font-medium text-slate-200">{row.id}</td><td className="py-4 text-amber-200">{row.status}</td><td className="py-4 text-slate-400">{row.lastUpdate}</td></tr>)}</tbody></table></div>
    </section>
  );
}
