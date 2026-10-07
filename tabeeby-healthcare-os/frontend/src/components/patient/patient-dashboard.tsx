import React, { useState, useEffect } from 'react';
import { VitalsPanel } from './vitals-panel';
import { AIPhysicianChat } from './ai-physician-chat';
import { EmergencyButton } from './emergency-button';
import { HealthTrends } from './health-trends';

interface PatientDashboardProps {
  patientId: string;
  userId: string;
}

export const PatientDashboard: React.FC<PatientDashboardProps> = ({ patientId, userId }) => {
  const [vitals, setVitals] = useState<any>(null);
  const [aiMessages, setAiMessages] = useState<string[]>([]);
  
  useEffect(() => {
    // IoT Biometric Integration - 1,440+ readings/day
    fetch(`/api/patient/${patientId}/vitals/realtime`)
      .then(r => r.json())
      .then(setVitals);
  }, [patientId]);

  return (
    <div className="patient-dashboard">
      <VitalsPanel vitals={vitals} />
      <AI滉ysicianChat patientId={patientId} messages={aiMessages} />
      <EmergencyButton patientId={patientId} onEmergency={() => {}} />
      <HealthTrends patientId={patientId} />
    </div>
  );
};