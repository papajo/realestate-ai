'use client'

import { useEffect, useState } from 'react'
import { Line, Bar, Doughnut } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import axios from 'axios'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

export default function Metrics() {
  const [leadData, setLeadData] = useState<any>(null)
  const [qualificationData, setQualificationData] = useState<any>(null)

  useEffect(() => {
    fetchMetrics()
  }, [])

  const fetchMetrics = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/leads`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )

      const leads = response.data
      
      // Lead pipeline chart
      const statusCounts = leads.reduce((acc: any, lead: any) => {
        acc[lead.status] = (acc[lead.status] || 0) + 1
        return acc
      }, {})

      setLeadData({
        labels: Object.keys(statusCounts),
        datasets: [
          {
            label: 'Leads by Status',
            data: Object.values(statusCounts),
            backgroundColor: [
              'rgba(59, 130, 246, 0.5)',
              'rgba(16, 185, 129, 0.5)',
              'rgba(245, 158, 11, 0.5)',
              'rgba(239, 68, 68, 0.5)',
            ],
          },
        ],
      })

      // Qualification rate
      const qualified = leads.filter((l: any) => l.status === 'qualified').length
      setQualificationData({
        labels: ['Qualified', 'Not Qualified'],
        datasets: [
          {
            data: [qualified, leads.length - qualified],
            backgroundColor: ['rgba(16, 185, 129, 0.5)', 'rgba(239, 68, 68, 0.5)'],
          },
        ],
      })
    } catch (error) {
      console.error('Error fetching metrics:', error)
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Lead Pipeline</h3>
        {leadData && <Doughnut data={leadData} />}
      </div>
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Qualification Rate</h3>
        {qualificationData && <Doughnut data={qualificationData} />}
      </div>
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">ROI Metrics</h3>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span>Total Leads</span>
            <span className="font-bold">0</span>
          </div>
          <div className="flex justify-between">
            <span>Conversion Rate</span>
            <span className="font-bold">0%</span>
          </div>
          <div className="flex justify-between">
            <span>Avg Deal Size</span>
            <span className="font-bold">$0</span>
          </div>
        </div>
      </div>
    </div>
  )
}

