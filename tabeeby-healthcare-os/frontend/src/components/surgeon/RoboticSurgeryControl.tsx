import React, { useState } from 'react';

const commands = ['move_up', 'move_down', 'move_left', 'move_right', 'rotate_ccw', 'rotate_cw'];
const [commandList, setCommandList] = useState<string[]>([]);

const sendCommand = (cmd: string) => setCommandList(prev => [cmd, ...prev].slice(0, 10));

export const RoboticSurgeryControl = () => (
  <div className="robotic-control">
    <h3>التحكم بالروبوت الجراحي - Sub-mm Precision</h3>
    <div className="robot-status">
      <span>✅ متصل</span>
      <span>🔋 85%</span>
    </div>
    <div className="robot-controls">
      <button onClick={() => sendCommand('move_up')}>⬆</button>
      <button onClick={() => sendCommand('move_down')}>⬇</button>
      <button onClick={() => sendCommand('move_left')}>⬅</button>
      <button onClick={() => sendCommand('move_right')}>➡</button>
      <button onClick={() => sendCommand('rotate_ccw')}>⟲</button>
      <button onClick={() => sendCommand('rotate_cw')}>⟳</button>
    </div>
    <button className="emergency-stop" onClick={() => sendCommand('emergency_stop')}>⏹ إيقاف طارئ</button>
    <div className="command-history">
      <h4>سجل الأوامر:</h4>
      <ul>{commandList.map((c, i) => <li key={i}>{c}</li>)}</ul>
    </div>
  </div>
);
