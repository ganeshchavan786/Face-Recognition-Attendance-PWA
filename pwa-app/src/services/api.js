import axios from 'axios'

export const api = axios.create({
  baseURL: '/api'
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const employeeApi = {
  getAll: (includeDescriptors = false) => api.get('/employees', { params: { include_descriptors: includeDescriptors } }),
  getById: (id) => api.get(`/employees/${id}`),
  create: (data) => api.post('/employees', data),
  update: (id, data) => api.put(`/employees/${id}`, data),
  delete: (id) => api.delete(`/employees/${id}`),
  enrollFace: (id, descriptors) => api.post(`/employees/${id}/enroll-face`, { face_descriptors: descriptors })
}

export const attendanceApi = {
  sync: (deviceId, records) => api.post('/attendance/sync', { device_id: deviceId, records }),
  getAll: (params) => api.get('/attendance', { params }),
  getSummary: (params) => api.get('/attendance/summary', { params })
}
