import React from 'react';
import { Subject, Mode } from '../../../types';

interface ModeSelectorProps {
  subject: Subject;
  selectedMode: Mode;
  onModeSelect: (mode: Mode) => void;
  onStartChat: () => void;
  currentColors: any;
}

export const ModeSelector: React.FC<ModeSelectorProps> = ({
  subject,
  selectedMode,
  onModeSelect,
  onStartChat,
  currentColors,
}) => {
  const styles = {
    welcomeCard: {
      maxWidth: '800px',
      width: '100%',
      backgroundColor: currentColors.bgSecondary,
      borderRadius: '24px',
      padding: '48px',
      boxShadow: `0 20px 60px ${currentColors.shadow}`,
      textAlign: 'center' as const,
    },
    modeSelector: {
      maxWidth: '600px',
      margin: '32px auto',
    },
    modeButtons: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '16px',
      marginBottom: '24px',
    },
    modeButton: (mode: string) => ({
      padding: '24px',
      borderRadius: '16px',
      border: `2px solid ${selectedMode === mode ? currentColors.primary : currentColors.border}`,
      backgroundColor: selectedMode === mode ? currentColors.primary : currentColors.bgTertiary,
      color: selectedMode === mode ? '#ffffff' : currentColors.text,
      cursor: 'pointer',
      transition: 'all 0.2s ease',
      fontSize: '18px',
      fontWeight: '600',
    }),
    startButton: {
      padding: '16px 48px',
      borderRadius: '12px',
      border: 'none',
      backgroundColor: selectedMode ? currentColors.primary : currentColors.border,
      color: '#ffffff',
      fontSize: '16px',
      fontWeight: '600',
      cursor: selectedMode ? 'pointer' : 'not-allowed',
      transition: 'all 0.2s ease',
      opacity: selectedMode ? 1 : 0.5,
    },
  };

  return (
    <div style={styles.welcomeCard}>
      <h2 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '16px', color: currentColors.text }}>
        {subject.icon} {subject.name}
      </h2>
      <p style={{ fontSize: '16px', color: currentColors.textSecondary, marginBottom: '32px' }}>
        Choose your level to get started
      </p>
      <div style={styles.modeSelector}>
        <div style={styles.modeButtons}>
          <button
            style={styles.modeButton('OL')}
            onClick={() => onModeSelect('OL')}
            onMouseEnter={(e) => {
              if (selectedMode !== 'OL') e.currentTarget.style.borderColor = currentColors.primary;
            }}
            onMouseLeave={(e) => {
              if (selectedMode !== 'OL') e.currentTarget.style.borderColor = currentColors.border;
            }}
          >
            📚 Ordinary Level
          </button>
          <button
            style={styles.modeButton('AL')}
            onClick={() => onModeSelect('AL')}
            onMouseEnter={(e) => {
              if (selectedMode !== 'AL') e.currentTarget.style.borderColor = currentColors.primary;
            }}
            onMouseLeave={(e) => {
              if (selectedMode !== 'AL') e.currentTarget.style.borderColor = currentColors.border;
            }}
          >
            🎓 Advanced Level
          </button>
        </div>
        <button
          style={styles.startButton}
          onClick={onStartChat}
          disabled={!selectedMode}
          onMouseEnter={(e) => {
            if (selectedMode) e.currentTarget.style.transform = 'scale(1.05)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
          }}
        >
          Start Learning
        </button>
      </div>
    </div>
  );
};