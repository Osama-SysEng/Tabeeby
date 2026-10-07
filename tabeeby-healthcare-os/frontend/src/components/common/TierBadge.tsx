import React from 'react';
const colors = ['#4CAF50', '#2196F3', '#9C27B0', '#FF9800', '#F44336'];
const labels = ['Patient - Tier 1', 'Physician - Tier 2', 'Researcher - Tier 3', 'Bioinformatics - Tier 4', 'Surgeon - Tier 5'];
export const TierBadge = ({ tier }: { tier: number }) => (
  <div className="tier-badge" style={{ backgroundColor: colors[tier - 1] }}>{labels[tier - 1]}</div>
);
