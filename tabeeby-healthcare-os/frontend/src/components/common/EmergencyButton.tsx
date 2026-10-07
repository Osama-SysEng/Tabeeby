import React from 'react';
import { AlertTriangle, Phone } from '../icons';
export const EmergencyButton = () => {
  const trigger = async () => { await fetch('/api/emergency/trigger', { method: 'POST' }); alert('تم تفعيل بروتوكول الطوارئ 7 خطوات التلقائي!'); };
  return <button className="emergency-button" onClick={trigger}><AlertTriangle /><Phone /><span>الطوارئ - اتصل الآن</span></button>;
};
