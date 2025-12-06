import React, { useRef, useEffect, useState } from 'react';
import { Send } from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { Message, Subject } from '../../../types';

interface ChatWindowProps {
  messages: Message[];
  selectedSubject: Subject;
  onSendMessage: (content: string) => void;
  currentColors: any;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  selectedSubject,
  onSendMessage,
  currentColors,
}) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!inputValue.trim()) return;
    onSendMessage(inputValue);
    setInputValue('');
  };

  const styles = {
    container: {
      width: '100%',
      height: '100%',
      display: 'flex',
      flexDirection: 'column' as const,
    },
    chatContainer: {
      flex: 1,
      padding: '24px',
      overflowY: 'auto' as const,
    },
    inputArea: {
      padding: '24px',
      backgroundColor: currentColors.bgSecondary,
      borderTop: `1px solid ${currentColors.border}`,
      display: 'flex',
      gap: '12px',
      alignItems: 'center',
    },
    input: {
      flex: 1,
      padding: '16px 20px',
      borderRadius: '12px',
      border: `1px solid ${currentColors.border}`,
      backgroundColor: currentColors.bg,
      color: currentColors.text,
      fontSize: '15px',
      outline: 'none',
    },
    sendButton: {
      padding: '16px 24px',
      borderRadius: '12px',
      border: 'none',
      backgroundColor: currentColors.primary,
      color: '#ffffff',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontWeight: '600',
      transition: 'all 0.2s ease',
    },
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatContainer}>
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} currentColors={currentColors} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div style={styles.inputArea}>
        <input
          style={styles.input}
          placeholder={`Ask anything about ${selectedSubject.name}...`}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button style={styles.sendButton} onClick={handleSend}>
          <Send size={20} />
          Send
        </button>
      </div>
    </div>
  );
};