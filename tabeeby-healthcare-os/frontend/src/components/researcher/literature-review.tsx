import React, { useState } from 'react';

interface Paper { id: string; title: string; authors: string; journal: string; year: number; relevance: number; doi: string; }
export const LiteratureReview: React.FC = () => {
  const [papers, setPapers] = useState<Paper[]>([]);
  const searchPapers = async (query: string) => {
    const res = await fetch('/api/researcher/literature', { method: 'POST', body: JSON.stringify({ query }) });
    setPapers(await res.json());
  };
  return (
    <div className="literature-review">
      <h2>مراجعة الأدبيات -索引 15,000+ مستند</h2>
      <input placeholder="البحث..." onKeyDown={e => { if(e.key==='Enter') searchPapers(e.target.value); }} />
      {papers.map(p => (
        <div key={p.id} className="paper-card">
          <h3>{p.title}</h3>
          <p>{p.authors} - {p.journal} ({p.year})</p>
          <p>الصلة: {p.relevance}%</p>
          <a href={`https://doi.org/${p.doi}`}>DOI</a>
        </div>
      ))}
    </div>
  );
};