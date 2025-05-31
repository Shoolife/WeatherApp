import React from 'react';
import { useStats } from '../hooks/useStats';

export default function StatsList() {
  const { data, isLoading, error } = useStats();

  if (isLoading) return <p>Загрузка истории…</p>;
  if (error) return <p>Ошибка при загрузке истории: {error.message}</p>;
  if (!Array.isArray(data)) return <p>Нет данных</p>;

  return (
    <div className="mt-4">
      <h2 className="font-semibold mb-2">История запросов</h2>
      <ul className="text-sm text-gray-700 space-y-1">
        {data.map((item) => (
          <li key={item.city}>
            {item.city} — {item.count} раз
          </li>
        ))}
      </ul>
    </div>
  );
}
