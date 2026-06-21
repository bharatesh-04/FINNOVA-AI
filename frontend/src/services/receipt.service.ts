'use client';

import apiClient from '@/lib/api-client';
import { Receipt } from '@/types';

export const receiptService = {
  upload: async (file: File): Promise<Receipt> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/receipts/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getAll: async (limit?: number, offset?: number) => {
    const response = await apiClient.get('/receipts', {
      params: { limit, offset },
    });
    return response.data;
  },

  getById: async (id: string): Promise<Receipt> => {
    const response = await apiClient.get(`/receipts/${id}`);
    return response.data;
  },

  extractData: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/receipts/extract', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  createTransactionFromReceipt: async (receiptId: string) => {
    const response = await apiClient.post(`/receipts/${receiptId}/create-transaction`);
    return response.data;
  },

  delete: async (id: string) => {
    await apiClient.delete(`/receipts/${id}`);
  },
};
