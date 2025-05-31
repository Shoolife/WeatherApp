import React from 'react';

export default function WeatherCard({ data }) {
  function formatTimestamp(timestamp) {
    if (!timestamp) return 'Нет данных';
    const isoString = timestamp.replace(' ', 'T'); 
    const date = new Date(isoString);
    return isNaN(date.getTime()) ? 'Неверная дата' : date.toLocaleString();
  }

  return (
    <div className="mt-4 bg-white shadow p-4 rounded">
      <h2 className="text-xl font-bold">{data.city}</h2>
      <p>Temperature: {data.temperature}°C</p>
      <p>Wind Speed: {data.wind_speed} m/s</p>
      <p>Timestamp: {formatTimestamp(data.timestamp)}</p>
    </div>
  );
}
