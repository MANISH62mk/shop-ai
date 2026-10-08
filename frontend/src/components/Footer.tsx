import React from 'react';
import { Sparkles, Cpu, ShieldCheck, Heart } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 border-t border-slate-800 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand info */}
          <div className="space-y-4 md:col-span-1">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
                <Sparkles className="w-4 h-4 text-amber-300" />
              </div>
              <span className="text-xl font-bold tracking-tight text-white">
                SHOP<span className="text-indigo-400">AI</span>
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              AI-Powered E-Commerce Assistant featuring natural language semantic search, live inventory verification, and automated stock deductions.
            </p>
            <div className="flex items-center gap-2 text-xs text-indigo-400 bg-slate-800/80 p-2.5 rounded-lg border border-slate-700">
              <Cpu className="w-4 h-4 text-indigo-400 shrink-0" />
              <span>FastAPI Semantic Engine + SQLite</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold text-white tracking-wider uppercase mb-3">Explore</h4>
            <ul className="space-y-2 text-xs">
              <li><Link to="/" className="hover:text-white transition-colors">Home & AI Search</Link></li>
              <li><Link to="/discover" className="hover:text-white transition-colors">Product Catalog</Link></li>
              <li><Link to="/cart" className="hover:text-white transition-colors">Shopping Cart</Link></li>
              <li><Link to="/orders" className="hover:text-white transition-colors">Order Tracking</Link></li>
            </ul>
          </div>

          {/* Admin & System */}
          <div>
            <h4 className="text-sm font-semibold text-white tracking-wider uppercase mb-3">Management</h4>
            <ul className="space-y-2 text-xs">
              <li><Link to="/admin" className="hover:text-white transition-colors">Admin Dashboard</Link></li>
              <li><Link to="/admin" className="hover:text-white transition-colors">Live Inventory Editor</Link></li>
              <li><Link to="/admin" className="hover:text-white transition-colors">CSV Inventory Import</Link></li>
              <li><Link to="/admin" className="hover:text-white transition-colors">Sales & Revenue Analytics</Link></li>
            </ul>
          </div>

          {/* College Project Details */}
          <div>
            <h4 className="text-sm font-semibold text-white tracking-wider uppercase mb-3">College Mini-Project</h4>
            <div className="space-y-2 text-xs text-slate-400">
              <div className="flex items-center gap-1.5 text-emerald-400 font-medium">
                <ShieldCheck className="w-4 h-4" />
                <span>Fully Functional Full-Stack System</span>
              </div>
              <p>Demo Payments: Cash on Delivery & Simulated Card</p>
              <p>Realistic Indian Rupee (₹ INR) seed catalog</p>
              <p className="text-[11px] text-slate-500 pt-2">
                Tech: React 19 + TypeScript + Tailwind CSS + FastAPI + SQLite
              </p>
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© 2026 SHOPAI. Built with precision for college mini-project demonstration.</p>
          <p className="flex items-center gap-1 mt-2 sm:mt-0">
            Engineered with <Heart className="w-3.5 h-3.5 text-rose-500 inline fill-rose-500" /> for semantic e-commerce.
          </p>
        </div>
      </div>
    </footer>
  );
};
