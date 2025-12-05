import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || ''
const API_URL = `${BASE_URL}/api/v1`

export const getPortfolio = async () => {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/portfolios/me`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    return response.data
}

export const executeTrade = async (tradeRequest) => {
    const token = localStorage.getItem('token')
    const response = await axios.post(`${API_URL}/trade/`, tradeRequest, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    return response.data
}

export const getQuote = async (symbol) => {
    const token = localStorage.getItem('token')
    console.log(`[getQuote] Fetching quote for ${symbol}. Token present: ${!!token}`)
    if (!token) console.warn('[getQuote] No token found in localStorage!')

    const response = await axios.get(`${API_URL}/market/quote/${symbol}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    return response.data
}

export const getHistory = async (symbol, resolution, limit) => {
    const token = localStorage.getItem('token')
    console.log(`[getHistory] Fetching history for ${symbol}. Token present: ${!!token}`)

    const response = await axios.get(`${API_URL}/market/history/${symbol}`, {
        params: { resolution, limit },
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    return response.data
}

export const getTransactions = async () => {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/transactions/`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    return response.data
}

export const getLeaderboard = async (window) => {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/leaderboard/${window}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    return response.data
}
