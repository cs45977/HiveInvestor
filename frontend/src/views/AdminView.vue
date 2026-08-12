<script setup>
import { ref, onMounted } from 'vue'
import { listUsers, updateUserRole, triggerEvaluation } from '@/services/admin'

const users = ref([])
const loading = ref(true)
const error = ref('')
const evaluationStatus = ref('')
const roleUpdateError = ref('')

const loadUsers = async () => {
  loading.value = true
  error.value = ''
  try {
    users.value = await listUsers()
  } catch (err) {
    if (err.response?.status === 403) {
      error.value = 'You do not have admin privileges to view this page.'
    } else {
      error.value = 'Failed to load users: ' + (err.response?.data?.detail || err.message)
    }
  } finally {
    loading.value = false
  }
}

const toggleRole = async (user) => {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  roleUpdateError.value = ''
  try {
    const updated = await updateUserRole(user.id, newRole)
    user.role = updated.role
  } catch (err) {
    roleUpdateError.value = err.response?.data?.detail || 'Failed to update role'
  }
}

const runEvaluation = async () => {
  evaluationStatus.value = 'Running...'
  try {
    const result = await triggerEvaluation()
    evaluationStatus.value = result.message
  } catch (err) {
    evaluationStatus.value = 'Failed: ' + (err.response?.data?.detail || err.message)
  }
}

onMounted(loadUsers)
</script>

<template>
  <div class="admin-view">
    <h1>Admin</h1>

    <section v-if="error" class="error-banner">
      {{ error }}
    </section>

    <section v-else>
      <div class="admin-actions">
        <button @click="runEvaluation">Trigger Portfolio Evaluation</button>
        <span v-if="evaluationStatus" class="status-text">{{ evaluationStatus }}</span>
      </div>

      <p v-if="roleUpdateError" class="error-text">{{ roleUpdateError }}</p>

      <div v-if="loading">Loading users...</div>
      <table v-else class="users-table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Username</th>
            <th>Role</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.email }}</td>
            <td>{{ user.username }}</td>
            <td>
              <span :class="['role-badge', user.role]">{{ user.role }}</span>
            </td>
            <td>
              <button @click="toggleRole(user)">
                {{ user.role === 'admin' ? 'Demote to user' : 'Promote to admin' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<style scoped>
.admin-view {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.error-banner {
  background: #fee2e2;
  color: #991b1b;
  padding: 1rem;
  border-radius: 4px;
}

.error-text {
  color: #991b1b;
  font-size: 0.9rem;
}

.admin-actions {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-text {
  font-size: 0.9rem;
  color: #4b5563;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th,
.users-table td {
  text-align: left;
  padding: 0.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.role-badge {
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  text-transform: uppercase;
}

.role-badge.admin {
  background: #ddd6fe;
  color: #5b21b6;
}

.role-badge.user {
  background: #e5e7eb;
  color: #374151;
}
</style>
