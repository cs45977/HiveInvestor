import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || ''
const API_URL = `${BASE_URL}/api/v1`

export const register = async (email, username, password) => {
    const response = await axios.post(`${API_URL}/users/register`, {
        email,
        username,
        password
    })
    return response.data
}

export const login = async (email, password) => {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await axios.post(`${API_URL}/users/login`, formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })

    if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
    }

    return response.data
}
