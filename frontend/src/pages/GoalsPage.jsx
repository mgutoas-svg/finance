import { useState, useEffect } from 'react'
import { useAuthStore } from '../store/authStore'
import { useFinancialStore } from '../store/financialStore'
import { Plus, Trash2, Target } from 'lucide-react'
import toast from 'react-hot-toast'

export default function GoalsPage() {
  const { token } = useAuthStore()
  const { goals, fetchGoals } = useFinancialStore()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    target_amount: '',
    frequency: 'monthly',
    due_date: ''
  })

  useEffect(() => {
    fetchGoals(token)
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/goals`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          ...formData,
          target_amount: parseFloat(formData.target_amount),
          due_date: formData.due_date ? new Date(formData.due_date).toISOString() : null
        })
      })

      if (!response.ok) throw new Error('Erro ao criar meta')

      toast.success('Meta criada!')
      setShowForm(false)
      setFormData({ title: '', description: '', target_amount: '', frequency: 'monthly', due_date: '' })
      await fetchGoals(token)
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Deseja deletar esta meta?')) return

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/goals/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (!response.ok) throw new Error('Erro ao deletar')

      toast.success('Meta deletada!')
      await fetchGoals(token)
    } catch (error) {
      toast.error(error.message)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Metas Financeiras</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus size={20} />
          Nova Meta
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg p-6 shadow">
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Título da meta"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg"
              required
            />
            <textarea
              placeholder="Descrição"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg"
              rows="2"
            />
            <input
              type="number"
              placeholder="Valor alvo"
              step="0.01"
              value={formData.target_amount}
              onChange={(e) => setFormData({...formData, target_amount: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg"
              required
            />
            <select
              value={formData.frequency}
              onChange={(e) => setFormData({...formData, frequency: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="daily">Diária</option>
              <option value="weekly">Semanal</option>
              <option value="monthly">Mensal</option>
            </select>
            <input
              type="date"
              value={formData.due_date}
              onChange={(e) => setFormData({...formData, due_date: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg"
            />
            <button type="submit" className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Criar Meta
            </button>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {goals.map(goal => (
          <div key={goal.id} className="bg-white rounded-lg p-6 shadow">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-start gap-3">
                <Target className="text-blue-600 mt-1" size={24} />
                <div>
                  <h3 className="font-semibold text-gray-900 text-lg">{goal.title}</h3>
                  {goal.description && <p className="text-sm text-gray-600 mt-1">{goal.description}</p>}
                </div>
              </div>
              <button
                onClick={() => handleDelete(goal.id)}
                className="text-red-600 hover:text-red-900"
              >
                <Trash2 size={18} />
              </button>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Progresso</span>
                <span className="font-semibold">{Math.round(goal.progress_percentage || 0)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-blue-600 h-3 rounded-full transition-all"
                  style={{ width: `${Math.min((goal.progress_percentage || 0), 100)}%` }}
                />
              </div>

              <div className="grid grid-cols-2 gap-2 text-sm pt-2">
                <div>
                  <span className="text-gray-600">Atual: </span>
                  <span className="font-semibold">R$ {goal.current_amount.toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-gray-600">Meta: </span>
                  <span className="font-semibold">R$ {goal.target_amount.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
