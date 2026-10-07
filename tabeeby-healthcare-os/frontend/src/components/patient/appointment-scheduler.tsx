import React, { useState } from 'react';
import { Calendar, Clock, User } from '../icons';

export const AppointmentScheduler: React.FC = () => {
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const bookAppointment = async () => {
    await fetch('/api/patient/appointment', { method: 'POST', body: JSON.stringify({ date, time }) });
  };
  return (
    <div className="appointment-scheduler">
      <Calendar /><input value={date} onChange={e => setDate(e.target.value)} />
      <Clock /><input value={time} onChange={e => setTime(e.target.value)} />
      <button onClick={bookAppointment}>حجز موعد</button>
    </div>
  );
};