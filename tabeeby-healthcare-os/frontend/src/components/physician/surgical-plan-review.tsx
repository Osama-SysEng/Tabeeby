import React, { useState } from 'react';

interface SurgicalPlan { id: string; procedure: string; approach: string; risks: string[]; benefits: string[]; UltraIQScore: number; }
export const SurgicalPlanReview: React.FC<{ planId: string }> = ({ planId }) => {
  const [plan, setPlan] = useState<SurgicalPlan | null>(null);
  const loadPlan = async () => {
    const res = await fetch(`/api/surgical/${planId}`);
    setPlan(await res.json());
  };
  return (
    <div className="surgical-plan-review">
      <button onClick={loadPlan}>تحميل الخطة</button>
      {plan && (
        <div>
          <h2>{plan.procedure}</h2>
          <p>النهج: {plan.approach}</p>
          <h3>المخاطر:</h3>
          <ul>{plan.risks.map(r => <li key={r}>{r}</li>)}</ul>
          <h3>الفوائد:</h3>
          <ul>{plan.benefits.map(b => <li key={b}>{b}</li>)}</ul>
          <p>تقييم Ultra IQ: {plan.UltraIQScore}/100</p>
        </div>
      )}
    </div>
  );
};