export interface Subject {
  id: string;
  name: string;
  icon: string;
  color: string;
}

export interface Message {
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
}

export type Mode = 'OL' | 'AL' | null;
