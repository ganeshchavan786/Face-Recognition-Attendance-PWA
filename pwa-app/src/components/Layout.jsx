import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Camera, History, LogOut, Wifi, WifiOff } from 'lucide-react'
import { useState, useEffect } from 'react'

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  const location = useLocation()
  const [isOnline, setIsOnline] = useState(navigator.onLine)

  useEffect(() => {
    const handleOnline = () => setIsOnline(true)
    const handleOffline = () => setIsOnline(false)
    
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    
    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-primary-500 text-white shadow-lg">
        <div className="max-w-lg mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-lg font-semibold">Face Attendance</h1>
          <div className="flex items-center gap-3">
            {isOnline ? (
              <Wifi className="w-5 h-5 text-green-300" />
            ) : (
              <WifiOff className="w-5 h-5 text-red-300" />
            )}
            <button
              onClick={logout}
              className="p-2 hover:bg-primary-600 rounded-full transition"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6">
        {children}
      </main>

      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg">
        <div className="max-w-lg mx-auto flex">
          <Link
            to="/"
            className={`flex-1 flex flex-col items-center py-3 ${
              location.pathname === '/' ? 'text-primary-500' : 'text-gray-500'
            }`}
          >
            <Camera className="w-6 h-6" />
            <span className="text-xs mt-1">Attendance</span>
          </Link>
          <Link
            to="/history"
            className={`flex-1 flex flex-col items-center py-3 ${
              location.pathname === '/history' ? 'text-primary-500' : 'text-gray-500'
            }`}
          >
            <History className="w-6 h-6" />
            <span className="text-xs mt-1">History</span>
          </Link>
        </div>
      </nav>
    </div>
  )
}
