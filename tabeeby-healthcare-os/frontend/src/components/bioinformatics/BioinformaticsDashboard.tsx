import React from 'react';
import { BioRobotProgramming } from './BioRobotProgramming';
import { NanoOSControl } from './NanoOSControl';
import { MolecularSimulation } from './MolecularSimulation';
import { VRSurgicalImmersion } from './VRSurgicalImmersion';

export const BioinformaticsDashboard = () => (
  <div className="bioinfo-dashboard">
    <h1>لوحة أخصائي المعلومات الحيوية</h1>
    <BioRobotProgramming />
    <NanoOSControl />
    <MolecularSimulation />
    <VRSurgicalImmersion />
  </div>
);
