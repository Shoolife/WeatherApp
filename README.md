# WeatherApp

**WeatherApp** — простое веб-приложение для просмотра текущей погоды и почасового прогноза в выбранном городе, а также автодополнение названий городов с помощью OpenStreetMap Nominatim.

---

## Реализовано

- 🔍 **Автодополнение городов**: ввод от 3 символов, запрос к FastAPI → Nominatim → фильтрация только городов (`city`, `town`, `village`, `hamlet`, `municipality`), обрезка до названия до первой запятой, исключение дублей.  
- 🌐 **Backend** на FastAPI:
  - Эндпоинты `/api/cities`, `/api/weather`, `/api/stats`
  - Использование `httpx.AsyncClient` для асинхронных запросов к внешним сервисам
  - Обработка ошибок и возврат корректных HTTP-статусов (422, 502)  
- ⚛️ **Frontend** на React + Vite + React Query:
  - Хук `useCities` для автодополнения
  - Хук `useWeather` для получения погоды
  - Компоненты `WeatherForm`, `WeatherCard`, `WeatherChart` (Recharts)
  - Перехват запросов `/api/*` на `http://localhost:8000` через Vite-прокси в режиме разработки  
- 🐳 **Docker Compose** для локального запуска сервисов:
  - `backend` (FastAPI + Uvicorn)
  - `frontend` (Vite dev server)  
- 📁 **.gitignore** настроен для игнорирования артефактов Python, Node, Docker и IDE.

---

## Технологии

- **Backend:** Python, FastAPI, Uvicorn, Pydantic, HTTPX, Docker  
- **Frontend:** JavaScript, React, Vite, Axios, React Query, Tailwind CSS, Recharts  
- **DevOps:** Docker, Docker Compose

---

## Запуск локально

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/yourusername/weatherapp.git
   cd weatherapp
   ```

2. Убедиться, что порты `8000` (backend) и `5173` (frontend) свободны.

3. Запустить Docker Compose:

   ```bash
   docker-compose up --build -d
   ```

4. Открыть браузер:

   - Frontend: http://localhost:5173
   - Backend Swagger: http://localhost:8000/docs

5. Остановить сервисы:

   ```bash
   docker-compose down
   ```

---

> **Примечание:** при разработке фронтенд запускается командой `npm run dev`, а бэкенд — через  
> `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.  
