import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, StopMic } from '../icons';

interface AIPhysicianChatProps { patientId: string; messages: string[]; }

export const AIPhysicianChat: React.FC<AIPhysicianChatProps> = ({ patientId, messages }) => {
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => { scrollRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setInput('');
    // Send to backend - Ultra IQ generates response
    const res = await fetch('/api/patient/ai-query', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ patientId, message: userMsg })
    });
    const data = await res.json();
    // Messages updated via parent
  };

  return (
    <div className="ai-physician-chat">
      <div className="chat-header">
        <h3>طبيبك الافتراضي AI</h3>
        <p>متصل طوال الوقت - يتذكر كل شيء</p>
      </div>
      <div className="chat-messages" ref={scrollRef}>
        {messages.map((m, i) => <div key={i} className="message ai">{m}</div>)}
      </div>
      <div className="chat-input">
        <button onClick={() => setIsListening(!isListening)}>
          {isListening ? <StopMic /> : <Mic />}
        </button>
        <input value={input} onChange={e => setInput(e.target.value)} placeholder="اكتب استفسارك...' />
        <button onClick={sendMessage}><Send /></button>
      </div>
    </div>
  );
};