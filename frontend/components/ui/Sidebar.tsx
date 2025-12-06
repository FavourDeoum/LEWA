import React from 'react';
import { GraduationCap, ChevronRight } from 'lucide-react';
import { subjects } from '../../lib/subjects';
import { Subject } from '../../../types';

interface SidebarProps {
  isOpen: boolean;
  selectedSubject: Subject | null;
  onSubjectSelect: (subject: Subject) => void;
  theme: string;
  currentColors: any;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  selectedSubject,
  onSubjectSelect,
  currentColors,
}) => {
  const styles = {
    sidebar: {
      width: isOpen ? '280px' : '0',
      backgroundColor: currentColors.bgSecondary,
      borderRight: `1px solid ${currentColors.border}`,
      display: 'flex',
      flexDirection: 'column' as const,
      transition: 'width 0.3s ease',
      overflow: 'hidden',
    },
    sidebarHeader: {
      padding: '24px 20px',
      borderBottom: `1px solid ${currentColors.border}`,
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
    },
    logo: {
      fontSize: '28px',
      fontWeight: '800',
      background: `linear-gradient(135deg, ${currentColors.primary}, ${currentColors.secondary})`,
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
    },
    subjectsList: {
      flex: 1,
      overflowY: 'auto' as const,
      padding: '12px',
    },
    subjectItem: (subject: Subject) => ({
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      padding: '14px 16px',
      margin: '4px 0',
      borderRadius: '12px',
      cursor: 'pointer',
      transition: 'all 0.2s ease',
      backgroundColor: selectedSubject?.id === subject.id ? currentColors.bgTertiary : 'transparent',
      border: selectedSubject?.id === subject.id ? `2px solid ${subject.color}` : '2px solid transparent',
    }),
  };

  return (
    <div style={styles.sidebar}>
      <div style={styles.sidebarHeader}>
        <div style={styles.logo}>
          <GraduationCap size={32} />
          LEWA
        </div>
      </div>
      <div style={styles.subjectsList}>
        <div style={{ padding: '8px 16px', fontSize: '12px', fontWeight: '600', color: currentColors.textSecondary, textTransform: 'uppercase', letterSpacing: '1px' }}>
          Subjects
        </div>
        {subjects.map(subject => (
          <div
            key={subject.id}
            style={styles.subjectItem(subject)}
            onClick={() => onSubjectSelect(subject)}
            onMouseEnter={(e) => e.currentTarget.style.backgroundColor = currentColors.bgTertiary}
            onMouseLeave={(e) => e.currentTarget.style.backgroundColor = selectedSubject?.id === subject.id ? currentColors.bgTertiary : 'transparent'}
          >
            <span style={{ fontSize: '24px' }}>{subject.icon}</span>
            <span style={{ flex: 1, fontWeight: '500' }}>{subject.name}</span>
            {selectedSubject?.id === subject.id && <ChevronRight size={20} color={subject.color} />}
          </div>
        ))}
      </div>
    </div>
  );
};