'use client'
import { useState } from 'react';
import { Message, Subject, Mode } from '../types/index';

export const useChat = () => {
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null);
  const [selectedMode, setSelectedMode] = useState<Mode>(null);
  const [chatStarted, setChatStarted] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);

  const [isLoading, setIsLoading] = useState(false);
  const [activeTool, setActiveTool] = useState<string | null>(null);

  const handleSubjectSelect = (subject: Subject) => {
    setSelectedSubject(subject);
    setSelectedMode(null);
    setChatStarted(false);
    setMessages([]);
    setActiveTool(null);
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

  const sendMessage = async (content: string) => {
    const userMessage: Message = {
      type: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    if (!selectedSubject || !selectedMode) return;

    setIsLoading(true);

    try {
      let finalQuestion = content;

      // Handle Researcher Tool
      if (activeTool === 'researcher') {
        const searchResponse = await fetch('http://127.0.0.1:8000/api/research', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: content, num_results: 3 }),
        });

        if (searchResponse.ok) {
          const searchData = await searchResponse.json();
          const snippets = searchData.results.map((r: any) => `- ${r.title}: ${r.snippet}`).join('\n');
          finalQuestion = `[CONTEXT FROM WEB SEARCH]:\n${snippets}\n\n[USER QUESTION]:\n${content}\n\nPlease use the above context to answer the user's question.`;
        } else {
          console.error("Research tool failed, proceeding without search results.");
        }
      }

      // Handle Messenger Tool (GCE Announcements)
      else if (activeTool === 'messenger') {
        const messengerResponse = await fetch('http://127.0.0.1:8000/api/messenger', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: content, num_results: 3 }),
        });

        if (messengerResponse.ok) {
          const messengerData = await messengerResponse.json();
          const snippets = messengerData.results.map((r: any) => `- [${r.date}] ${r.title}: ${r.snippet}`).join('\n');
          finalQuestion = `[CONTEXT FROM GCE ANNOUNCEMENTS]:\n${snippets}\n\n[USER QUESTION]:\n${content}\n\nPlease use the above announcements to answer the user's question about the GCE Board.`;
        } else {
          console.error("Messenger tool failed, proceeding without announcements.");
        }
      }

      // Call the subject endpoint
      const response = await fetch(`http://127.0.0.1:8000/api/${selectedSubject.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: finalQuestion, mode: selectedMode }),
      });

      if (!response.ok || !response.body) {
        throw new Error(`API Request failed with status ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      // Initialize empty bot message
      setMessages(prev => [...prev, {
        type: 'bot',
        content: '',
        timestamp: new Date(),
      }]);

      let botResponse = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        botResponse += chunk;

        // Update the last message (bot's message) with new content
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMessage = newMessages[newMessages.length - 1];
          if (lastMessage.type === 'bot') {
            lastMessage.content = botResponse;
          }
          return newMessages;
        });
      }

    } catch (error) {
      console.error('Error fetching AI response:', error);
      const errorMessage: Message = {
        type: 'bot',
        content: "I'm sorry, I encountered an error connecting to the tutor. Please check if the backend is running.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    selectedSubject,
    selectedMode,
    chatStarted,
    messages,
    isLoading,
    activeTool,
    setActiveTool,
    handleSubjectSelect,
    handleModeSelect,
    handleStartChat,
    sendMessage,
  };
};
