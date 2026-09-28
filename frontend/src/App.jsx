import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import { Toaster } from 'react-hot-toast'

// Pages
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import TransactionsPage from './pages/TransactionsPage'
import CategoriesPage from './pages/CategoriesPage'
import GoalsPage from './pages/GoalsPage'
import AnalyticsPage from './pages/AnalyticsPage'
import SettingsPage from './pages/SettingsPage'

// Layout
import Layout from './components/Layout'
import PrivateRoute from './components/PrivateRoute'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <>
      <Router>
        <Routes>
          {/* Login */}
          <Route
            path="/login"
            element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />}
          />

          {/* Protected routes */}
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Layout>
                  <DashboardPage />
                </Layout>
              </PrivateRoute>
            }
          />

          <Route
            path="/transacoes"
            element={
              <PrivateRoute>
                <Layout>
                  <TransactionsPage />
                </Layout>
              </PrivateRoute>
            }
          />

          <Route
            path="/categorias"
            element={
              <PrivateRoute>
                <Layout>
                  <CategoriesPage />
                </Layout>
              </PrivateRoute>
            }
          />

          <Route
            path="/metas"
            element={
              <PrivateRoute>
                <Layout>
                  <GoalsPage />
                </Layout>
              </PrivateRoute>
            }
          />

          <Route
            path="/analises"
            element={
              <PrivateRoute>
                <Layout>
                  <AnalyticsPage />
                </Layout>
              </PrivateRoute>
            }
          />

          <Route
            path="/configuracoes"
            element={
              <PrivateRoute>
                <Layout>
                  <SettingsPage />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* 404 */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>

      <Toaster position="top-right" />
    </>
  )
}

export default App
