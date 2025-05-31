import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api';

export const getWeather = async (city) => {
  const response = await axios.get(`${BASE_URL}/weather`, {
    params: { city }
  });
  return response.data;
};

export const getStats = async () => {
  const response = await axios.get(`${BASE_URL}/stats`);
  return response.data;
};

export const getCities = async (query) => {
  const response = await axios.get(`${BASE_URL}/cities`, {
    params: { query }
  });
  return response.data;
};
