import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || ''
const API_URL = `${BASE_URL}/api/v1/admin`

const authHeaders = () => {
    const token = localStorage.getItem('token')
    return { 'Authorization': `Bearer ${token}` }
}

export const listUsers = async () => {
    const response = await axios.get(`${API_URL}/users`, { headers: authHeaders() })
    return response.data
}

export const updateUserRole = async (userId, role) => {
    const response = await axios.patch(
        `${API_URL}/users/${userId}/role`,
        { role },
        { headers: authHeaders() }
    )
    return response.data
}

export const triggerEvaluation = async () => {
    const response = await axios.post(
        `${BASE_URL}/api/v1/leaderboard/admin/evaluate`,
        {},
        { headers: authHeaders() }
    )
    return response.data
}
