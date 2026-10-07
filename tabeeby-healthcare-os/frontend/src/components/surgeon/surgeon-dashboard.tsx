import React from 'react';
import { VRSimulationSuite } from './vr-simulation-suite';
import { ARLiveAssistance } from './ar-live-assistance';
import { MetaverseOR } from './metaverse-or';
import { RoboticSurgeryControl } from './robotic-surgery-control';
import { PerformanceAnalytics } from './performance-analytics';

export const SurgeonDashboard: React.FC = () => {
  return (
    <div className="surgeon-dashboard">
      <h1>لوحة الجراح (الدرجة 5)</h1>
      <VRSimulationSuite />
      <ARLiveAssistance />
      <MetaverseOR />
      <RoboticSurgeryControl />
      <PerformanceAnalytics />
    </div>
  );
};