'use client';

import React, { useState } from 'react';
import { colors } from '../lib/colors';
import { useTheme } from '../hooks/useTheme';
import { useChat } from '../hooks/useChat';
import { Sidebar } from '../components/ui/Sidebar';
import { Header } from '../components/ui/Header';
import { WelcomeCard } from '../components/ui/WelcomeCard';
import { ModeSelector } from '../components/ui/ModeSelector';
import { ChatWindow } from '../components/ui/ChatWindow';
import { ToolsPanel } from '../components/ui/ToolsPanel';

const LEWAApp = () => {
  const { theme, toggleTheme } = useTheme();
  const {
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
  } = useChat();

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showTools, setShowTools] = useState(false);

  const currentColors = colors[theme as 'light' | 'dark'];

  const styles = {
    container: {
      display: 'flex',
      height: '100vh',
      backgroundColor: currentColors.bg,
      color: currentColors.text,
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      overflow: 'hidden',
    },
    mainContent: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column' as const,
      position: 'relative' as const,
    },
    contentArea: {
      flex: 1,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px',
      overflowY: 'auto' as const,
    },
  };

  return (
    <div style={styles.container}>
      <Sidebar
        isOpen={sidebarOpen}
        selectedSubject={selectedSubject}
        onSubjectSelect={handleSubjectSelect}
        theme={theme}
        currentColors={currentColors}
      />

      <div style={styles.mainContent}>
        <Header
          selectedSubject={selectedSubject}
          selectedMode={selectedMode}
          theme={theme}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          onToggleTheme={toggleTheme}
          currentColors={currentColors}
        />

        <div style={styles.contentArea}>
          {!selectedSubject ? (
            <WelcomeCard currentColors={currentColors} />
          ) : !chatStarted ? (
            <ModeSelector
              subject={selectedSubject}
              selectedMode={selectedMode}
              onModeSelect={handleModeSelect}
              onStartChat={handleStartChat}
              currentColors={currentColors}
            />
          ) : (
            <ChatWindow
              messages={messages}
              selectedSubject={selectedSubject}
              onSendMessage={sendMessage}
              currentColors={currentColors}
              isLoading={isLoading}
              onToggleTools={() => setShowTools(!showTools)}
              activeTool={activeTool}
              setActiveTool={setActiveTool}
            />
          )}
        </div>

        <ToolsPanel
          isOpen={showTools}
          onClose={() => setShowTools(false)}
          currentColors={currentColors}
        />
      </div>
    </div>
  );
};

export default LEWAApp;
