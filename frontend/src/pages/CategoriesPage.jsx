import { useState, useEffect } from 'react'
import { useAuthStore } from '../store/authStore'
import { useFinancialStore } from '../store/financialStore'
import { Plus, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function CategoriesPage() {
  const { token } = useAuthStore()
  const { categories, fetchCategories } = useFinancialStore()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', description: '', ideal_percentage: 0 })

  useEffect(() => {
    fetchCategories(token)
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/categories`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      })

      if (!response.ok) throw new Error('Erro ao criar categoria')

      toast.success('Categoria criada!')
      setShowForm(false)
      setFormData({ name: '', description: '', ideal_percentage: 0 })
      await fetchCategories(token)
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleDelete = async (id, isCustom) => {
    if (!isCustom) {
      toast.error('Não é possível deletar categorias padrão')
      return
    }

    if (!confirm('Deseja deletar esta categoria?')) return

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/categories/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (!response.ok) throw new Error('Erro ao deletar')

      toast.success('Categoria deletada!')
      await fetchCategories(token)
    } catch (error) {
      toast.error(error.message)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Categorias</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus size={20} />
          Nova Categoria
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg p-6 shadow">
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Nome da categoria"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg"
              required
            />
            <textarea
              placeholder="Descrição"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg"
              rows="3"
            />
            <input
              type="number"
              placeholder="% Ideal"
              step="0.1"
              value={formData.ideal_percentage}
              onChange={(e) => setFormData({...formData, ideal_percentage: parseFloat(e.target.value)})}
              className="w-full px-4 py-2 border rounded-lg"
            />
            <button type="submit" className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Salvar
            </button>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {categories.map(cat => (
          <div key={cat.id} className="bg-white rounded-lg p-4 shadow">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-gray-900">{cat.name}</h3>
              {cat.is_custom && (
                <button
                  onClick={() => handleDelete(cat.id, cat.is_custom)}
                  className="text-red-600 hover:text-red-900"
                >
                  <Trash2 size={16} />
                </button>
              )}
            </div>
            {cat.description && <p className="text-sm text-gray-600 mb-2">{cat.description}</p>}
            <div className="text-sm text-gray-500">
              Meta: {cat.ideal_percentage}%
              {!cat.is_custom && <span className="ml-2 text-xs bg-gray-200 px-2 py-1 rounded">Padrão</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
