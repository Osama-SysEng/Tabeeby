import React from 'react';
import { AlertTriangle, Phone } from '../icons';

interface EmergencyButtonProps { patientId: string; onEmergency: () => void; }

export const EmergencyButton: React.FC<EmergencyButtonProps> = ({ patientId, onEmergency }) => {
  const triggerEmergency = async () => {
    // 7-step autonomous emergency protocol fires simultaneously
    await fetch('/api/patient/emergency-trigger', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ patientId })
    });
    onEmergency();
  };

  return (
    <button className="emergency-button" onClick={triggerEmergency}>
      <AlertTriangle />
      <span>الطوارئ - اتصل الآن</span>
      <Phone />
    </button>
  );
};