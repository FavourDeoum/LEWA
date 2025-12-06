import React from 'react';

interface WelcomeCardProps {
  currentColors: any;
}

export const WelcomeCard: React.FC<WelcomeCardProps> = ({ currentColors }) => {
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
    welcomeTitle: {
      fontSize: '48px',
      fontWeight: '800',
      marginBottom: '16px',
      background: `linear-gradient(135deg, ${currentColors.primary}, ${currentColors.secondary})`,
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    },
  };

  return (
    <div style={styles.welcomeCard}>
      <h1 style={styles.welcomeTitle}>Welcome to LEWA</h1>
      <p style={{ fontSize: '18px', color: currentColors.textSecondary, marginBottom: '32px' }}>
        Your AI-powered tutor for GCE OL & AL success
      </p>
      <p style={{ fontSize: '16px', color: currentColors.textSecondary }}>
        Select a subject from the sidebar to begin your learning journey
      </p>
    </div>
  );
};