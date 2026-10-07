import React, { useState, useEffect } from 'react';

interface Message { id: string; text: string; sender: 'user' | 'ai'; timestamp: Date; }
interface AIPhysicianProps { patientId: string; }

export const AIPhysician: React.FC<AIPhysicianProps> = ({ patientId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    setMessages([{ id: '1', text: 'مرحباً بك! أنا طبيبك الافتراضي AI. كيف حالك اليوم؟', sender: 'ai', timestamp: new Date() }]);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { id: Date.now().toString(), text: input, sender: 'user' as const, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    const res = await fetch(`/api/patient/ai-chat/${patientId}`, {
      method: 'POST',
      body: JSON.stringify({ message: input })
    });
    const data = await res.json();
    const aiMsg = { id: (Date.now()+1).toString(), text: data.response, sender: 'ai' as const, timestamp: new Date() };
    setMessages(prev => [...prev, aiMsg]);
  };

  return (
    <div className="ai-physician">
      <div className="chat-header">
        <h3>طبيبك الافتراضي 🤖</h3>
        <span className={isOnline ? 'online' : 'offline'}>{isOnline ? 'متصل' : 'غير متصل'}</span>
      </div>
      <div className="chat-window">
        {messages.map(m => (
          <div key={m.id} className={`message ${m.sender}`}>
            <p>{m.text}</p>
            <small>{m.timestamp.toLocaleTimeString()}</small>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendMessage()} placeholder="اكتب رسالتك..." />
        <button onClick={sendMessage}>إرسال</button>
      </div>
    </div>
  );
};"