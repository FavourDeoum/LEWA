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
      fontWeight: '900',
      marginBottom: '16px',
      color: currentColors.primary,
      letterSpacing: '2px',
      textShadow: `0 2px 8px ${currentColors.shadow}`,
    },
    welcomeText: {
      fontSize: '20px',
      color: currentColors.text,
      fontWeight: '600',
      marginBottom: '32px',
      textShadow: `0 1px 4px ${currentColors.shadow}`,
    },
    subText: {
      fontSize: '16px',
      color: currentColors.textSecondary,
    },
  };

  return (
    <div style={styles.welcomeCard}>
      <h1 style={styles.welcomeTitle}>Welcome to LEWA</h1>
      <p style={styles.welcomeText}>
        Your AI-powered tutor for GCE OL & AL success
      </p>
      <p style={styles.subText}>
        Select a subject from the sidebar to begin your learning journey
      </p>
    </div>
  );
};