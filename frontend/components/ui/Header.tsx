import React from 'react';
import { Menu, Moon, Sun, Sparkles } from 'lucide-react';
import { Subject, Mode } from '../../../types';

interface HeaderProps {
  selectedSubject: Subject | null;
  selectedMode: Mode;
  theme: string;
  onToggleSidebar: () => void;
  onToggleTheme: () => void;
  onToggleTools: () => void;
  currentColors: any;
}

export const Header: React.FC<HeaderProps> = ({
  selectedSubject,
  selectedMode,
  theme,
  onToggleSidebar,
  onToggleTheme,
  onToggleTools,
  currentColors,
}) => {
  const styles = {
    header: {
      padding: '16px 24px',
      backgroundColor: currentColors.bgSecondary,
      borderBottom: `1px solid ${currentColors.border}`,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    },
    headerLeft: {
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
    },
    headerRight: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
    },
    iconButton: {
      padding: '10px',
      borderRadius: '10px',
      border: 'none',
      backgroundColor: currentColors.bgTertiary,
      color: currentColors.text,
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'all 0.2s ease',
    },
  };

  return (
    <div style={styles.header}>
      <div style={styles.headerLeft}>
        <button style={styles.iconButton} onClick={onToggleSidebar}>
          <Menu size={20} />
        </button>
        {selectedSubject && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '24px' }}>{selectedSubject.icon}</span>
            <div>
              <div style={{ fontWeight: '600', fontSize: '16px' }}>{selectedSubject.name}</div>
              {selectedMode && <div style={{ fontSize: '12px', color: currentColors.textSecondary }}>{selectedMode} Level</div>}
            </div>
          </div>
        )}
      </div>
      <div style={styles.headerRight}>
        <button style={styles.iconButton} onClick={onToggleTools}>
          <Sparkles size={20} />
        </button>
        <button style={styles.iconButton} onClick={onToggleTheme}>
          {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
        </button>
      </div>
    </div>
  );
};