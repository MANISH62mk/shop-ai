import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShoppingBag, Sparkles, User as UserIcon, Shield, Search, PackageCheck } from 'lucide-react';
import { useApp } from '../context/AppContext';

export const Navbar: React.FC = () => {
  const { user, cartCount, setIsAuthModalOpen, logout } = useApp();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-700 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5 text-amber-300" />
            </div>
            <div>
              <span className="text-xl font-black tracking-tight bg-gradient-to-r from-slate-900 via-indigo-950 to-indigo-800 bg-clip-text text-transparent">
                SHOP<span className="text-indigo-600">AI</span>
              </span>
              <span className="hidden sm:inline-block ml-2 px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 rounded border border-indigo-200/60">
                Semantic Store
              </span>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1 text-sm font-semibold">
            <Link
              to="/"
              className={`px-3.5 py-2 rounded-lg transition-colors ${
                isActive('/') ? 'text-indigo-600 bg-indigo-50/70 font-bold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              Home
            </Link>
            <Link
              to="/discover"
              className={`px-3.5 py-2 rounded-lg transition-colors flex items-center gap-1.5 ${
                isActive('/discover') ? 'text-indigo-600 bg-indigo-50/70 font-bold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              <Search className="w-4 h-4 text-slate-400" />
              Discover
            </Link>
            <Link
              to="/orders"
              className={`px-3.5 py-2 rounded-lg transition-colors flex items-center gap-1.5 ${
                isActive('/orders') ? 'text-indigo-600 bg-indigo-50/70 font-bold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              <PackageCheck className="w-4 h-4 text-slate-400" />
              Orders
            </Link>
            {user?.role === 'admin' && (
              <Link
                to="/admin"
                className={`px-3.5 py-2 rounded-lg transition-colors flex items-center gap-1.5 ${
                  isActive('/admin') ? 'text-purple-600 bg-purple-50 font-bold' : 'text-purple-700 hover:bg-purple-50/70'
                }`}
              >
                <Shield className="w-4 h-4 text-purple-600" />
                Admin Panel
              </Link>
            )}
          </nav>

          {/* Right Action Icons */}
          <div className="flex items-center gap-3">
            {/* Quick Admin link if not admin yet to allow easy testing */}
            <Link
              to="/admin"
              className="hidden lg:flex items-center gap-1 px-2.5 py-1 text-xs font-semibold text-slate-600 hover:text-indigo-600 bg-slate-100 hover:bg-indigo-50 rounded-md border border-slate-200 transition-colors"
              title="Open Admin Dashboard"
            >
              <Shield className="w-3.5 h-3.5 text-purple-600" />
              Admin
            </Link>

            {/* Cart Button */}
            <Link
              to="/cart"
              className="relative p-2.5 text-slate-700 hover:text-indigo-600 hover:bg-slate-100 rounded-xl transition-all"
              aria-label="View shopping cart"
            >
              <ShoppingBag className="w-5 h-5" />
              {cartCount > 0 && (
                <span className="absolute -top-0.5 -right-0.5 bg-indigo-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shadow-sm animate-pulse">
                  {cartCount}
                </span>
              )}
            </Link>

            {/* Auth / Profile button */}
            {user ? (
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 border border-slate-200 rounded-xl text-xs font-medium text-slate-800">
                  <div className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-[11px]">
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                  <div className="hidden sm:block text-left">
                    <p className="font-semibold leading-tight line-clamp-1">{user.name}</p>
                    <span className="text-[10px] text-slate-500 uppercase tracking-wider">{user.role}</span>
                  </div>
                </div>
                <button
                  onClick={logout}
                  className="px-2.5 py-1.5 text-xs text-rose-600 hover:bg-rose-50 rounded-lg transition-colors font-medium border border-rose-200/50"
                >
                  Logout
                </button>
              </div>
            ) : (
              <button
                onClick={() => setIsAuthModalOpen(true)}
                className="flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow-sm transition-all"
              >
                <UserIcon className="w-4 h-4" />
                <span>Sign In</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
