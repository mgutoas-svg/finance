import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import { useFinancialStore } from '../store/financialStore'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Download } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AnalyticsPage() {
  const { token } = useAuthStore()
  const { categoryAnalysis, fetchCategoryAnalysis } = useFinancialStore()
  const [dateRange, setDateRange] = useState('30d')

  useEffect(() => {
    loadData()
  }, [dateRange])

  const getDateRange = () => {
    const end = new Date().toISOString()
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
      default:
        start.setDate(start.getDate() - 30)
    }

    return { start: start.toISOString(), end }
  }

  const loadData = async () => {
    const { start, end } = getDateRange()
    await fetchCategoryAnalysis(token, start, end)
  }

  const handleExportPDF = async () => {
    try {
      const { start, end } = getDateRange()
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/reports/generate-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          period_start: start,
          period_end: end,
          include_goals: true,
          include_recommendations: true
        })
      })

      if (!response.ok) throw new Error('Erro ao gerar PDF')

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `relatorio_${new Date().toISOString().split('T')[0]}.pdf`
      a.click()

      toast.success('Relatório baixado!')
    } catch (error) {
      toast.error(error.message)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Análises Financeiras</h1>
        <div className="flex gap-2">
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
          <button
            onClick={handleExportPDF}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            <Download size={20} />
            Exportar PDF
          </button>
        </div>
      </div>

      {/* Gráfico de categorias */}
      {categoryAnalysis.length > 0 && (
        <div className="bg-white rounded-lg p-6 shadow">
          <h2 className="text-lg font-semibold mb-4">Gastos por Categoria</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={categoryAnalysis}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category_name" />
              <YAxis />
              <Tooltip formatter={(value) => `R$ ${value.toFixed(2)}`} />
              <Legend />
              <Bar dataKey="total_amount" name="Total" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Tabela de análise */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Categoria</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Total</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">% Total</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Transações</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Média</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {categoryAnalysis.map(cat => (
              <tr key={cat.category_id} className="hover:bg-gray-50">
                <td className="px-6 py-3 text-sm text-gray-900 font-medium">{cat.category_name}</td>
                <td className="px-6 py-3 text-sm text-gray-900">R$ {cat.total_amount.toFixed(2)}</td>
                <td className="px-6 py-3 text-sm text-gray-900">{cat.percentage_of_total.toFixed(1)}%</td>
                <td className="px-6 py-3 text-sm text-gray-900">{cat.transaction_count}</td>
                <td className="px-6 py-3 text-sm text-gray-900">R$ {cat.average_transaction.toFixed(2)}</td>
                <td className="px-6 py-3 text-sm">
                  {cat.is_alert ? (
                    <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-semibold">⚠️ Alerta</span>
                  ) : (
                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-semibold">✓ OK</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
