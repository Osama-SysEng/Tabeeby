import React, { useState, useEffect } from 'react';

interface PipelineStage { id: string; name: string; status: string; compounds: number; details: string; }
export const DrugPipeline: React.FC = () => {
  const [stages, setStages] = useState<PipelineStage[]>([]);
  useEffect(() => {
    fetch('/api/drug-discovery/pipeline').then(r => r.json()).then(setStages);
  }, []);
  return (
    <div className="drug-pipeline">
      <h2>مسار اكتشاف الأدوية - Ultra IQ (10 مراحل)</h2>
      {stages.map(s => (
        <div key={s.id} className={`pipeline-stage ${s.status}`}>
          <h3>{s.name}</h3>
          <p>المركبات: {s.compounds}</p>
          <p>{s.details}</p>
        </div>
      ))}
    </div>
  );
};