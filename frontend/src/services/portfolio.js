import axios from 'axios'

const API_URL = '/api/v1'

export const getPortfolio = async () => {
    const token = localStorage.getItem('token')
    // Ideally we use an axios instance with interceptor
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
    // Endpoint is public, no auth required
    const response = await axios.get(`${API_URL}/market/quote/${symbol}`)
    return response.data
}

export const getHistory = async (symbol, resolution, limit) => {
    const response = await axios.get(`${API_URL}/market/history/${symbol}`, {
        params: { resolution, limit }
    })
    return response.data
}

export const cancelTransaction = async (transactionId) => {
    const token = localStorage.getItem('token')
    const response = await axios.post(`${API_URL}/transactions/${transactionId}/cancel`, {}, {
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




