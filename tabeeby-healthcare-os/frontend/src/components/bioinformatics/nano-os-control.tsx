import React, { useState } from 'react';

interface NanoMission { id: string; target: string; status: string; progress: number; }
export const NanoOSControl: React.FC = () => {
  const [missions, setMissions] = useState<NanoMission[]>([]);
  const deployNano = async (target: string, payload: string) => {
    const res = await fetch('/api/nano-os/deploy', {
      method: 'POST',
      body: JSON.stringify({ target, payload })
    });
    setMissions([...missions, await res.json()]);
  };
  return (
    <div className="nano-os-control">
      <h2>نظام النانو التشغيلي - Nano-OS</h2>
      <input placeholder="الهدف..." />
      <input placeholder="الحمولة الجزيئية..." />
      <button onClick={() => deployNano('tumor', 'doxorubicin')}>نشر النانو</button>
      {missions.map(m => (
        <div key={m.id} className="nano-mission">
          <h3>{m.target}</h3>
          <progress value={m.progress} max="100" />
          <span>{m.status}</span>
        </div>
      ))}
    </div>
  );
};