// src/components/WeatherForm.jsx
import React, { useState, useEffect, useRef } from 'react'
import { useCities } from '../hooks/useCities'
import { useWeather } from '../hooks/useWeather'
import WeatherCard from './WeatherCard'
import WeatherChart from './WeatherChart'

export default function WeatherForm() {
  const [query, setQuery] = useState('')
  const [city, setCity] = useState('')
  const [showSuggestions, setShowSuggestions] = useState(false)
  const wrapperRef = useRef(null)

  const { options: cities, loading: citiesLoading } = useCities(query)

  const {
    data: weather,
    isFetching: weatherLoading,
    refetch,
    error: weatherError,
  } = useWeather(city, { enabled: false })

  useEffect(() => {
    function onClick(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowSuggestions(false)
      }
    }
    document.addEventListener('mousedown', onClick)
    return () => document.removeEventListener('mousedown', onClick)
  }, [])

  useEffect(() => {
    const last = localStorage.getItem('lastCity')
    if (last) {
      setQuery(last)
      setCity(last)
      refetch()
    }
  }, [refetch])

  const handleSearch = () => {
    const t = query.trim()
    if (!t) return
    setCity(t)
    localStorage.setItem('lastCity', t)
    refetch()
    setShowSuggestions(false)
  }

  const handleSelect = (name) => {
    setQuery(name)
    setCity(name)
    localStorage.setItem('lastCity', name)
    refetch()
    setShowSuggestions(false)
  }

  const onChange = (v) => {
    setQuery(v)
    setShowSuggestions(v.trim().length >= 3)
  }

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <div className="relative" ref={wrapperRef}>
        <div className="flex gap-2">
          <input
            type="text"
            className="border p-2 flex-1 rounded"
            value={query}
            onChange={e => onChange(e.target.value)}
            onFocus={() => query.trim().length >= 3 && setShowSuggestions(true)}
            placeholder="Введите город"
          />
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
            onClick={handleSearch}
            disabled={!query.trim()}
          >
            Поиск
          </button>
        </div>

        {showSuggestions && (
          <ul className="absolute top-full left-0 right-0 mt-1 bg-white border rounded shadow-md max-h-40 overflow-auto z-50">
            {citiesLoading && (
              <li className="px-4 py-2 text-gray-600">Загрузка подсказок…</li>
            )}
            {!citiesLoading && cities?.length === 0 && (
              <li className="px-4 py-2 text-gray-600">Ничего не найдено</li>
            )}
            {!citiesLoading &&
              cities?.map(c => (
                <li
                  key={c.name}
                  className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                  onMouseDown={() => handleSelect(c.name)} 
                >
                  {c.name}
                </li>
              ))}
          </ul>
        )}
      </div>

      {weatherLoading && <p className="mt-4">Загрузка погоды…</p>}

      {weatherError && (
        <p className="mt-4 text-red-600">
          {weatherError.message === 'City not found'
            ? 'Город не найден'
            : 'Ошибка сервера'}
        </p>
      )}

      {weather && (
        <div className="mt-6 space-y-6">
          <WeatherCard data={weather} />
          <WeatherChart data={weather.hourly.slice(0, 24)} />
        </div>
      )}
    </div>
)
}
