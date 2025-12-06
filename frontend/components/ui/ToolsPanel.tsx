import React from 'react';
import { X, Search, BarChart3, Bell } from 'lucide-react';
import { tools } from '../../lib/subjects';

interface ToolsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  currentColors: any;
}

export const ToolsPanel: React.FC<ToolsPanelProps> = ({ isOpen, onClose, currentColors }) => {
  const getToolIcon = (toolId: string) => {
    switch (toolId) {
      case 'researcher': return Search;
      case 'analytics': return BarChart3;
      case 'messenger': return Bell;
      default: return Search;
    }
  };

  const styles = {
    toolsPanel: {
      position: 'absolute' as const,
      right: isOpen ? '0' : '-320px',
      top: '0',
      bottom: '0',
      width: '320px',
      backgroundColor: currentColors.bgSecondary,
      borderLeft: `1px solid ${currentColors.border}`,
      padding: '24px',
      transition: 'right 0.3s ease',
      overflowY: 'auto' as const,
      zIndex: 10,
    },
    iconButton: {
      padding: '8px',
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
    toolCard: {
      padding: '20px',
      borderRadius: '16px',
      backgroundColor: currentColors.bg,
      marginBottom: '16px',
      cursor: 'pointer',
      transition: 'all 0.2s ease',
      border: `1px solid ${currentColors.border}`,
    },
  };

  return (
    <div style={styles.toolsPanel}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h3 style={{ fontSize: '20px', fontWeight: '700' }}>AI Tools</h3>
        <button style={styles.iconButton} onClick={onClose}>
          <X size={20} />
        </button>
      </div>
      {tools.map(tool => {
        const Icon = getToolIcon(tool.id);
        return (
          <div
            key={tool.id}
            style={styles.toolCard}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = `0 8px 24px ${currentColors.shadow}`;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
              <div style={{ padding: '8px', borderRadius: '8px', backgroundColor: currentColors.bgTertiary }}>
                <Icon size={20} color={currentColors.primary} />
              </div>
              <h4 style={{ fontSize: '16px', fontWeight: '600' }}>{tool.name}</h4>
            </div>
            <p style={{ fontSize: '14px', color: currentColors.textSecondary }}>{tool.description}</p>
          </div>
        );
      })}
    </div>
  );
};