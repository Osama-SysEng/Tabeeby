import React, { useEffect, useState } from 'react';

interface LabResult { id: string; testName: string; value: string; unit: string; referenceRange: string; date: string; patientId: string; }
export const LabResultsViewer: React.FC<{ physicianId: string; patientId?: string }> = ({ physicianId, patientId }) => {
  const [results, setResults] = useState<LabResult[]>([]);
  useEffect(() => {
    const pid = patientId || '';
    fetch(`/api/physician/${physicianId}/lab-results?patientId=${pid}`).then(r => r.json()).then(setResults);
  }, [physicianId, patientId]);
  return (
    <div className="lab-results">
      <h2>نتائج المختبر</h2>
      <table>
        <thead><tr><th>الفحص</th><th>القيمة</th><th>الوحدة</th><th>النطاق</th><th>التاريخ</th></tr></thead>
        <tbody>{results.map(r => <tr key={r.id}><td>{r.testName}</td><td>{r.value}</td><td>{r.unit}</td><td>{r.referenceRange}</td><td>{r.date}</td></tr>)}</tbody>
      </table>
    </div>
  );
};