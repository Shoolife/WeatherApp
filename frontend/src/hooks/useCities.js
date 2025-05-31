import { useState, useEffect } from 'react'
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.DEV ? '' : ''
})

export function useCities(query) {
  const [options, setOptions] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const q = query.trim()
    if (q.length < 2) {
      setOptions([])
      return
    }

    const controller = new AbortController()
    setLoading(true)

    api
      .get('/api/cities', {
        params: { q },
        signal: controller.signal
      })
      .then(res => {
        setOptions(res.data)
      })
      .catch(err => {
        if (err.name === 'CanceledError' || err.message === 'canceled') {
          return
        }
        if (axios.isAxiosError(err) && err.response?.status === 422) {
          setOptions([])
          return
        }
        console.error('Ошибка автодополнения:', err)
      })
      .finally(() => {
        setLoading(false)
      })

    return () => {
      controller.abort()
    }
  }, [query])

  return { options, loading }
}
