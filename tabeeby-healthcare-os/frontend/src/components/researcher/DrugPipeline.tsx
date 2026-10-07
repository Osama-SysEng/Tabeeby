import React from 'react';
import { Molecule } from '../icons';

const stages = [
  { id: '1', name: 'تحديد نمط المرض', status: 'completed', compounds: 0 },
  { id: '2', name: 'تحديد الهدف الجزيئي', status: 'completed', compounds: 0 },
  { id: '3', name: 'تنبؤ الثبات', status: 'active', compounds: 1250 },
  { id: '4', name: 'إنشاء مركب جديد', status: 'active', compounds: 0 },
  { id: '5', name: 'إعادة استخدام الأدوية', status: 'pending', compounds: 0 },
  { id: '6', name: 'تنبؤ ADMET', status: 'pending', compounds: 0 },
  { id: '7', name: 'محاكاة التجارب السريرية', status: 'pending', compounds: 0 },
  { id: '8', name: 'مسار التخليق', status: 'pending', compounds: 0 },
  { id: '9', name: 'طريقة علاج جديدة', status: 'pending', compounds: 0 },
  { id: '10', name: 'الجاهزية التصنيعية', status: 'pending', compounds: 0 },
];

export const DrugPipeline = () => (
  <div className="drug-pipeline">
    <h3>مسار اكتشاف الأدوية - Ultra IQ (10 مراحل)</h3>
    {stages.map(s => (
      <div key={s.id} className={`stage ${s.status}`}>
        <span>{s.name}</span>
        {s.compounds > 0 && <small>{s.compounds} مركب</small>}
      </div>
    ))}
  </div>
);
