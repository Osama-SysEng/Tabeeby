import React, { useState } from 'react';

interface ORUser { id: string; name: string; specialty: string; location: string; avatar: string; }
export const MetaverseOR: React.FC = () => {
  const [users, setUsers] = useState<ORUser[]>([
    { id: '1', name: 'Dr. Smith', specialty: 'Cardiac Surgery', location: 'Boston', avatar: 'cardiac' },
    { id: '2', name: 'Dr. Chen', specialty: 'Neurosurgery', location: 'Tokyo', avatar: 'neuro' },
  ]);
  const [procedure, setProcedure] = useState('');
  const startMetaverseOR = () => { alert(`Metaverse OR starting: ${procedure}`); };
  return (
    <div className="metaverse-or">
      <h2>غرفة العمليات الميتافيرسية</h2>
      <h3>المشاركون الحاليون: {users.length}</h3>
      {users.map(u => (
        <div key={u.id} className="or-user">
          <span>{u.avatar}</span>
          <span>{u.name} - {u.specialty}</span>
          <span>{u.location}</span>
        </div>
      ))}
      <input value={procedure} onChange={e => setProcedure(e.target.value)} placeholder="اسم الإجراء..." />
      <button onClick={startMetaverseOR}>ابدأ غرفة العمليات</button>
    </div>
  );
};