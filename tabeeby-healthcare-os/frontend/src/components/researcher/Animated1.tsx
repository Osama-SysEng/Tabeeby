import React, { useState, useEffect } from 'react';
// Pipeline drugs animated
export const AnimatedDrugPipeline = () => {
  const [stages] = useState([
    { id: '1', name: 'تحديد نمط المرض', status: 'completed', compounds: 0, progress: 100 },
    { id: '2', name: 'تحديد الهدف الجزيئي', status: 'completed', compounds: 0, progress: 100 },
    { id: '3', name: 'تنبؤ الثبات', status: 'active', compounds: 1250, progress: 60 },
    { id: '4', name: 'إنشاء مركب جديد', status: 'active', compounds: 0, progress: 30 },
    { id: '5', name: 'إعادة استخدام الأدوية', status: 'pending', compounds: 0, progress: 0 },
    { id: '6', name: 'تنبؤ ADMET', status: 'pending', compounds: 0, progress: 0 },
    { id: '7', name: 'محاكاة التجارب السريرية', status: 'pending', compounds: 0, progress: 0 },
    { id: '8', name: 'مسار التخليق', status: 'pending', compounds: 0, progress: 0 },
    { id: '9', name: 'طريقة علاج جديدة', status: 'pending', compounds: 0, progress: 0 },
    { id: '10', name: 'الجاهزية التصنيعية', status: 'pending', compounds: 0, progress: 0 },
  ]);

  return (
    <div className="animated-drug-pipeline">
      <h3>مسار اكتشاف الأدوية - Ultra IQ 300B Ops/sec</h3>
      <div className="pipeline-animated">
        {stages.map((s, i) => (
          <div key={s.id} className={`pipeline-stage-animated ${s.status}`} style={{ '--progress': s.progress + '%' }}>
            <div className="stage-number">{i + 1}</div>
            <div className="stage-content">
              <h4>{s.name}</h4>
              {s.compounds > 0 && <span>{s.compounds} مركب قيد التحليل</span>}
              <div className="stage-progress-bar"><div className="stage-fill" /></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
