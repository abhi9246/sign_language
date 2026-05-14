import { useState, useEffect } from 'react';
import axios from 'axios';

// Create an Axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'
});

// Setup interceptor to inject JWT token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getUser: () => api.get('/auth/user')
};

export const historyAPI = {
  getHistory: () => api.get('/history'),
  saveSentence: (sentence) => api.post('/history', { sentence }),
  deleteRecord: (id) => api.delete(`/history/${id}`)
};

export const aiAPI = {
  predict: (image) => api.post('/ai/predict', { image }),
  suggest: (word) => api.post('/ai/suggest', { word })
};
