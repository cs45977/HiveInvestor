import { reactive, computed } from 'vue';
import axios from 'axios'; // Import axios
import { login as apiLogin, register as apiRegister } from '../services/auth'; // Renamed to avoid conflicts
import router from '../router';

const authState = reactive({
  isAuthenticated: false,
  user: null,
  token: localStorage.getItem('token') || null,
});

const checkAuth = async () => {
  if (authState.token) {
    try {
      // Verify the token and fetch user details from the backend
      const userResponse = await axios.get('/api/v1/users/me', {
        headers: {
          Authorization: `Bearer ${authState.token}`
        }
      });
      authState.user = userResponse.data;
      authState.isAuthenticated = true;
      localStorage.setItem('user', JSON.stringify(authState.user)); // Update user in local storage
    } catch (error) {
      console.error('Auth check failed:', error);
      logout(); // Token might be invalid or expired, log out
    }
  }
};

const login = async (email, password) => {
  try {
    const response = await apiLogin(email, password); // This gets the token
    authState.token = response.access_token;
    localStorage.setItem('token', authState.token);

    // Fetch user details to get role etc.
    const userResponse = await axios.get('/api/v1/users/me', {
      headers: {
        Authorization: `Bearer ${authState.token}`
      }
    });
    authState.user = userResponse.data;
    localStorage.setItem('user', JSON.stringify(authState.user));

    authState.isAuthenticated = true;
    router.push('/dashboard'); // Redirect to dashboard after login
    return true;
  } catch (error) {
    console.error('Login failed:', error);
    logout(); // Ensure state is clean on failed login
    throw error;
  }
};

const registerAndLogin = async (email, username, password) => {
  try {
    const registeredUserResponse = await apiRegister(email, username, password); // Register returns the user object directly
    
    // After successful registration, call the login API to get a token and set auth state
    const loginResponse = await apiLogin(email, password);
    authState.token = loginResponse.access_token;
    localStorage.setItem('token', authState.token);

    // Use the user object obtained from registration, or fetch from /me again for consistency
    // For now, assume registeredUserResponse is enough (it has id, email, username, role)
    // If the register response gets updated by the server (e.g., initial portfolio created),
    // a fetch from /me might be better. Keeping it simple here.
    authState.user = registeredUserResponse; // Use the response from register API directly
    localStorage.setItem('user', JSON.stringify(authState.user));

    authState.isAuthenticated = true;
    router.push('/dashboard'); // Redirect to dashboard after registration and login
    return true;
  } catch (error) {
    console.error('Registration or auto-login failed:', error);
    logout(); // Ensure state is clean on failed registration/login
    throw error;
  }
};


const logout = () => {
  authState.isAuthenticated = false;
  authState.user = null;
  authState.token = null;
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login'); // Redirect to login page after logout
};

const isAdmin = computed(() => {
  return authState.isAuthenticated && authState.user && authState.user.role === 'admin';
});

export function useAuthStore() {
  // Check auth state on initial load
  // This needs to be done once, not every time useAuthStore is called
  // The initial check can be done in main.js or the root component
  return {
    authState,
    login,
    registerAndLogin,
    logout,
    isAdmin,
    checkAuth // Expose checkAuth for initial app load
  };
}
