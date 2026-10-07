import React, { useState } from 'react';
import { Calendar, Clock } from '../icons';

export const AppointmentScheduler = () => {
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [doctor, setDoctor] = useState('');
  const book = async () => {
    await fetch('/api/patient/appointment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, doctor })
    });
    alert('تم حجز الموعد!');
  };
  return (
    <div className="appointment-scheduler">
      <h3>حجز موعد طبي</h3>
      <Calendar />
      <input type="date" value={date} onChange={e => setDate(e.target.value)} />
      <Clock />
      <input type="time" value={time} onChange={e => setTime(e.target.value)} />
      <select value={doctor} onChange={e => setDoctor(e.target.value)}>
        <option value="">اختر الطبيب</option>
        <option value="d1">د. أحمد - القلب</option>
        <option value="d2">د. فاطمة - السكري</option>
      </select>
      <button onClick={book}>حجز الموعد</button>
    </div>
  );
};
