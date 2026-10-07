import React, { useState, useEffect } from 'react';
import { DoctorPatientList } from './DoctorPatientList';
import { UltraIQAlerts } from './UltraIQAlerts';
import { TreatmentRecommender } from './TreatmentRecommender';
import { DrugInteractionChecker } from './DrugInteractionChecker';

export const DoctorDashboard = ({ physicianId }: { physicianId: string }) => {
  const [patients, setPatients] = useState<any[]>([]);
  useEffect(() => {
    fetch('/api/physician/' + physicianId + '/patients').then(r => r.json()).then(setPatients);
  }, [physicianId]);
  return (
    <div className="doctor-dashboard">
      <h1>لوحة الطبيب - Ultra IQ</h1>
      <DoctorPatientList patients={patients} />
      <UltraIQAlerts physicianId={physicianId} />
      <TreatmentRecommender />
      <DrugInteractionChecker />
    </div>
  );
};
