'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/hooks/useAuth'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function Settings() {
  const { user } = useAuth()
  const [profile, setProfile] = useState({
    full_name: '',
    email: '',
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (user) {
      setProfile({
        full_name: user.full_name || '',
        email: user.email || '',
      })
    }
  }, [user])

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const token = localStorage.getItem('access_token')
      await axios.patch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/me`,
        profile,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      toast.success('Profile updated successfully')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold">Settings</h2>
      </div>

      <div className="p-6 space-y-6">
        {/* Profile Settings */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Profile Settings</h3>
          <form onSubmit={handleUpdateProfile} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full Name
              </label>
              <input
                type="text"
                value={profile.full_name}
                onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={profile.email}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
            >
              {loading ? 'Updating...' : 'Update Profile'}
            </button>
          </form>
        </div>

        {/* Account Information */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Account Information</h3>
          <div className="bg-gray-50 p-4 rounded-md">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Account Type</p>
                <p className="font-medium">User</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Member Since</p>
                <p className="font-medium">N/A</p>
              </div>
            </div>
          </div>
        </div>

        {/* API Information */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">API Access</h3>
          <div className="bg-gray-50 p-4 rounded-md">
            <p className="text-sm text-gray-600 mb-2">
              Your API token for integrations:
            </p>
            <div className="flex items-center space-x-2">
              <code className="flex-1 px-3 py-2 bg-white border border-gray-300 rounded text-sm font-mono">
                {localStorage.getItem('access_token')?.substring(0, 50)}...
              </code>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(localStorage.getItem('access_token') || '')
                  toast.success('Token copied to clipboard')
                }}
                className="px-3 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 text-sm"
              >
                Copy
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}