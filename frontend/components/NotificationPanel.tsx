'use client'

import { useState } from 'react'

interface Notification {
  type: string
  title: string
  message: string
  timestamp: string
}

export default function NotificationPanel({ notifications }: { notifications: Notification[] }) {
  const [isOpen, setIsOpen] = useState(false)

  if (notifications.length === 0) return null

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 right-4 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 z-50"
      >
        Notifications ({notifications.length})
      </button>

      {isOpen && (
        <div className="fixed top-16 right-4 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 max-h-96 overflow-y-auto">
          <div className="p-4 border-b border-gray-200">
            <h3 className="font-semibold">Notifications</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {notifications.map((notif, idx) => (
              <div key={idx} className="p-4 hover:bg-gray-50">
                <div className="font-medium text-sm">{notif.title}</div>
                <div className="text-xs text-gray-600 mt-1">{notif.message}</div>
                <div className="text-xs text-gray-400 mt-2">
                  {new Date(notif.timestamp).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

