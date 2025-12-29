'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

interface Lead {
  id: number
  property_address: string
  property_city: string
  property_state: string
  lead_score: number
  status: string
  distress_signals: any
  owner_name?: string
  owner_email?: string
  owner_phone?: string
  property_zip?: string
}

export default function LeadPipeline() {
  const [leads, setLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null)
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [newLead, setNewLead] = useState({
    property_address: '',
    property_city: '',
    property_state: '',
    property_zip: '',
    owner_name: '',
    owner_email: '',
    owner_phone: '',
  })

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
    } catch (error) {
      toast.error('Failed to fetch leads')
    } finally {
      setLoading(false)
    }
  }

  const handleStatusChange = async (leadId: number, newStatus: string) => {
    try {
      const token = localStorage.getItem('access_token')
      await axios.patch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/leads/${leadId}`,
        { status: newStatus },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      toast.success('Lead updated')
      fetchLeads()
    } catch (error) {
      toast.error('Failed to update lead')
    }
  }

  const handleViewDetails = (lead: Lead) => {
    setSelectedLead(lead)
    setShowDetailModal(true)
  }

  const handleCreateLead = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('access_token')
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/leads`,
        newLead,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      toast.success('Lead created successfully!')
      setShowCreateForm(false)
      setNewLead({
        property_address: '',
        property_city: '',
        property_state: '',
        property_zip: '',
        owner_name: '',
        owner_email: '',
        owner_phone: '',
      })
      fetchLeads()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create lead')
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading leads...</div>
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <h2 className="text-xl font-semibold">Lead Pipeline</h2>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          {showCreateForm ? 'Cancel' : '+ Create Lead'}
        </button>
      </div>

      {showCreateForm && (
        <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <form onSubmit={handleCreateLead} className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Address</label>
              <input
                type="text"
                required
                value={newLead.property_address}
                onChange={(e) => setNewLead({ ...newLead, property_address: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">City</label>
              <input
                type="text"
                required
                value={newLead.property_city}
                onChange={(e) => setNewLead({ ...newLead, property_city: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">State</label>
              <input
                type="text"
                required
                maxLength={2}
                value={newLead.property_state}
                onChange={(e) => setNewLead({ ...newLead, property_state: e.target.value.toUpperCase() })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">ZIP</label>
              <input
                type="text"
                required
                value={newLead.property_zip}
                onChange={(e) => setNewLead({ ...newLead, property_zip: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Owner Name</label>
              <input
                type="text"
                value={newLead.owner_name}
                onChange={(e) => setNewLead({ ...newLead, owner_name: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Owner Email</label>
              <input
                type="email"
                value={newLead.owner_email}
                onChange={(e) => setNewLead({ ...newLead, owner_email: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
            <div className="col-span-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Owner Phone</label>
              <input
                type="tel"
                value={newLead.owner_phone}
                onChange={(e) => setNewLead({ ...newLead, owner_phone: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
            <div className="col-span-2">
              <button
                type="submit"
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
              >
                Create Lead
              </button>
            </div>
          </form>
        </div>
      )}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Address</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {leads.map((lead) => (
              <tr key={lead.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {lead.property_address}
                  </div>
                  <div className="text-sm text-gray-500">
                    {lead.property_city}, {lead.property_state}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    lead.lead_score > 0.7 ? 'bg-green-100 text-green-800' :
                    lead.lead_score > 0.4 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {(lead.lead_score * 100).toFixed(0)}%
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <select
                    value={lead.status}
                    onChange={(e) => handleStatusChange(lead.id, e.target.value)}
                    className="text-sm border-gray-300 rounded-md"
                  >
                    <option value="new">New</option>
                    <option value="qualified">Qualified</option>
                    <option value="contacted">Contacted</option>
                    <option value="converted">Converted</option>
                    <option value="lost">Lost</option>
                  </select>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <button 
                    onClick={() => handleViewDetails(lead)}
                    className="text-primary-600 hover:text-primary-900"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {leads.length === 0 && (
          <div className="text-center py-8 text-gray-500">No leads found</div>
        )}
      </div>

      {/* Lead Detail Modal */}
      {showDetailModal && selectedLead && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">Lead Details</h3>
                <button
                  onClick={() => setShowDetailModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <span className="text-2xl">&times;</span>
                </button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Property Information</h4>
                  <div className="space-y-2">
                    <p><span className="font-medium">Address:</span> {selectedLead.property_address}</p>
                    <p><span className="font-medium">City:</span> {selectedLead.property_city}</p>
                    <p><span className="font-medium">State:</span> {selectedLead.property_state}</p>
                    {selectedLead.property_zip && <p><span className="font-medium">ZIP:</span> {selectedLead.property_zip}</p>}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Lead Information</h4>
                  <div className="space-y-2">
                    <p><span className="font-medium">Score:</span> {(selectedLead.lead_score * 100).toFixed(1)}%</p>
                    <p><span className="font-medium">Status:</span> {selectedLead.status}</p>
                    {selectedLead.owner_name && <p><span className="font-medium">Owner:</span> {selectedLead.owner_name}</p>}
                    {selectedLead.owner_email && <p><span className="font-medium">Email:</span> {selectedLead.owner_email}</p>}
                    {selectedLead.owner_phone && <p><span className="font-medium">Phone:</span> {selectedLead.owner_phone}</p>}
                  </div>
                </div>
              </div>
              
              {selectedLead.distress_signals && (
                <div className="mt-4">
                  <h4 className="font-semibold text-gray-700 mb-2">Distress Signals</h4>
                  <div className="bg-gray-50 p-3 rounded">
                    <pre className="text-sm text-gray-600 whitespace-pre-wrap">
                      {JSON.stringify(selectedLead.distress_signals, null, 2)}
                    </pre>
                  </div>
                </div>
              )}
              
              <div className="flex justify-end mt-6">
                <button
                  onClick={() => setShowDetailModal(false)}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

