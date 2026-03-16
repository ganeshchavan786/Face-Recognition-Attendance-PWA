import { attendanceDB } from './db'
import { attendanceApi } from './api'

const DEVICE_ID = getOrCreateDeviceId()

function getOrCreateDeviceId() {
  let deviceId = localStorage.getItem('device_id')
  if (!deviceId) {
    deviceId = 'DEV-' + crypto.randomUUID()
    localStorage.setItem('device_id', deviceId)
  }
  return deviceId
}

export async function syncPendingAttendance() {
  const pendingRecords = await attendanceDB.getPending()
  
  if (pendingRecords.length === 0) {
    console.log('No pending records to sync')
    return { synced: 0, failed: 0 }
  }
  
  console.log(`Syncing ${pendingRecords.length} pending records...`)
  
  try {
    const records = pendingRecords.map(record => ({
      local_id: record.id,
      emp_id: record.emp_id,
      date: record.date,
      time: record.time,
      latitude: record.latitude,
      longitude: record.longitude,
      photo: record.photo
    }))
    
    const response = await attendanceApi.sync(DEVICE_ID, records)
    const { results } = response.data
    
    for (const result of results) {
      if (result.status === 'synced') {
        await attendanceDB.updateStatus(result.local_id, 'SYNCED')
      } else if (result.status === 'duplicate') {
        await attendanceDB.updateStatus(result.local_id, 'SYNCED')
      }
    }
    
    return {
      synced: results.filter(r => r.status === 'synced').length,
      failed: results.filter(r => r.status === 'failed').length
    }
  } catch (error) {
    console.error('Sync failed:', error)
    throw error
  }
}

export function registerBackgroundSync() {
  if ('serviceWorker' in navigator && 'SyncManager' in window) {
    navigator.serviceWorker.ready.then(registration => {
      return registration.sync.register('sync-attendance')
    }).catch(err => {
      console.log('Background sync registration failed:', err)
    })
  }
}

export async function checkAndSync() {
  if (navigator.onLine) {
    try {
      const result = await syncPendingAttendance()
      console.log('Sync completed:', result)
      return result
    } catch (error) {
      console.error('Sync error:', error)
    }
  }
  return null
}

window.addEventListener('online', () => {
  console.log('Back online, attempting sync...')
  checkAndSync()
})
