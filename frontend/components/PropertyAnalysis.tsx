'use client'

import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function PropertyAnalysis() {
  const [files, setFiles] = useState<File[]>([])
  const [analyzing, setAnalyzing] = useState(false)
  const [results, setResults] = useState<any>(null)

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

    setAnalyzing(true)
    try {
      const token = localStorage.getItem('access_token')
      const formData = new FormData()
      files.forEach((file) => {
        formData.append('images', file)
      })

      // Note: This would need a lead_id - for demo, using 1
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/property-analysis/analyze/1`,
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
    } catch (error) {
      toast.error('Failed to analyze images')
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Property Analysis</h2>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
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
        disabled={analyzing || files.length === 0}
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

