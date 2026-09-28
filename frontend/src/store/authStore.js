import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      setUser: (user) => set({ user }),
      setToken: (token) => set({ token }),
      setRefreshToken: (refreshToken) => set({ refreshToken }),
      setIsLoading: (isLoading) => set({ isLoading }),
      setError: (error) => set({ error }),

      login: async (email, password) => {
        set({ isLoading: true, error: null })
        try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
          })

          if (!response.ok) {
            throw new Error('Email ou senha incorretos')
          }

          const data = await response.json()
          set({
            token: data.access_token,
            refreshToken: data.refresh_token,
            isAuthenticated: true,
            error: null
          })

          return true
        } catch (error) {
          set({ error: error.message, isAuthenticated: false })
          return false
        } finally {
          set({ isLoading: false })
        }
      },

      logout: () => set({
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false
      }),

      changePassword: async (currentPassword, newPassword) => {
        set({ isLoading: true, error: null })
        try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/change-password`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${get().token}`
            },
            body: JSON.stringify({
              current_password: currentPassword,
              new_password: newPassword
            })
          })

          if (!response.ok) {
            throw new Error('Erro ao alterar senha')
          }

          set({ error: null })
          return true
        } catch (error) {
          set({ error: error.message })
          return false
        } finally {
          set({ isLoading: false })
        }
      }
    }),
    {
      name: 'auth-storage'
    }
  )
)
