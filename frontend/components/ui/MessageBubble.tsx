import React from 'react';
import { Message } from '../../../types';

interface MessageBubbleProps {
  message: Message;
  currentColors: any;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message, currentColors }) => {
  const styles = {
    message: {
      display: 'flex',
      justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
      marginBottom: '16px',
    },
    messageBubble: {
      maxWidth: '70%',
      padding: '16px 20px',
      borderRadius: '20px',
      backgroundColor: message.type === 'user' ? currentColors.primary : currentColors.bgSecondary,
      color: message.type === 'user' ? '#ffffff' : currentColors.text,
      boxShadow: `0 2px 8px ${currentColors.shadow}`,
    },
  };

  return (
    <div style={styles.message}>
      <div style={styles.messageBubble}>
        {message.content}
      </div>
    </div>
  );
};