import React from 'react';

const tips = [
  'شرب 8 أكواب ماء يومياً يحسن الصحة',
  'المشي 30 دقيقة يومياً يقلل خطر القلب',
  'النوم 7-8 ساعات ضروري للشفاء',
  'الخضار والفواكه 5 حصص يومياً',
  'التمارين 150 دقيقة أسبوعياً تمد العمر',
];

export const HealthTips = () => (
  <div className="health-tips">
    <h3>نصائح صحية يومية</h3>
    {tips.map((tip, i) => (
      <p key={i}>💡 {tip}</p>
    ))}
  </div>
);
