import React, { useState, useEffect } from 'react';

interface RobotStatus { robotId: string; name: string; connected: boolean; battery: number; position: { x: number; y: number; z: number }; }
export const RoboticSurgeryControl: React.FC<{ robotId: string }> = ({ robotId }) => {
  const [robot, setRobot] = useState<RobotStatus | null>(null);
  useEffect(() => {
    fetch(`/api/robotic-surgery/${robotId}/status`).then(r => r.json()).then(setRobot);
  }, [robotId]);
  const sendCommand = async (command: string) => {
    await fetch(`/api/robotic-surgery/${robotId}/command`, {
      method: 'POST',
      body: JSON.stringify({ command })
    });
  };
  return (
    <div className="robotic-surgery-control">
      <h2>التحكم بالروبوت الجراحي</h2>
      {robot && (
        <div>
          <h3>{robot.name}</h3>
          <p>متصل: {robot.connected ? 'نعم' : 'لا'}</p>
          <p>البطارية: {robot.battery}%</p>
          <p>الموضع: X={robot.position.x}, Y={robot.position.y}, Z={robot.position.z}</p>
          <div className="robot-controls">
            <button onClick={() => sendCommand('move_up')}>أعلى</button>
            <button onClick={() => sendCommand('move_down')}>أسفل</button>
            <button onClick={() => sendCommand('move_left')}>يسار</button>
            <button onClick={() => sendCommand('move_right')}>يمين</button>
            <button onClick={() => sendCommand('emergency_stop')}>إيقاف طارئ</button>
          </div>
        </div>
      )}
    </div>
  );
};