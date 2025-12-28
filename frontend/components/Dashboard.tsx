'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/hooks/useAuth'
import LeadPipeline from '@/components/LeadPipeline'
import PropertyAnalysis from '@/components/PropertyAnalysis'
import CashBuyers from '@/components/CashBuyers'
import NoCodeBuilder from '@/components/NoCodeBuilder'
import Metrics from '@/components/Metrics'
import NotificationPanel from '@/components/NotificationPanel'
import ListStacking from '@/components/ListStacking'
import Chatbot from '@/components/Chatbot'
import Settings from '@/components/Settings'
import { useWebSocket } from '@/hooks/useWebSocket'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const [activeTab, setActiveTab] = useState('dashboard')
  const { notifications } = useWebSocket()

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">AI Real Estate Investing</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">{user?.email}</span>
            <button
              onClick={logout}
              className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'dashboard', label: 'Dashboard' },
              { id: 'leads', label: 'Leads' },
              { id: 'list-stacking', label: 'List Stacking' },
              { id: 'chatbot', label: 'Chatbot' },
              { id: 'analysis', label: 'Property Analysis' },
              { id: 'buyers', label: 'Cash Buyers' },
              { id: 'tools', label: 'No-Code Builder' },
              { id: 'settings', label: 'Settings' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Notification Panel */}
        <NotificationPanel notifications={notifications} />

        {/* Content */}
        <div className="mt-6">
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <Metrics />
            </div>
          )}
          {activeTab === 'leads' && <LeadPipeline />}
          {activeTab === 'list-stacking' && <ListStacking />}
          {activeTab === 'chatbot' && <Chatbot />}
          {activeTab === 'analysis' && <PropertyAnalysis />}
          {activeTab === 'buyers' && <CashBuyers />}
          {activeTab === 'tools' && <NoCodeBuilder />}
          {activeTab === 'settings' && <Settings />}
        </div>
      </div>
    </div>
  )
}

