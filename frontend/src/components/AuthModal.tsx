import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { X, Lock, Mail, Shield, User as UserIcon, Sparkles } from 'lucide-react';

export const AuthModal: React.FC = () => {
  const { isAuthModalOpen, setIsAuthModalOpen, login } = useApp();
  const [email, setEmail] = useState('demo@shopai.com');
  const [password, setPassword] = useState('demo123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isAuthModalOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.message || 'Login failed. Check credentials.');
    } finally {
      setLoading(false);
    }
  };

  const setDemoCustomer = () => {
    setEmail('demo@shopai.com');
    setPassword('demo123');
    setError(null);
  };

  const setDemoAdmin = () => {
    setEmail('admin@shopai.com');
    setPassword('admin123');
    setError(null);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200 relative">
        <button
          onClick={() => setIsAuthModalOpen(false)}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-1">
          <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white">
            <Sparkles className="w-4 h-4 text-amber-300" />
          </div>
          <h3 className="text-xl font-bold text-slate-900">Sign in to ShopAI</h3>
        </div>
        <p className="text-xs text-slate-500 mb-6">
          Use the demo credentials below for instant role-based exploration.
        </p>

        {/* Quick Demo Pre-fill Buttons */}
        <div className="grid grid-cols-2 gap-2 mb-6">
          <button
            type="button"
            onClick={setDemoCustomer}
            className={`p-3 rounded-xl border text-left transition-all ${
              email === 'demo@shopai.com'
                ? 'border-indigo-600 bg-indigo-50/70 text-indigo-950 shadow-sm'
                : 'border-slate-200 hover:border-slate-300 bg-slate-50 text-slate-700'
            }`}
          >
            <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-700 mb-1">
              <UserIcon className="w-3.5 h-3.5" /> Customer
            </div>
            <div className="text-[11px] text-slate-500 font-mono truncate">demo@shopai.com</div>
          </button>

          <button
            type="button"
            onClick={setDemoAdmin}
            className={`p-3 rounded-xl border text-left transition-all ${
              email === 'admin@shopai.com'
                ? 'border-purple-600 bg-purple-50/70 text-purple-950 shadow-sm'
                : 'border-slate-200 hover:border-slate-300 bg-slate-50 text-slate-700'
            }`}
          >
            <div className="flex items-center gap-1.5 text-xs font-bold text-purple-700 mb-1">
              <Shield className="w-3.5 h-3.5" /> Admin
            </div>
            <div className="text-[11px] text-slate-500 font-mono truncate">admin@shopai.com</div>
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-10 pr-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-600 bg-slate-50/50"
                placeholder="name@example.com"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-600 bg-slate-50/50"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-semibold text-sm rounded-xl shadow-md transition-all flex items-center justify-center gap-2 mt-2"
          >
            {loading ? (
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <span>Sign In</span>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};
