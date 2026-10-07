import React from 'react';
import { VRSimulationSuite } from './VRSimulationSuite';
import { ARLiveAssistance } from './ARLiveAssistance';
import { MetaverseOR } from './MetaverseOR';
import { RoboticSurgeryControl } from './RoboticSurgeryControl';
import { PerformanceAnalytics } from './PerformanceAnalytics';

export const SurgeonDashboard = () => (
  <div className="surgeon-dashboard">
    <h1>لوحة الجراح - Tier 5 (مُcertified)</h1>
    <VRSimulationSuite />
    <ARLiveAssistance />
    <MetaverseOR />
    <RoboticSurgeryControl />
    <PerformanceAnalytics />
  </div>
);
