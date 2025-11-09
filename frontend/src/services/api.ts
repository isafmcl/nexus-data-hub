import axios from 'axios';

const apiUrl = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: apiUrl,
  timeout: 30_000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function get(path: string, params?: any) {
  const res = await api.get(path, { params });
  return res.data;
}

export async function post(path: string, data?: any) {
  const res = await api.post(path, data);
  return res.data;
}
