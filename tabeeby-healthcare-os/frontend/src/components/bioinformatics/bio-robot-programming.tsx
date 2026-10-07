import React, { useState } from 'react';

interface BioRobotProgram { id: string; name: string; steps: string[]; condition: string; payload: string; }
export const BioRobotProgramming: React.FC = () => {
  const [programs, setPrograms] = useState<BioRobotProgram[]>([]);
  const createProgram = async (spec: string) => {
    const res = await fetch('/api/bio-robot/generate-program', {
      method: 'POST',
      body: JSON.stringify({ specification: spec })
    });
    setPrograms([...programs, await res.json()]);
  };
  return (
    <div className="bio-robot-programming">
      <h2>برمجة الروبوتات الحيوية</h2>
      <textarea placeholder="وصف المهمة... ex: 'تدمير خلايا الورم في الفص الكبدي الأيسر'" />
      <button onClick={() => createProgram(' destroyer tumor cells ')}>توليد البرنامج</button>
      {programs.map(p => (
        <div key={p.id} className="program-card">
          <h3>{p.name}</h3>
          <pre>{JSON.stringify(p, null, 2)}</pre>
        </div>
      ))}
    </div>
  );
};