import { create } from 'zustand'

export const useFinancialStore = create((set, get) => ({
  transactions: [],
  categories: [],
  goals: [],
  summary: null,
  categoryAnalysis: [],
  recommendations: [],
  isLoading: false,
  error: null,

  setTransactions: (transactions) => set({ transactions }),
  setCategories: (categories) => set({ categories }),
  setGoals: (goals) => set({ goals }),
  setSummary: (summary) => set({ summary }),
  setCategoryAnalysis: (analysis) => set({ categoryAnalysis: analysis }),
  setRecommendations: (recommendations) => set({ recommendations }),
  setIsLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),

  fetchTransactions: async (token, params = {}) => {
    set({ isLoading: true, error: null })
    try {
      const queryString = new URLSearchParams(params).toString()
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/transactions?${queryString}`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      )

      if (!response.ok) throw new Error('Erro ao buscar transações')

      const data = await response.json()
      set({ transactions: data })
      return data
    } catch (error) {
      set({ error: error.message })
      return []
    } finally {
      set({ isLoading: false })
    }
  },

  fetchSummary: async (token, startDate, endDate) => {
    set({ isLoading: true })
    try {
      const params = new URLSearchParams({
        start_date: startDate,
        end_date: endDate
      })

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/analytics/summary?${params}`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      )

      if (!response.ok) throw new Error('Erro ao buscar resumo')

      const data = await response.json()
      set({ summary: data })
      return data
    } catch (error) {
      set({ error: error.message })
    } finally {
      set({ isLoading: false })
    }
  },

  fetchCategoryAnalysis: async (token, startDate, endDate) => {
    try {
      const params = new URLSearchParams({
        start_date: startDate,
        end_date: endDate
      })

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/analytics/by-category?${params}`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      )

      if (!response.ok) throw new Error('Erro ao buscar análise')

      const data = await response.json()
      set({ categoryAnalysis: data })
      return data
    } catch (error) {
      set({ error: error.message })
      return []
    }
  },

  fetchCategories: async (token) => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/categories`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      )

      if (!response.ok) throw new Error('Erro ao buscar categorias')

      const data = await response.json()
      set({ categories: data })
      return data
    } catch (error) {
      set({ error: error.message })
      return []
    }
  },

  fetchGoals: async (token) => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/goals`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      )

      if (!response.ok) throw new Error('Erro ao buscar metas')

      const data = await response.json()
      set({ goals: data })
      return data
    } catch (error) {
      set({ error: error.message })
      return []
    }
  },

  fetchRecommendations: async (token, startDate, endDate) => {
    try {
      const params = new URLSearchParams({
        start_date: startDate,
        end_date: endDate
      })

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/analytics/recommendations?${params}`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      )

      if (!response.ok) throw new Error('Erro ao buscar recomendações')

      const data = await response.json()
      set({ recommendations: data })
      return data
    } catch (error) {
      set({ error: error.message })
      return []
    }
  }
}))
