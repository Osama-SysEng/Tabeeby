import React, { useState, useEffect } from 'react';
// Robotic surgery control animated
export const AnimatedRoboticControl = () => {
  const [position, setPosition] = useState({ x: 0, y: 0, z: 0 });
  const [battery, setBattery] = useState(85);
  const [isMoving, setIsMoving] = useState(false);

  const move = (axis: 'x' | 'y' | 'z', delta: number) => {
    setIsMoving(true);
    setPosition(prev => ({ ...prev, [axis]: prev[axis] + delta }));
    setTimeout(() => setIsMoving(false), 500);
  };

  return (
    <div className="animated-robotic-control">
      <h3>التحكم بالروبوت الجراحي - Sub-mm Precision</h3>
      <div className="robot-position-animated">
        <div className="position-display">
          <div className="position-axis"><span>X:</span> <span className="position-value-x">{position.x.toFixed(2)}</span> مم</div>
          <div className="position-axis"><span>Y:</span> <span className="position-value-y">{position.y.toFixed(2)}</span> مم</div>
          <div className="position-axis"><span>Z:</span> <span className="position-value-z">{position.z.toFixed(2)}</span> مم</div>
        </div>
        <canvas ref={React.useRef<HTMLCanvasElement>(null)} className="robot-path-canvas" />
      </div>
      <div className="robot-controls-animated">
        <div className="control-group">
          <button onClick={() => move('x', 0.1)} className="control-btn">⬆ للأعلى</button>
          <button onClick={() => move('x', -0.1)} className="control-btn">⬇ للأسفل</button>
        </div>
        <div className="control-group">
          <button onClick={() => move('y', 0.1)} className="control-btn">⬅ لليسار</button>
          <button onClick={() => move('y', -0.1)} className="control-btn">➡ لليمين</button>
        </div>
        <div className="control-group">
          <button onClick={() => move('z', 0.1)} className="control-btn">🔼 للأمام</button>
          <button onClick={() => move('z', -0.1)} className="control-btn">🔽 للخلف</button>
        </div>
      </div>
      <div className="battery-animated">
        <div className="battery-level">
          <div className="battery-fill" style={{ width: battery + '%' }} />
        </div>
        <span>البطارية: {battery}%</span>
      </div>
      <div className="emergency-stop-animated">
        <button className="emergency-stop-btn">⏹ إيقاف طارئ</button>
      </div>
    </div>
  );
};
