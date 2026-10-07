import React from 'react';
import { AlertTriangle, Phone } from '../icons';

export const EmergencyButton = () => {
  const triggerEmergency = async () => {
    await fetch('/api/emergency/trigger', { method: 'POST' });
    alert('تم تفعيل بروتوكول الطوارئ 7 خطوات!');
  };
  return (
    <button className="emergency-button" onClick={triggerEmergency}>
      <AlertTriangle /> <Phone />
      <span>الطوارئ - اتصل الآن</span>
    </button>
  );
};
