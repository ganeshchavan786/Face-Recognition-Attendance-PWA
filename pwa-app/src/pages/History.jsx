import { useState, useEffect } from 'react'
import { Calendar, Clock, MapPin, CheckCircle, RefreshCw, Loader2 } from 'lucide-react'
import { attendanceDB } from '../services/db'
import { checkAndSync } from '../services/syncService'
import { format, parseISO } from 'date-fns'

export default function History() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [syncing, setSyncing] = useState(false)

  useEffect(() => {
    loadRecords()
  }, [])

  async function loadRecords() {
    setLoading(true)
    try {
      const allRecords = await attendanceDB.getAll()
      const sorted = allRecords.sort((a, b) => 
        new Date(b.created_at) - new Date(a.created_at)
      )
      setRecords(sorted)
    } catch (error) {
      console.error('Error loading records:', error)
    } finally {
      setLoading(false)
    }
  }

  async function handleSync() {
    if (!navigator.onLine) {
      alert('You are offline. Please connect to internet to sync.')
      return
    }

    setSyncing(true)
    try {
      const result = await checkAndSync()
      if (result) {
        alert(`Synced: ${result.synced}, Failed: ${result.failed}`)
        await loadRecords()
      }
    } catch (error) {
      alert('Sync failed. Please try again.')
    } finally {
      setSyncing(false)
    }
  }

  const pendingCount = records.filter(r => r.sync_status === 'PENDING').length

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
      </div>
    )
  }

  return (
    <div className="pb-20">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Attendance History</h2>
          <p className="text-sm text-gray-500">{records.length} records</p>
        </div>
        
        <button
          onClick={handleSync}
          disabled={syncing || pendingCount === 0}
          className="flex items-center gap-2 px-4 py-2 bg-primary-500 text-white rounded-lg text-sm disabled:opacity-50"
        >
          {syncing ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <RefreshCw className="w-4 h-4" />
          )}
          Sync ({pendingCount})
        </button>
      </div>

      {records.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <Calendar className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p>No attendance records yet</p>
        </div>
      ) : (
        <div className="space-y-3">
          {records.map((record) => (
            <div
              key={record.id}
              className="bg-white rounded-lg shadow p-4 border-l-4"
              style={{
                borderLeftColor: record.sync_status === 'SYNCED' ? '#22c55e' : '#f59e0b'
              }}
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-medium text-gray-800">
                    {record.emp_name || 'Unknown'}
                  </p>
                  <p className="text-sm text-gray-500">{record.emp_code}</p>
                </div>
                <div className={`px-2 py-1 rounded text-xs font-medium ${
                  record.sync_status === 'SYNCED' 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {record.sync_status}
                </div>
              </div>
              
              <div className="mt-3 flex items-center gap-4 text-sm text-gray-500">
                <div className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  <span>{record.date}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <span>{record.time}</span>
                </div>
              </div>
              
              {record.latitude && record.longitude && (
                <div className="mt-2 flex items-center gap-1 text-xs text-gray-400">
                  <MapPin className="w-3 h-3" />
                  <span>{record.latitude.toFixed(4)}, {record.longitude.toFixed(4)}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
