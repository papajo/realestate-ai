'use client'

import { useState } from 'react'
import Editor from '@monaco-editor/react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function NoCodeBuilder() {
  const [description, setDescription] = useState('')
  const [generatedTool, setGeneratedTool] = useState<any>(null)
  const [generating, setGenerating] = useState(false)

  const handleGenerate = async () => {
    if (!description.trim()) {
      toast.error('Please enter a tool description')
      return
    }

    setGenerating(true)
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/tools/generate`,
        { description },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      setGeneratedTool(response.data)
      toast.success('Tool generated successfully!')
    } catch (error) {
      toast.error('Failed to generate tool')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">No-Code Tool Builder</h2>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Describe the tool you want to create
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g., Create a tool that generates property listing ads with AI"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          rows={4}
        />
      </div>

      <button
        onClick={handleGenerate}
        disabled={generating || !description.trim()}
        className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
      >
        {generating ? 'Generating...' : 'Generate Tool'}
      </button>

      {generatedTool && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-4">{generatedTool.name}</h3>
          <div className="border border-gray-300 rounded-md">
            <Editor
              height="400px"
              defaultLanguage="javascript"
              value={generatedTool.code}
              theme="vs-dark"
              options={{
                readOnly: true,
                minimap: { enabled: false },
              }}
            />
          </div>
          <div className="mt-4">
            <button className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
              Deploy Tool
            </button>
            <button className="ml-2 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700">
              Save as Template
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

