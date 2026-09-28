import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import { useFinancialStore } from '../store/financialStore'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { TrendingUp, TrendingDown, Target, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']

export default function DashboardPage() {
  const { token } = useAuthStore()
  const { summary, categoryAnalysis, goals, recommendations, fetchSummary, fetchCategoryAnalysis, fetchGoals, fetchRecommendations } = useFinancialStore()
  const [dateRange, setDateRange] = useState('30d')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [dateRange])

  const getDateRange = () => {
    const end = new Date()
    const start = new Date()

    switch (dateRange) {
      case '3m':
        start.setMonth(start.getMonth() - 3)
        break
      case '6m':
        start.setMonth(start.getMonth() - 6)
        break
      case '1y':
        start.setFullYear(start.getFullYear() - 1)
        break
      default: // 30d
        start.setDate(start.getDate() - 30)
    }

    return {
      start: start.toISOString(),
      end: end.toISOString()
    }
  }

  const loadData = async () => {
    setLoading(true)
    try {
      const { start, end } = getDateRange()

      await Promise.all([
        fetchSummary(token, start, end),
        fetchCategoryAnalysis(token, start, end),
        fetchGoals(token),
        fetchRecommendations(token, start, end)
      ])
    } catch (error) {
      toast.error('Erro ao carregar dados')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Carregando...</div>
  }

  const cards = [
    {
      title: 'Receita Total',
      value: summary?.total_income || 0,
      icon: <TrendingUp className="text-green-500" />,
      color: 'bg-green-50'
    },
    {
      title: 'Despesa Total',
      value: summary?.total_expense || 0,
      icon: <TrendingDown className="text-red-500" />,
      color: 'bg-red-50'
    },
    {
      title: 'Resultado',
      value: summary?.net_result || 0,
      icon: <Target className="text-blue-500" />,
      color: 'bg-blue-50',
      highlight: true
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header com filtro de datas */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <select
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg bg-white"
        >
          <option value="30d">Últimos 30 dias</option>
          <option value="3m">Últimos 3 meses</option>
          <option value="6m">Últimos 6 meses</option>
          <option value="1y">Último ano</option>
        </select>
      </div>

      {/* Cards de resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((card, index) => (
          <div key={index} className={`${card.color} rounded-lg p-6 shadow`}>
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-600 font-medium">{card.title}</p>
                <p className={`text-2xl font-bold mt-2 ${card.highlight ? 'text-blue-600' : 'text-gray-900'}`}>
                  R$ {Math.abs(card.value).toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}
                </p>
              </div>
              {card.icon}
            </div>
          </div>
        ))}
      </div>

      {/* Gráficos e análises */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico de categorias */}
        {categoryAnalysis.length > 0 && (
          <div className="bg-white rounded-lg p-6 shadow">
            <h2 className="text-lg font-semibold mb-4">Gastos por Categoria</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryAnalysis}
                  dataKey="total_amount"
                  nameKey="category_name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {categoryAnalysis.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `R$ ${value.toFixed(2)}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Metas */}
        {goals.length > 0 && (
          <div className="bg-white rounded-lg p-6 shadow">
            <h2 className="text-lg font-semibold mb-4">Metas Financeiras</h2>
            <div className="space-y-4">
              {goals.slice(0, 3).map(goal => (
                <div key={goal.id}>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-900">{goal.title}</span>
                    <span className="text-sm text-gray-600">{Math.round(goal.progress_percentage || 0)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${Math.min((goal.progress_percentage || 0), 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Recomendações */}
      {recommendations.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <AlertCircle className="text-yellow-600 flex-shrink-0 mt-1" />
            <div>
              <h2 className="text-lg font-semibold text-yellow-900 mb-3">Recomendações</h2>
              <div className="space-y-2">
                {recommendations.slice(0, 3).map((rec, index) => (
                  <div key={index} className="text-sm text-yellow-800">
                    <strong>{rec.title}:</strong> {rec.description}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
