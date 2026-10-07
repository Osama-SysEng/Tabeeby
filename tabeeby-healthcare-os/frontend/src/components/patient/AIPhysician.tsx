import React, { useState, useEffect } from 'react';
import { Send, Mic } from '../icons';

interface Message { id: string; text: string; sender: 'user' | 'ai'; time: string; }

export const AIPhysician = ({ patientId }: { patientId: string }) => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', text: 'مرحباً! أنا طبيبك الافتراضي الذكي. كيف يمكنني مساعدتك؟', sender: 'ai', time: '10:00' },
  ]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { id: Date.now().toString(), text: input, sender: 'user' as const, time: new Date().toLocaleTimeString() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    const aiMsg = { id: (Date.now()+1).toString(), text: 'شكراً لسؤالك. لأفضل تشخيص، يرجى استشارة طبيب مختص.', sender: 'ai' as const, time: new Date().toLocaleTimeString() };
    setTimeout(() => setMessages(prev => [...prev, aiMsg]), 300);
  };

  return (
    <div className="ai-physician">
      <h3>طبيبك الافتراضي AI</h3>
      <div className="chat-messages">
        {messages.map(m => (
          <div key={m.id} className={`message ${m.sender}`}>
            <p>{m.text}</p>
            <small>{m.time}</small>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <button onClick={() => setIsListening(!isListening)}><Mic /></button>
        <input value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="اكتب سؤالك..." />
        <button onClick={sendMessage}><Send /></button>
      </div>
    </div>
  );
};
