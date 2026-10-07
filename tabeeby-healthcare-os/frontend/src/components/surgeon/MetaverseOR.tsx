import React, { useState } from 'react';

export const MetaverseOR = () => {
  const [users] = useState([
    { name: 'د. أحمد - الجراح', specialty: 'القلب', location: 'القاهرة' },
    { name: 'د. سارة - التخدير', specialty: 'التخدير', location: 'الإسكندرية' },
  ]);
  const [isStarted, setIsStarted] = useState(false);
  return (
    <div className="metaverse-or">
      <h3>غرفة العمليات الميتافيرسية</h3>
      <h4>الإجراء: CABG - زراعة الشريان التاجي</h4>
      <p>المشاركون: {users.length} من 2 موقع</p>
      {users.map(u => (
        <div key={u.name} className="or-user">
          <span>{u.avatar}</span>
          <p>{u.name}</p>
          <p>{u.specialty} - {u.location}</p>
        </div>
      ))}
      <button onClick={() => setIsStarted(!isStarted)}>
        {isStarted ? 'قيد التشغيل' : 'ابدأ الغرفة'}
      </button>
    </div>
  );
};
