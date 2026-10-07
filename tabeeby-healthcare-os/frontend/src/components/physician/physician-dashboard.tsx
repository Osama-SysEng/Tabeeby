import React, { useState, useEffect } from 'react';
import { PatientCard } from './patient-card';
import { UltraIQAlert } from './ultra-iq-alert';
import { TreatmentRecommender } from './treatment-recommender';
import { DrugInteractionChecker } from './drug-interaction-checker';

interface PhysicianDashboardProps { physicianId: string; }

export const PhysicianDashboard: React.FC<PhysicianDashboardProps> = ({ physicianId }) => {
  const [patients, setPatients] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  
  useEffect(() => {
    // 50 concurrent patients - real-time dashboard
    fetch(`/api/physician/${physicianId}/patients`).then(r => r.json()).then(setPatients);
    fetch(`/api/physician/${physicianId}/alerts`).then(r => r.json()).then(setAlerts);
  }, [physicianId]);

  return (
    <div className="physician-dashboard">
      <h1>لوحة physician</h1>
      <div className="patient-grid">
        {patients.slice(0, 50).map(p => <PatientCard key={p.id} patient={p} />)}
      </div>
      <UltraIQAlert alerts={alerts} />
      <TreatmentRecommender physicianId={physicianId} />
      <DrugInteractionChecker />
    </div>
  );
};