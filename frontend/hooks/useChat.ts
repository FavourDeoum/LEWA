'use client'
import { useState } from 'react';
import { Message, Subject, Mode } from '../types/index';

export const useChat = () => {
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null);
  const [selectedMode, setSelectedMode] = useState<Mode>(null);
  const [chatStarted, setChatStarted] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSubjectSelect = (subject: Subject) => {
    setSelectedSubject(subject);
    setSelectedMode(null);
    setChatStarted(false);
    setMessages([]);
  };

  const handleModeSelect = (mode: Mode) => {
    setSelectedMode(mode);
  };

  const handleStartChat = () => {
    if (selectedMode && selectedSubject) {
      setChatStarted(true);
      setMessages([{
        type: 'bot',
        content: `Welcome to ${selectedSubject.name} ${selectedMode} tutoring! I'm here to help you excel. Ask me anything related to ${selectedSubject.name}.`,
        timestamp: new Date(),
      }]);
    }
  };

  const sendMessage = (content: string) => {
    const userMessage: Message = {
      type: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    // Simulate bot response (will be replaced with actual API call)
    setTimeout(() => {
      const botMessage: Message = {
        type: 'bot',
        content: `I understand your question about "${content}". This is a demo response for ${selectedSubject?.name} ${selectedMode}. The backend integration will provide actual AI-powered responses.`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMessage]);
    }, 1000);
  };

  return {
    selectedSubject,
    selectedMode,
    chatStarted,
    messages,
    handleSubjectSelect,
    handleModeSelect,
    handleStartChat,
    sendMessage,
  };
};
