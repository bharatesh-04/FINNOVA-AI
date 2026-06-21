'use client';

import apiClient from '@/lib/api-client';
import { FinancialHealth } from '@/types';

export const analyticsService = {
  getFinancialHealth: async (): Promise<FinancialHealth> => {
    const response = await apiClient.get('/analytics/financial-health');
    return response.data;
  },

  getForecasts: async (type?: 'expense' | 'income' | 'savings') => {
    const response = await apiClient.get('/analytics/forecasts', {
      params: { type },
    });
    return response.data;
  },

  getInsights: async () => {
    const response = await apiClient.get('/analytics/insights');
    return response.data;
  },

  getSpendingTrends: async (period: 'weekly' | 'monthly' | 'yearly' = 'monthly') => {
    const response = await apiClient.get('/analytics/spending-trends', {
      params: { period },
    });
    return response.data;
  },

  getSubscriptions: async () => {
    const response = await apiClient.get('/analytics/subscriptions');
    return response.data;
  },

  getFraudAlerts: async () => {
    const response = await apiClient.get('/analytics/fraud-alerts');
    return response.data;
  },

  generateReport: async (format: 'pdf' | 'csv' | 'json' = 'pdf') => {
    const response = await apiClient.get('/analytics/report', {
      params: { format },
      responseType: format === 'pdf' ? 'blob' : 'json',
    });
    return response.data;
  },
};
