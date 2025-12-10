import React, { useRef, useEffect, useState } from 'react';
import { Send, Sparkles } from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { Message, Subject } from '../../types';
import { tools } from '../../lib/subjects';

interface ChatWindowProps {
  messages: Message[];
  selectedSubject: Subject;
  onSendMessage: (content: string) => void;
  currentColors: any;
  isLoading: boolean;
  onToggleTools: () => void;
  activeTool: string | null;
  setActiveTool: (toolId: string | null) => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  selectedSubject,
  onSendMessage,
  currentColors,
  isLoading,
  onToggleTools,
  activeTool,
  setActiveTool,
}) => {
  const [inputValue, setInputValue] = useState('');
  const [showToolsMenu, setShowToolsMenu] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = () => {
    if (!inputValue.trim() || isLoading) return;
    onSendMessage(inputValue);
    setInputValue('');
  };

  const handleToggleTools = () => {
    setShowToolsMenu(!showToolsMenu);
  };

  const handleSelectTool = (toolId: string) => {
    setActiveTool(toolId);
    setShowToolsMenu(false);
  };

  const styles = {
    container: {
      width: '100%',
      height: '100%',
      display: 'flex',
      flexDirection: 'column' as const,
      position: 'relative' as const,
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
      position: 'relative' as const,
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
    actionButton: {
      padding: '16px',
      borderRadius: '12px',
      border: `1px solid ${activeTool ? currentColors.primary : currentColors.border}`,
      backgroundColor: activeTool ? currentColors.primary + '20' : currentColors.bgTertiary,
      color: activeTool ? currentColors.primary : currentColors.text,
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'all 0.2s ease',
    },
    sendButton: {
      padding: '16px 24px',
      borderRadius: '12px',
      border: 'none',
      backgroundColor: isLoading ? currentColors.bgTertiary : currentColors.primary,
      color: '#ffffff',
      cursor: isLoading ? 'not-allowed' : 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontWeight: '600',
      transition: 'all 0.2s ease',
    },
    loadingBubble: {
      display: 'flex',
      gap: '4px',
      padding: '16px 20px',
      backgroundColor: currentColors.bgSecondary,
      borderRadius: '12px 12px 12px 2px',
      width: 'fit-content',
      marginBottom: '16px',
    },
    loadingDot: {
      width: '8px',
      height: '8px',
      backgroundColor: currentColors.textSecondary,
      borderRadius: '50%',
      animation: 'bounce 1.4s infinite ease-in-out both',
    },
    toolsMenu: {
      position: 'absolute' as const,
      bottom: '100%',
      left: '24px',
      marginBottom: '12px',
      backgroundColor: currentColors.bgSecondary,
      border: `1px solid ${currentColors.border}`,
      borderRadius: '12px',
      padding: '8px',
      boxShadow: `0 4px 12px ${currentColors.shadow}`,
      display: 'flex',
      flexDirection: 'column' as const,
      width: '200px',
      zIndex: 100,
    },
    toolOption: {
      padding: '10px 12px',
      borderRadius: '8px',
      cursor: 'pointer',
      display: 'block', // Changed from flex to block to accommodate the internal divs
      color: currentColors.text,
      fontSize: '14px',
      transition: 'all 0.2s ease',
    },
    activeToolIndicator: {
      position: 'absolute' as const,
      top: '-40px',
      left: '24px',
      padding: '6px 12px',
      backgroundColor: currentColors.primary,
      color: '#fff',
      borderRadius: '20px',
      fontSize: '12px',
      fontWeight: '600',
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
      boxShadow: `0 2px 8px ${currentColors.shadow}`,
    }
  };

  return (
    <div style={styles.container}>
      <style>
        {`
          @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
          }
        `}
      </style>
      <div style={styles.chatContainer}>
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} currentColors={currentColors} />
        ))}
        {isLoading && (
          <div style={styles.loadingBubble}>
            <div style={{ ...styles.loadingDot, animationDelay: '-0.32s' }} />
            <div style={{ ...styles.loadingDot, animationDelay: '-0.16s' }} />
            <div style={styles.loadingDot} />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={styles.inputArea}>
        {showToolsMenu && (
          <div style={styles.toolsMenu}>
            {tools.map((tool) => (
              <div
                key={tool.id}
                style={{ ...styles.toolOption, backgroundColor: activeTool === tool.id ? currentColors.bgTertiary : 'transparent' }}
                onClick={() => handleSelectTool(tool.id)}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = currentColors.bgTertiary}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = activeTool === tool.id ? currentColors.bgTertiary : 'transparent'}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Sparkles size={16} />
                    <span style={{ fontWeight: '500' }}>{tool.name}</span>
                  </div>
                  <div style={{ fontSize: '11px', color: currentColors.textSecondary, marginLeft: '24px', marginTop: '2px' }}>
                    {tool.description}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTool && (
          <div style={styles.activeToolIndicator}>
            <Sparkles size={12} />
            {tools.find(t => t.id === activeTool)?.name || 'Tool'} Active
            <span style={{ cursor: 'pointer', marginLeft: '4px' }} onClick={() => setActiveTool(null)}>×</span>
          </div>
        )}

        <button
          style={styles.actionButton}
          onClick={handleToggleTools}
          title="Open Tools"
        >
          <Sparkles size={20} />
        </button>
        <input
          style={styles.input}
          placeholder={`Ask anything about ${selectedSubject.name}...`}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={isLoading}
        />
        <button style={styles.sendButton} onClick={handleSend} disabled={isLoading}>
          <Send size={20} />
          {isLoading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
};