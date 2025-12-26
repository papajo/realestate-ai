import { useState, useEffect, useRef } from 'react'
import { useAuth } from './useAuth'

interface Notification {
  type: string
  title: string
  message: string
  timestamp: string
  data?: any
}

export function useWebSocket() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const wsRef = useRef<WebSocket | null>(null)
  const { user } = useAuth()

  useEffect(() => {
    if (!user) return

    const token = localStorage.getItem('access_token')
    if (!token) return

    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL}/ws?token=${token}`)

    ws.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type) {
          setNotifications((prev) => [data, ...prev].slice(0, 50)) // Keep last 50
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
    }

    wsRef.current = ws

    return () => {
      ws.close()
    }
  }, [user])

  return { notifications }
}

