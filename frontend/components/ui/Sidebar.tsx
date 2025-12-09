import React, { useState } from 'react';
import { GraduationCap, ChevronRight, Search } from 'lucide-react';
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
  const [searchQuery, setSearchQuery] = useState('');

  const filteredSubjects = subjects.filter(subject =>
    subject.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

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
      flexDirection: 'column' as const,
      gap: '16px',
    },
    logo: {
      fontSize: '28px',
      fontWeight: '800',
      color: currentColors.primary, // Fixed visibility: plain color
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
    },
    searchContainer: {
      position: 'relative' as const,
    },
    searchInput: {
      width: '100%',
      padding: '10px 12px 10px 36px',
      borderRadius: '8px',
      border: `1px solid ${currentColors.border}`,
      backgroundColor: currentColors.bgTertiary,
      color: currentColors.textPrimary,
      fontSize: '14px',
      outline: 'none',
    },
    searchIcon: {
      position: 'absolute' as const,
      left: '10px',
      top: '50%',
      transform: 'translateY(-50%)',
      color: currentColors.textSecondary,
    },
    subjectsList: {
      flex: 1,
      overflowY: 'auto' as const,
      padding: '16px',
      display: 'flex',
      flexDirection: 'column' as const,
      gap: '8px',
    },
    subjectButton: (subject: Subject, isSelected: boolean) => ({
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      padding: '14px 16px',
      borderRadius: '12px',
      cursor: 'pointer',
      transition: 'all 0.2s ease',
      backgroundColor: isSelected ? currentColors.primary + '15' : currentColors.bgTertiary, // Button-like bg
      border: isSelected ? `2px solid ${subject.color}` : '1px solid transparent',
      boxShadow: isSelected ? `0 0 10px ${subject.color}20` : 'none',
      color: currentColors.textPrimary,
    }),
  };

  return (
    <div style={styles.sidebar}>
      <div style={styles.sidebarHeader}>
        <div style={styles.logo}>
          <GraduationCap size={32} />
          LEWA
        </div>
        <div style={styles.searchContainer}>
          <Search size={16} style={styles.searchIcon} />
          <input
            type="text"
            placeholder="Search subjects..."
            style={styles.searchInput}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>
      <div style={styles.subjectsList}>
        <div style={{ marginBottom: '8px', fontSize: '12px', fontWeight: '600', color: currentColors.textSecondary, textTransform: 'uppercase', letterSpacing: '1px' }}>
          Menu
        </div>
        {filteredSubjects.map(subject => {
          const isSelected = selectedSubject?.id === subject.id;
          return (
            <div
              key={subject.id}
              style={styles.subjectButton(subject, isSelected)}
              onClick={() => onSubjectSelect(subject)}
              onMouseEnter={(e) => {
                if (!isSelected) e.currentTarget.style.backgroundColor = currentColors.bgTertiary + '99';
                e.currentTarget.style.transform = 'translateY(-2px)';
              }}
              onMouseLeave={(e) => {
                if (!isSelected) e.currentTarget.style.backgroundColor = currentColors.bgTertiary;
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              <span style={{ fontSize: '24px' }}>{subject.icon}</span>
              <span style={{ flex: 1, fontWeight: '600' }}>{subject.name}</span>
              {isSelected && <ChevronRight size={20} color={subject.color} />}
            </div>
          );
        })}
      </div>
    </div>
  );
};