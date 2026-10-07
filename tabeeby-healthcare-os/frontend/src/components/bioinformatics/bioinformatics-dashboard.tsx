import React from 'react';
import { BioRobotProgramming } from './bio-robot-programming';
import { NanoOSControl } from './nano-os-control';
import { MolecularSimulation } from './molecular-simulation';
import { VRSurgicalImmersion } from './vr-surgical-immersion';

export const BioinformaticsDashboard: React.FC = () => {
  return (
    <div className="bioinformatics-dashboard">
      <h1>لوحة أخصائي المعلومات الحيوية</h1>
      <BioRobotProgramming />
      <NanoOSControl />
      <MolecularSimulation />
      <VRSurgicalImmersion />
    </div>
  );
};