import axios from 'axios';

const API_URL = '/api/v1';

export const register = async (email, username, password) => {
    try {
        const response = await axios.post(`${API_URL}/users/register`, {
            email,
            username,
            password
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const login = async (email, password) => {
    const formData = new FormData();
    formData.append('username', email); // OAuth2 expects 'username'
    formData.append('password', password);

    try {
        const response = await axios.post(`${API_URL}/users/login`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}
