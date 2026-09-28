import { useState, useEffect } from 'react'
import { useAuthStore } from '../store/authStore'
import { useFinancialStore } from '../store/financialStore'
import { Plus, Trash2, Upload } from 'lucide-react'
import toast from 'react-hot-toast'

export default function TransactionsPage() {
  const { token } = useAuthStore()
  const { transactions, fetchTransactions, categories, fetchCategories } = useFinancialStore()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    description: '',
    amount: '',
    transaction_date: new Date().toISOString().split('T')[0],
    transaction_type: 'expense',
    category_id: ''
  })
  const [file, setFile] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    await fetchTransactions(token)
    await fetchCategories(token)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/transactions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          ...formData,
          amount: parseFloat(formData.amount),
          category_id: formData.category_id ? parseInt(formData.category_id) : null
        })
      })

      if (!response.ok) throw new Error('Erro ao criar transação')

      toast.success('Transação criada!')
      setShowForm(false)
      setFormData({
        description: '',
        amount: '',
        transaction_date: new Date().toISOString().split('T')[0],
        transaction_type: 'expense',
        category_id: ''
      })
      await fetchTransactions(token)
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const formDataFile = new FormData()
    formDataFile.append('file', file)

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/transactions/import`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formDataFile
      })

      if (!response.ok) throw new Error('Erro ao importar')

      const result = await response.json()
      toast.success(`${result.records_imported} transações importadas!`)
      await fetchTransactions(token)
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Deseja deletar esta transação?')) return

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/transactions/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) throw new Error('Erro ao deletar')

      toast.success('Transação deletada!')
      await fetchTransactions(token)
    } catch (error) {
      toast.error(error.message)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Transações</h1>
        <div className="flex gap-2">
          <label className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 cursor-pointer">
            <Upload size={20} />
            Importar
            <input type="file" accept=".csv,.xlsx,.pdf" onChange={handleFileUpload} className="hidden" />
          </label>
          <button
            onClick={() => setShowForm(!showForm)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <Plus size={20} />
            Nova
          </button>
        </div>
      </div>

      {/* Form */}
      {showForm && (
        <div className="bg-white rounded-lg p-6 shadow">
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Descrição"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="px-4 py-2 border rounded-lg"
              required
            />
            <input
              type="number"
              placeholder="Valor"
              step="0.01"
              value={formData.amount}
              onChange={(e) => setFormData({...formData, amount: e.target.value})}
              className="px-4 py-2 border rounded-lg"
              required
            />
            <input
              type="date"
              value={formData.transaction_date}
              onChange={(e) => setFormData({...formData, transaction_date: e.target.value})}
              className="px-4 py-2 border rounded-lg"
              required
            />
            <select
              value={formData.transaction_type}
              onChange={(e) => setFormData({...formData, transaction_type: e.target.value})}
              className="px-4 py-2 border rounded-lg"
            >
              <option value="expense">Despesa</option>
              <option value="income">Receita</option>
            </select>
            <select
              value={formData.category_id}
              onChange={(e) => setFormData({...formData, category_id: e.target.value})}
              className="px-4 py-2 border rounded-lg"
            >
              <option value="">Sem categoria</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Salvar
            </button>
          </form>
        </div>
      )}

      {/* List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Data</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Descrição</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Categoria</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Valor</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {transactions.map(trans => {
              const category = categories.find(c => c.id === trans.category_id)
              return (
                <tr key={trans.id} className="hover:bg-gray-50">
                  <td className="px-6 py-3 text-sm text-gray-900">{new Date(trans.transaction_date).toLocaleDateString('pt-BR')}</td>
                  <td className="px-6 py-3 text-sm text-gray-900">{trans.description}</td>
                  <td className="px-6 py-3 text-sm text-gray-600">{category?.name || '-'}</td>
                  <td className={`px-6 py-3 text-sm font-semibold ${trans.transaction_type === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                    {trans.transaction_type === 'income' ? '+' : '-'} R$ {Math.abs(trans.amount).toFixed(2)}
                  </td>
                  <td className="px-6 py-3 text-sm">
                    <button
                      onClick={() => handleDelete(trans.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
