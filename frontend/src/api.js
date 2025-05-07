import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const predictNextSession = (data) => api.post('/predict', data);
export const spacedRepetition = (data) => api.post('/spaced', data);
export const generateQuiz = (topic) => api.post('/generate-quiz', { topic });
export const scheduleStudySession = (data) => api.post('/schedule-session', data);
