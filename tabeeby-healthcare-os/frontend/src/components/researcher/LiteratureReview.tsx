import React, { useState } from 'react';

const papers = [
  { title: 'Novel Biomarkers for Alzheimer Detection', journal: 'Nature Medicine', year: 2025, relevance: 94 },
  { title: 'CAR-T Cell Therapy for Solid Tumors', journal: 'Science', year: 2025, relevance: 91 },
];

export const LiteratureReview = () => {
  const [query, setQuery] = useState('');
  return (
    <div className="literature-review">
      <h3>مراجعة الأدبيات - 15000+ مستند</h3>
      <input value={query} onChange={e => setQuery(e.target.value)} placeholder="البحث..." />
      {papers.map((p, i) => (
        <div key={i} className="paper-card">
          <p>{p.title} - {p.journal} ({p.year}) - صلة {p.relevance}%</p>
        </div>
      ))}
    </div>
  );
};
