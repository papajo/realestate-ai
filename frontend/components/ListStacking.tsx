'use client'

import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function ListStacking() {
  const [searching, setSearching] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [formData, setFormData] = useState({
    address: '',
    city: '',
    state: '',
    zip_code: '',
  })

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    setSearching(true)

    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/list-stacking/search`,
        formData,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )

      setResults(response.data)
      toast.success('Property search completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Search failed')
    } finally {
      setSearching(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">List Stacking Search</h2>
      
      <form onSubmit={handleSearch} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Address
            </label>
            <input
              type="text"
              required
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="123 Main St"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              City
            </label>
            <input
              type="text"
              required
              value={formData.city}
              onChange={(e) => setFormData({ ...formData, city: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="Los Angeles"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              State
            </label>
            <input
              type="text"
              required
              value={formData.state}
              onChange={(e) => setFormData({ ...formData, state: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="CA"
              maxLength={2}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              ZIP Code
            </label>
            <input
              type="text"
              required
              value={formData.zip_code}
              onChange={(e) => setFormData({ ...formData, zip_code: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="90001"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={searching}
          className="w-full px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
        >
          {searching ? 'Searching...' : 'Search Property'}
        </button>
      </form>

      {results && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold mb-2">Search Results</h3>
          <div className="space-y-2">
            <div>
              <span className="font-medium">Lead Score: </span>
              <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                results.lead_score > 0.7 ? 'bg-green-100 text-green-800' :
                results.lead_score > 0.4 ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {(results.lead_score * 100).toFixed(0)}%
              </span>
            </div>
            {results.lead_id && (
              <div>
                <span className="font-medium">Lead Created: </span>
                <span className="text-sm text-gray-600">ID #{results.lead_id}</span>
              </div>
            )}
            {results.distress_signals && (
              <div>
                <span className="font-medium">Distress Signals: </span>
                <ul className="list-disc list-inside text-sm text-gray-600 mt-1">
                  {Object.entries(results.distress_signals).map(([key, value]) => (
                    <li key={key}>
                      {key.replace(/_/g, ' ')}: {String(value)}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

