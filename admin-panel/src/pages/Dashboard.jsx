import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Users, UserCheck, UserX, CalendarCheck, ArrowRight } from 'lucide-react'
import { employeeApi, attendanceApi } from '../services/api'
import { format, startOfMonth, endOfMonth } from 'date-fns'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalEmployees: 0,
    enrolledFaces: 0,
    pendingEnrollment: 0,
    todayAttendance: 0
  })
  const [loading, setLoading] = useState(true)
  const [recentEmployees, setRecentEmployees] = useState([])

  useEffect(() => {
    loadDashboardData()
  }, [])

  async function loadDashboardData() {
    try {
      const empResponse = await employeeApi.getAll({ limit: 100 })
      const employees = empResponse.data.employees || []
      
      const enrolled = employees.filter(e => e.face_enrolled).length
      const pending = employees.filter(e => !e.face_enrolled).length
      
      const today = format(new Date(), 'yyyy-MM-dd')
      let todayCount = 0
      try {
        const attResponse = await attendanceApi.getSummary({
          start_date: today,
          end_date: today
        })
        todayCount = attResponse.data.total_attendance_records || 0
      } catch (e) {
        console.log('Attendance summary not available')
      }

      setStats({
        totalEmployees: employees.length,
        enrolledFaces: enrolled,
        pendingEnrollment: pending,
        todayAttendance: todayCount
      })

      setRecentEmployees(employees.slice(0, 5))
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    { label: 'Total Employees', value: stats.totalEmployees, icon: Users, color: 'bg-blue-500' },
    { label: 'Face Enrolled', value: stats.enrolledFaces, icon: UserCheck, color: 'bg-green-500' },
    { label: 'Pending Enrollment', value: stats.pendingEnrollment, icon: UserX, color: 'bg-orange-500' },
    { label: "Today's Attendance", value: stats.todayAttendance, icon: CalendarCheck, color: 'bg-purple-500' },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-500">Welcome to Face Attendance Admin Panel</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <div key={index} className="bg-white rounded-xl shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-800 mt-1">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Recent Employees */}
      <div className="bg-white rounded-xl shadow">
        <div className="p-4 border-b flex items-center justify-between">
          <h2 className="font-semibold text-gray-800">Recent Employees</h2>
          <Link to="/employees" className="text-primary-600 text-sm flex items-center gap-1 hover:underline">
            View All <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="divide-y">
          {recentEmployees.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              No employees yet. <Link to="/employees" className="text-primary-600 hover:underline">Add one</Link>
            </div>
          ) : (
            recentEmployees.map((emp) => (
              <div key={emp.id} className="p-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                    <span className="text-gray-600 font-medium">
                      {emp.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-800">{emp.name}</p>
                    <p className="text-sm text-gray-500">{emp.emp_code} • {emp.department || 'N/A'}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {emp.face_enrolled ? (
                    <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                      Enrolled
                    </span>
                  ) : (
                    <Link
                      to={`/employees/${emp.id}/enroll`}
                      className="px-3 py-1 bg-orange-100 text-orange-700 text-xs rounded-full hover:bg-orange-200"
                    >
                      Enroll Face
                    </Link>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
