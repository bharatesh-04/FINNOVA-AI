import apiClient from '@/lib/api-client';
import { Transaction } from '@/types';

export const transactionService = {
  getAll: async (filters?: {
    startDate?: string;
    endDate?: string;
    category?: string;
    type?: 'expense' | 'income';
    limit?: number;
    offset?: number;
  }) => {
    const response = await apiClient.get('/transactions', { params: filters });
    return response.data;
  },

  getById: async (id: string): Promise<Transaction> => {
    const response = await apiClient.get(`/transactions/${id}`);
    return response.data;
  },

  create: async (data: Partial<Transaction>): Promise<Transaction> => {
    const response = await apiClient.post('/transactions', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Transaction>): Promise<Transaction> => {
    const response = await apiClient.put(`/transactions/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await apiClient.delete(`/transactions/${id}`);
  },

  getStats: async (startDate?: string, endDate?: string) => {
    const response = await apiClient.get('/transactions/stats', {
      params: { startDate, endDate },
    });
    return response.data;
  },

  getCategoryBreakdown: async (startDate?: string, endDate?: string) => {
    const response = await apiClient.get('/transactions/category-breakdown', {
      params: { startDate, endDate },
    });
    return response.data;
  },

  getDashboardStats: async () => {
    const response = await apiClient.get('/transactions/dashboard-stats');
    return response.data;
  },
};
