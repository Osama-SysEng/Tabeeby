import React from 'react';
import { DrugPipeline } from './DrugPipeline';
import { EpidemicMap } from './EpidemicMap';
import { PopulationGenetics } from './PopulationGenetics';
import { LiteratureReview } from './LiteratureReview';

export const ResearcherDashboard = () => (
  <div className="researcher-dashboard">
    <h1>لوحة الباحث - Ultra IQ 300B Ops</h1>
    <DrugPipeline />
    <EpidemicMap />
    <PopulationGenetics />
    <LiteratureReview />
  </div>
);
