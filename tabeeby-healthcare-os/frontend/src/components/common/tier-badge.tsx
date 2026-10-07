import React from 'react';

const tierColors = ['#4CAF50', '#2196F3', '#9C27B0', '#FF9800', '#F44336'];
const tierLabels = ['مريض', 'طبيب', 'باحث', 'أخصائي', 'جراح'];

export const TierBadge: React.FC<{ tier: number }> = ({ tier }) => {
  return (
    <div className="tier-badge" style={{ backgroundColor: tierColors[tier-1], color: 'white' }}>
      {tierLabels[tier-1]} - المستوى {tier}
    </div>
  );
};