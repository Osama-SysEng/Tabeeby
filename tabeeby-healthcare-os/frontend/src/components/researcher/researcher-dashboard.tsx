import React, { useState, useEffect } from 'react';
import { DrugPipeline } from './drug-pipeline';
import { EpidemicMap } from './epidemic-map';
import { PopulationGenetics } from './population-genetics';
import { LiteratureReview } from './literature-review';

export const ResearcherDashboard: React.FC = () => {
  return (
    <div className="researcher-dashboard">
      <h1>لوحة الباحث</h1>
      <DrugPipeline />
      <EpidemicMap />
      <PopulationGenetics />
      <LiteratureReview />
    </div>
  );
};