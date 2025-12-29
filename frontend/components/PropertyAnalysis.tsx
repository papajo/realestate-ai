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
}

export default function PropertyAnalysis() {
  const [leads, setLeads] = useState<Lead[]>([])
  const [leadId, setLeadId] = useState<number | null>(null)
  const [files, setFiles] = useState<File[]>([])
  const [analyzing, setAnalyzing] = useState(false)
  const [results, setResults] = useState<any>(null)
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

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files))
    }
  }

  const handleAnalyze = async () => {
    if (files.length === 0) {
      toast.error('Please select at least one image')
      return
    }
    if (!leadId) {
      toast.error('Please select a lead')
      return
    }

    setAnalyzing(true)
    try {
      const token = localStorage.getItem('access_token')
      const formData = new FormData()
      files.forEach((file) => {
        formData.append('images', file)
      })

      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/property-analysis/analyze/${leadId}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        }
      )

      setResults(response.data)
      toast.success('Analysis complete!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to analyze images')
    } finally {
      setAnalyzing(false)
    }
  }

  if (loadingLeads) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Property Analysis</h2>
        <p className="text-gray-500">Loading leads...</p>
      </div>
    )
  }

  if (leads.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Property Analysis</h2>
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
      <h2 className="text-xl font-semibold mb-4">Property Analysis</h2>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Select Lead
        </label>
        <select
          value={leadId || ''}
          onChange={(e) => setLeadId(parseInt(e.target.value) || null)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-primary-500 focus:border-primary-500 mb-4"
        >
          <option value="">Select a lead...</option>
          {leads.map((lead) => (
            <option key={lead.id} value={lead.id}>
              {lead.property_address}, {lead.property_city}, {lead.property_state} (Score: {(lead.lead_score * 100).toFixed(0)}%)
            </option>
          ))}
        </select>
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Upload Property Images
        </label>
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
        />
      </div>

      <button
        onClick={handleAnalyze}
        disabled={analyzing || files.length === 0 || !leadId}
        className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
      >
        {analyzing ? 'Analyzing...' : 'Analyze Images'}
      </button>

      {results && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-4">Analysis Results</h3>
          <div className="space-y-4">
            <div>
              <p className="font-medium">Detected Issues:</p>
              <ul className="list-disc list-inside mt-2">
                {results.detected_issues?.map((issue: any, idx: number) => (
                  <li key={idx}>
                    {issue.category} (Confidence: {(issue.confidence * 100).toFixed(0)}%)
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="font-medium">
                Estimated Repair Cost: ${results.repair_cost_estimate?.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">
                Images Analyzed: {results.images_analyzed}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

