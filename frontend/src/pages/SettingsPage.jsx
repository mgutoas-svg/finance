import { useState } from 'react'
import { useAuthStore } from '../store/authStore'
import { useNavigate } from 'react-router-dom'
import { Lock, Mail } from 'lucide-react'
import toast from 'react-hot-toast'

export default function SettingsPage() {
  const navigate = useNavigate()
  const { token, logout, changePassword } = useAuthStore()
  const [activeTab, setActiveTab] = useState('password')
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  })
  const [emailForm, setEmailForm] = useState({
    recovery_email: ''
  })
  const [loading, setLoading] = useState(false)

  const handlePasswordChange = async (e) => {
    e.preventDefault()

    if (passwordForm.new_password !== passwordForm.confirm_password) {
      toast.error('As senhas não conferem')
      return
    }

    setLoading(true)
    const success = await changePassword(
      passwordForm.current_password,
      passwordForm.new_password
    )

    if (success) {
      toast.success('Senha alterada com sucesso!')
      setPasswordForm({ current_password: '', new_password: '', confirm_password: '' })
    } else {
      toast.error('Erro ao alterar senha')
    }

    setLoading(false)
  }

  const handleEmailChange = async (e) => {
    e.preventDefault()

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/set-recovery-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(emailForm)
      })

      if (!response.ok) throw new Error('Erro ao atualizar email')

      toast.success('Email de recuperação atualizado!')
      setEmailForm({ recovery_email: '' })
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
    toast.success('Você saiu da sua conta')
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Configurações</h1>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <div className="flex gap-4">
          <button
            onClick={() => setActiveTab('password')}
            className={`px-4 py-2 border-b-2 transition-colors ${
              activeTab === 'password'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            <Lock className="inline mr-2" size={20} />
            Senha
          </button>
          <button
            onClick={() => setActiveTab('email')}
            className={`px-4 py-2 border-b-2 transition-colors ${
              activeTab === 'email'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            <Mail className="inline mr-2" size={20} />
            Email de Recuperação
          </button>
        </div>
      </div>

      {/* Tab Content */}
      <div className="bg-white rounded-lg p-6 shadow">
        {activeTab === 'password' && (
          <form onSubmit={handlePasswordChange} className="space-y-4 max-w-md">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Senha Atual
              </label>
              <input
                type="password"
                value={passwordForm.current_password}
                onChange={(e) => setPasswordForm({...passwordForm, current_password: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nova Senha
              </label>
              <input
                type="password"
                value={passwordForm.new_password}
                onChange={(e) => setPasswordForm({...passwordForm, new_password: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                minLength="8"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Confirmar Senha
              </label>
              <input
                type="password"
                value={passwordForm.confirm_password}
                onChange={(e) => setPasswordForm({...passwordForm, confirm_password: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Atualizando...' : 'Alterar Senha'}
            </button>
          </form>
        )}

        {activeTab === 'email' && (
          <form onSubmit={handleEmailChange} className="space-y-4 max-w-md">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email de Recuperação
              </label>
              <input
                type="email"
                value={emailForm.recovery_email}
                onChange={(e) => setEmailForm({...emailForm, recovery_email: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="seu-email@exemplo.com"
                required
              />
              <p className="text-xs text-gray-500 mt-2">
                Use este email para recuperar sua conta caso esqueça a senha
              </p>
            </div>

            <button
              type="submit"
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Atualizar Email
            </button>
          </form>
        )}
      </div>

      {/* Logout */}
      <div className="bg-red-50 rounded-lg p-6 shadow">
        <h3 className="text-lg font-semibold text-red-900 mb-2">Sair da Conta</h3>
        <p className="text-sm text-red-700 mb-4">
          Você será desconectado de sua conta
        </p>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Sair Agora
        </button>
      </div>
    </div>
  )
}
