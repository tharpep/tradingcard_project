import { useState, useEffect } from 'react'
import { LoginPage } from './components/LoginPage'
import { SignupPage } from './components/SignupPage'
import { CardCollection } from './components/CardCollection'
import { api, getAuthToken } from './services/api'

type AuthState = 'login' | 'signup' | 'authenticated'

function App() {
  const [authState, setAuthState] = useState<AuthState>('login')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Check for existing auth token on app load
  useEffect(() => {
    const token = getAuthToken()
    if (token) {
      setAuthState('authenticated')
    }
  }, [])

  // Real authentication handlers
  const handleLogin = async (email: string, password: string) => {
    setLoading(true)
    setError(null)
    
    try {
      await api.login({ email, password })
      setAuthState('authenticated')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleSignup = async (email: string, password: string, username: string) => {
    setLoading(true)
    setError(null)
    
    try {
      await api.signup({ email, password, username })
      setAuthState('authenticated')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await api.logout()
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      setAuthState('login')
      setError(null)
    }
  }

  const switchToLogin = () => {
    setAuthState('login')
    setError(null)
  }

  const switchToSignup = () => {
    setAuthState('signup')
    setError(null)
  }

  // Show authentication pages
  if (authState === 'login') {
    return (
      <LoginPage
        onLogin={handleLogin}
        onSwitchToSignup={switchToSignup}
        loading={loading}
        error={error || undefined}
      />
    )
  }

  if (authState === 'signup') {
    return (
      <SignupPage
        onSignup={handleSignup}
        onSwitchToLogin={switchToLogin}
        loading={loading}
        error={error || undefined}
      />
    )
  }

  // Show card collection when authenticated
  return <CardCollection onLogout={handleLogout} />
}

export default App