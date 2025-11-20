export const register = async (email, username, password) => {
    // Placeholder for API call
    return new Promise(resolve => setTimeout(() => resolve({ id: '123', email, username }), 500));
}

export const login = async (email, password) => {
    // Placeholder for API call
    return new Promise(resolve => setTimeout(() => resolve({ access_token: 'fake-jwt-token', token_type: 'bearer' }), 500));
}
