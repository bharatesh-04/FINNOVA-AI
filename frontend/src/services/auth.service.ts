'use client';

import apiClient from '@/lib/api-client';
import { User } from '@/types';

export const authService = {
  register: async (email: string, password: string, name: string) => {
    const response = await apiClient.post('/auth/register', {
      email,
      password,
      name,
    });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login', {
      email,
      password,
    });
    const { access_token, user } = response.data;
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
    }
    return { token: access_token, user };
  },

  googleLogin: async (token: string) => {
    const response = await apiClient.post('/auth/google', { token });
    const { access_token, user } = response.data;
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
    }
    return { token: access_token, user };
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  logout: async () => {
    await apiClient.post('/auth/logout');
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },

  refreshToken: async () => {
    const response = await apiClient.post('/auth/refresh');
    const { access_token } = response.data;
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', access_token);
    }
    return access_token;
  },
};
