'use client'

import { useEffect, useState } from 'react'

// Ticket types
interface Ticket {
  id: number
  title: string
  priority: 'LOW' | 'MED' | 'HIGH'
  status: 'BACKLOG' | 'DONE'
  created_at: string
  updated_at: string
}

const API_URL = 'http://127.0.0.1:8000/api/tickets'

export default function Home() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchTickets() {
      try {
        const response = await fetch(API_URL)
        if (!response.ok) {
          throw new Error('Failed to fetch tickets')
        }
        const data = await response.json()
        setTickets(data)
        setLoading(false)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setLoading(false)
      }
    }

    fetchTickets()
  }, [])

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'LOW':
        return 'text-green-700 bg-green-100 border-green-600'
      case 'MED':
        return 'text-yellow-700 bg-yellow-100 border-yellow-600'
      case 'HIGH':
        return 'text-red-700 bg-red-100 border-red-600'
      default:
        return 'text-gray-700 bg-gray-100 border-gray-300'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'BACKLOG':
        return 'text-blue-700 bg-blue-100 border-blue-600'
      case 'DONE':
        return 'text-green-700 bg-green-100 border-green-600'
      default:
        return 'text-gray-700 bg-gray-100 border-gray-300'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading tickets...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center p-8">
          <div className="bg-red-50 border-l-4 border-red-400 text-red-700 px-6 py-4 rounded-lg max-w-md">
            <h2 className="text-xl font-bold mb-2">Error</h2>
            <p className="text-sm">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-600 px-6 py-4 shadow-md">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-white">
            🎫 Dev-Ops Ticket Management
          </h1>
          <p className="text-blue-100 text-sm mt-1">
            API: {API_URL}
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white shadow-lg rounded-lg overflow-hidden">
          {/* Page Header */}
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-2xl font-semibold text-gray-900">
              All Tickets
            </h2>
            <p className="text-gray-600 text-sm mt-1">
              Showing {tickets.length} ticket{tickets.length !== 1 ? 's' : ''}
            </p>
          </div>

          {/* Ticket List */}
          <div className="p-6">
            {tickets.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-lg text-gray-500">No tickets found</p>
                <button
                  onClick={() => window.location.reload()}
                  className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded"
                >
                  Refresh
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {tickets.map((ticket) => (
                  <div
                    key={ticket.id}
                    className={`border rounded-lg p-5 hover:shadow-md transition-shadow ${getStatusColor(ticket.status).split(' ')[2]}`}
                  >
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-xl font-semibold text-gray-900 flex-1">
                        {ticket.title}
                      </h3>
                      <div className="flex space-x-2 flex-shrink-0">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold border-2 ${getPriorityColor(ticket.priority)}`}
                        >
                          {ticket.priority}
                        </span>
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold border-2 ${getStatusColor(ticket.status).split(' ')[2]}`}
                        >
                          {ticket.status}
                        </span>
                      </div>
                    </div>

                    <div className="text-sm text-gray-600 space-y-1">
                      <p><strong>ID:</strong> {ticket.id}</p>
                      <p><strong>Created:</strong> {new Date(ticket.created_at).toLocaleString()}</p>
                      <p><strong>Updated:</strong> {new Date(ticket.updated_at).toLocaleString()}</p>
                    </div>

                    <div className="mt-4 flex space-x-2">
                      <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-medium">
                        Edit
                      </button>
                      <button className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded font-medium">
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
