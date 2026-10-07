import React from 'react';
import { VitalMonitor } from './VitalMonitor';
import { AIPhysician } from './AIPhysician';
import { EmergencyButton } from './EmergencyButton';
import { AppointmentScheduler } from './AppointmentScheduler';
import { MedicationTracker } from './MedicationTracker';
import { SymptomChecker } from './SymptomChecker';
import { HealthTips } from './HealthTips';
import { WeatherHealth } from './WeatherHealth';
import { EMIntegration } from './EMIntegration';

export const PatientDashboard = () => (
  <div className="patient-dashboard">
    <VitalMonitor />
    <AIPhysician patientId="patient-001" />
    <EmergencyButton />
    <AppointmentScheduler />
    <MedicationTracker />
    <SymptomChecker />
    <div className="row">
      <HealthTips />
      <WeatherHealth />
    </div>
    <EMIntegration />
  </div>
);
