import React, { useEffect, useState } from 'react';

export const ImagingComparison: React.FC<{ patientId: string }> = ({ patientId }) => {
  const [images, setImages] = useState<any[]>([]);
  useEffect(() => {
    fetch(`/api/diagnostic/${patientId}/comparisons`).then(r => r.json()).then(setImages);
  }, [patientId]);
  return (
    <div className="imaging-comparison">
      <h2>مقارنة الصور الطبية</h2>
      {images.map(img => (
        <div key={img.id} className="image-compare">
          <img src={img.url} alt={img.modality} />
          <p>{img.modality} - {img.date} - {img.finding}</p>
        </div>
      ))}
    </div>
  );
};