'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

interface CashBuyer {
  id: number
  name: string
  company_name: string
  city: string
  state: string
  total_purchases: number
  average_purchase_price: number
}

export default function CashBuyers() {
  const [buyers, setBuyers] = useState<CashBuyer[]>([])
  const [loading, setLoading] = useState(true)
  const [scraping, setScraping] = useState(false)

  useEffect(() => {
    fetchBuyers()
  }, [])

  const fetchBuyers = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/cash-buyers`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      setBuyers(response.data)
    } catch (error) {
      toast.error('Failed to fetch cash buyers')
    } finally {
      setLoading(false)
    }
  }

  const handleScrape = async () => {
    setScraping(true)
    try {
      const token = localStorage.getItem('access_token')
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/cash-buyers/scrape`,
        { location: 'Los Angeles, CA', limit: 100 },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      toast.success('Scraping started in background')
      setTimeout(fetchBuyers, 5000) // Refresh after 5 seconds
    } catch (error) {
      toast.error('Failed to start scraping')
    } finally {
      setScraping(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading cash buyers...</div>
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <h2 className="text-xl font-semibold">Cash Buyers</h2>
        <button
          onClick={handleScrape}
          disabled={scraping}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
        >
          {scraping ? 'Scraping...' : 'Scrape New Buyers'}
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Company</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Purchases</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avg Price</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {buyers.map((buyer) => (
              <tr key={buyer.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {buyer.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {buyer.company_name || 'N/A'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {buyer.city}, {buyer.state}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {buyer.total_purchases}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  ${buyer.average_purchase_price?.toLocaleString() || 'N/A'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {buyers.length === 0 && (
          <div className="text-center py-8 text-gray-500">No cash buyers found</div>
        )}
      </div>
    </div>
  )
}

