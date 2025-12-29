'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

interface Message {
  role: string
  content: string
  timestamp: string
}

interface Lead {
  id: number
  property_address: string
  property_city: string
  property_state: string
  lead_score: number
}

export default function Chatbot() {
  const [leads, setLeads] = useState<Lead[]>([])
  const [leadId, setLeadId] = useState<number | null>(null)
  const [message, setMessage] = useState('')
  const [conversation, setConversation] = useState<any>(null)
  const [sending, setSending] = useState(false)
  const [loadingLeads, setLoadingLeads] = useState(true)

  useEffect(() => {
    fetchLeads()
  }, [])

  const fetchLeads = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/leads`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      setLeads(response.data)
      if (response.data.length > 0 && !leadId) {
        setLeadId(response.data[0].id)
      }
    } catch (error) {
      toast.error('Failed to load leads')
    } finally {
      setLoadingLeads(false)
    }
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim() || !leadId) {
      toast.error('Please enter a message and select a lead')
      return
    }

    setSending(true)
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/chatbot/conversation`,
        { lead_id: leadId, message },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )

      setConversation(response.data)
      setMessage('')
      toast.success('Message sent!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to send message')
    } finally {
      setSending(false)
    }
  }

  if (loadingLeads) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">AI Chatbot</h2>
        <p className="text-gray-500">Loading leads...</p>
      </div>
    )
  }

  if (leads.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">AI Chatbot</h2>
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <p className="text-yellow-800">
            No leads found. Please create a lead first using{' '}
            <strong>List Stacking</strong> or the <strong>Leads</strong> tab.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">AI Chatbot</h2>
      
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Select Lead
        </label>
        <select
          value={leadId || ''}
          onChange={(e) => setLeadId(parseInt(e.target.value) || null)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
        >
          <option value="">Select a lead...</option>
          {leads.map((lead) => (
            <option key={lead.id} value={lead.id}>
              {lead.property_address}, {lead.property_city}, {lead.property_state} (Score: {(lead.lead_score * 100).toFixed(0)}%)
            </option>
          ))}
        </select>
      </div>

      {conversation && (
        <div className="mb-4 p-4 bg-gray-50 rounded-lg max-h-96 overflow-y-auto">
          <div className="space-y-2">
            {conversation.messages?.map((msg: Message, idx: number) => (
              <div
                key={idx}
                className={`p-2 rounded ${
                  msg.role === 'user' ? 'bg-blue-100 ml-8' : 'bg-gray-100 mr-8'
                }`}
              >
                <div className="text-xs text-gray-500 mb-1">
                  {msg.role === 'user' ? 'You' : 'AI Assistant'}
                </div>
                <div>{msg.content}</div>
              </div>
            ))}
          </div>
          {conversation.qualification_status && (
            <div className="mt-4 p-2 bg-yellow-50 rounded">
              <span className="font-medium">Status: </span>
              {conversation.qualification_status} 
              {conversation.qualification_score && (
                <span className="ml-2">
                  (Score: {(conversation.qualification_score * 100).toFixed(0)}%)
                </span>
              )}
            </div>
          )}
        </div>
      )}

      <form onSubmit={handleSendMessage} className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          placeholder="Type your message..."
        />
        <button
          type="submit"
          disabled={sending || !message.trim() || !leadId}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
        >
          {sending ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  )
}

