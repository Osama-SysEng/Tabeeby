import React, { useEffect, useRef, useState } from 'react';
// AI Doctor Chat with typing animation + message transitions
export const AnimatedAIPhysicianChat = () => {
  const [messages, setMessages] = React.useState<{ id: string; text: string; sender: 'user' | 'ai'; time: string }[]>([
    { id: '1', text: 'مرحباً! أنا طبيبك الافتراضي AI. كيف حالك؟', sender: 'ai', time: '10:00 ص' },
  ]);
  const [input, setInput] = React.useState('');
  const [isTyping, setIsTyping] = React.useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { id: Date.now().toString(), text: input, sender: 'user' as const, time: new Date().toLocaleTimeString() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);
    await new Promise(r => setTimeout(r, 1500));
    const aiResponses = [
      'شكراً لسؤالك! بناءً على أحدث الأبحاث، أوصي بمراجعة طبيب مختص.',
      'أشعر بال concern حول عرضك. إليك بعض المعلومات الطبية المفيدة.',
      'لقد قمت بتحليل عرضك ضد قاعدة بيانات 15000+ مستند طبي.',
    ];
    const aiMsg = { id: (Date.now()+1).toString(), text: aiResponses[Math.floor(Math.random() * aiResponses.length)], sender: 'ai', time: new Date().toLocaleTimeString() };
    setIsTyping(false);
    setMessages(prev => [...prev, aiMsg]);
  };

  return (
    <div className="animated-ai-chat">
      <div className="chat-header">
        <h3>طبيبك الافتراضي AI</h3>
        <span className="status-indicator">🟢 متصل</span>
      </div>
      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={m.id} className={`message ${m.sender} slide-in`}>
            {m.sender === 'ai' && <span className="ai-avatar">🤖</span>}
            <p className="message-text">{m.text}</p>
            <small className="message-time">{m.time}</small>
          </div>
        ))}
        {isTyping && (
          <div className="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-animated">
        <input value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="اكتب رسالتك للطبيب AI..." />
        <button onClick={sendMessage}>إرسال</button>
      </div>
    </div>
  );
};
