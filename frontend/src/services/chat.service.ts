'use client';

import apiClient from '@/lib/api-client';
import { ChatMessage } from '@/types';

export const chatService = {
  sendMessage: async (content: string): Promise<ChatMessage> => {
    const response = await apiClient.post('/chat/message', { content });
    return response.data;
  },

  getHistory: async () => {
    const response = await apiClient.get('/chat/history');
    return response.data;
  },

  clearHistory: async () => {
    await apiClient.delete('/chat/history');
  },

  askQuestion: async (question: string) => {
    const response = await apiClient.post('/chat/ask', { question });
    return response.data;
  },
};
