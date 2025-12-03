import { mount, flushPromises } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ProfileView from '../ProfileView.vue';
import { useAuthStore } from '../../stores/auth';

// Mock the auth store
vi.mock('../../stores/auth', () => ({
  useAuthStore: vi.fn(),
}));

const pushMock = vi.fn();
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

describe('ProfileView', () => {
  beforeEach(() => {
    // Reset mocks before each test
    pushMock.mockClear();
    useAuthStore.mockReturnValue({
      isAuthenticated: true,
      user: {
        email: 'test@example.com',
        username: 'testuser',
      },
      fetchUser: vi.fn().mockResolvedValue(true),
      updateUser: vi.fn(),
    });
  });

  it('renders correctly when authenticated', async () => {
    const wrapper = mount(ProfileView, {
      global: {
        stubs: {
          RouterLink: true, // Stub RouterLink if used
        },
      },
    });
    await flushPromises(); // Wait for onMounted

    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find('h1').text()).toBe('User Profile');
    // Check if the form elements are present
    expect(wrapper.find('label[for="email"]').exists()).toBe(true);
    expect(wrapper.find('input[id="email"]').element.value).toBe('test@example.com');
    expect(wrapper.find('label[for="username"]').exists()).toBe(true);
    expect(wrapper.find('input[id="username"]').element.value).toBe('testuser');
    expect(wrapper.find('button[type="submit"]').text()).toBe('Update Profile');
  });

  it('fetches user data on mount', () => {
    const fetchUserMock = vi.fn().mockResolvedValue(true);
    useAuthStore.mockReturnValue({
      isAuthenticated: true,
      user: { email: '', username: '' },
      fetchUser: fetchUserMock,
      updateUser: vi.fn(),
    });

    mount(ProfileView);

    expect(fetchUserMock).toHaveBeenCalled();
  });

  it('updates user profile successfully', async () => {
    const updateUserMock = vi.fn().mockResolvedValue(true); // returns true on success
    useAuthStore.mockReturnValue({
      isAuthenticated: true,
      user: { email: 'test@example.com', username: 'olduser' },
      fetchUser: vi.fn().mockResolvedValue(true),
      updateUser: updateUserMock,
    });

    const wrapper = mount(ProfileView);
    await flushPromises(); // Wait for onMounted initialization
    
    // Set new username
    const usernameInput = wrapper.find('input[id="username"]');
    await usernameInput.setValue('newuser');
    
    // Submit form
    await wrapper.find('form').trigger('submit.prevent');

    expect(updateUserMock).toHaveBeenCalledWith({ username: 'newuser' });
    // Verify success message is displayed (assuming implementation will show it)
    expect(wrapper.text()).toContain('Profile updated successfully');
  });

  it('displays error message on update failure', async () => {
    const updateUserMock = vi.fn().mockRejectedValue(new Error('Update failed'));
    useAuthStore.mockReturnValue({
      isAuthenticated: true,
      user: { email: 'test@example.com', username: 'olduser' },
      fetchUser: vi.fn().mockResolvedValue(true),
      updateUser: updateUserMock,
    });

    const wrapper = mount(ProfileView);
    await flushPromises(); 
    
    // Submit form
    await wrapper.find('form').trigger('submit.prevent');

    expect(updateUserMock).toHaveBeenCalled();
    // Verify error message is displayed
    expect(wrapper.text()).toContain('Update failed'); // Or a generic error message
  });

  it('redirects to login if not authenticated', async () => {
    useAuthStore.mockReturnValue({
      isAuthenticated: false,
      user: null,
      fetchUser: vi.fn(),
      updateUser: vi.fn(),
    });

    mount(ProfileView);
    await flushPromises();

    expect(pushMock).toHaveBeenCalledWith('/login');
  });
});
