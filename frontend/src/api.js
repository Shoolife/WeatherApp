const API_URL = import.meta.env.VITE_API_URL;

export async function getWeather(city) {
  const res = await fetch(`${API_URL}/weather?city=${encodeURIComponent(city)}`);
  if (!res.ok) throw new Error('City not found');
  return res.json();
}

export async function getCities(query) {
  const res = await fetch(`${API_URL}/cities?q=${encodeURIComponent(query)}`);
  if (!res.ok) return [];
  return res.json();
}

export async function getStats() {
  const res = await fetch(`${API_URL}/stats`);
  if (!res.ok) throw new Error('Stats fetch error');
  return res.json();
}