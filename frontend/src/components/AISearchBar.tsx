import React, { useState } from 'react';
import { Sparkles, Search, ArrowRight, CornerDownLeft, AlertTriangle } from 'lucide-react';
import { AISearchResponse } from '../types';
import { api } from '../services/api';

interface AISearchBarProps {
  onSearchComplete: (data: AISearchResponse | null) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  initialQuery?: string;
}

export const AISearchBar: React.FC<AISearchBarProps> = ({
  onSearchComplete,
  isLoading,
  setIsLoading,
  initialQuery = '',
}) => {
  const [query, setQuery] = useState(initialQuery);
  const [lastResponse, setLastResponse] = useState<AISearchResponse | null>(null);

  const sampleQueries = [
    'I need a laptop for coding under ₹60,000',
    'Show me cotton shirts under ₹1,500',
    'Double door refrigerator under ₹40,000',
    'Best running shoes under ₹3,000',
    'Phone with good camera under ₹30,000',
    'Gaming headphones',
    'Office chair under ₹8,000',
  ];

  const handleSearch = async (textToSearch?: string) => {
    const q = (textToSearch !== undefined ? textToSearch : query).trim();
    if (!q) return;

    if (textToSearch !== undefined) {
      setQuery(textToSearch);
    }

    setIsLoading(true);
    try {
      const result = await api.searchAI(q);
      setLastResponse(result);
      onSearchComplete(result);
    } catch (err) {
      console.error('AI Search failed:', err);
      onSearchComplete(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Search Input Box */}
      <div className="relative group bg-white p-2 sm:p-2.5 rounded-2xl sm:rounded-3xl shadow-xl shadow-indigo-600/10 border-2 border-indigo-200/80 focus-within:border-indigo-600 focus-within:ring-4 focus-within:ring-indigo-500/10 transition-all">
        <div className="flex items-center gap-3 pl-3 sm:pl-4">
          <Sparkles className="w-6 h-6 text-indigo-600 shrink-0 animate-pulse" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Tell ShopAI what you need (e.g. 'I need a lightweight laptop for coding under ₹60,000')..."
            className="w-full py-2.5 text-sm sm:text-base text-slate-800 placeholder-slate-400 bg-transparent focus:outline-none"
          />

          <button
            onClick={() => handleSearch()}
            disabled={isLoading || !query.trim()}
            className="flex items-center gap-2 px-5 sm:px-6 py-3 sm:py-3.5 bg-gradient-to-r from-indigo-600 via-indigo-700 to-purple-600 hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 text-white font-bold text-sm rounded-xl sm:rounded-2xl shadow-md shadow-indigo-500/25 transition-all shrink-0 active:scale-95"
          >
            {isLoading ? (
              <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <span>Ask ShopAI</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Quick Prompts Pills */}
      <div className="mt-3.5 flex flex-wrap items-center gap-1.5 sm:gap-2">
        <span className="text-xs font-semibold text-slate-400 flex items-center gap-1">
          <CornerDownLeft className="w-3.5 h-3.5 text-indigo-500" /> Try:
        </span>
        {sampleQueries.map((item, idx) => (
          <button
            key={idx}
            onClick={() => handleSearch(item)}
            className="text-xs font-medium px-3 py-1.5 rounded-xl bg-white/80 hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 border border-slate-200/80 hover:border-indigo-300 transition-all shadow-xs"
          >
            {item}
          </button>
        ))}
      </div>

      {/* AI Reasoning & Intent Display Banner */}
      {lastResponse && (
        <div className="mt-6 p-5 sm:p-6 bg-gradient-to-r from-indigo-950 via-slate-900 to-purple-950 rounded-2xl text-white shadow-xl border border-indigo-500/30 animate-in fade-in duration-300">
          {/* Out of Stock Alert Banner if triggered */}
          {lastResponse.out_of_stock_alert && (
            <div className="mb-4 p-3.5 bg-amber-500/20 border border-amber-400/40 rounded-xl flex items-start gap-2.5 text-amber-200 text-xs sm:text-sm">
              <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-amber-300 mb-0.5">Live Inventory Alert</p>
                <p>{lastResponse.out_of_stock_alert}</p>
              </div>
            </div>
          )}

          {/* Assistant Voice Message */}
          <div className="flex items-start gap-3 mb-4">
            <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center shrink-0 shadow-md">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-300">
                ShopAI Reasoning Assistant
              </span>
              <p className="text-base sm:text-lg font-medium text-slate-100 mt-0.5">
                "{lastResponse.response_message}"
              </p>
            </div>
          </div>

          {/* Extracted Intent Chips */}
          <div className="pt-3 border-t border-indigo-800/60 flex flex-wrap items-center gap-2 text-xs">
            <span className="text-indigo-300 font-semibold mr-1">Extracted Intent:</span>

            {lastResponse.extracted_intent.category && (
              <span className="px-2.5 py-1 rounded-lg bg-indigo-800/60 text-indigo-200 border border-indigo-600/40">
                📁 Category: <strong className="text-white">{lastResponse.extracted_intent.category}</strong>
              </span>
            )}

            {lastResponse.extracted_intent.max_budget && (
              <span className="px-2.5 py-1 rounded-lg bg-emerald-900/60 text-emerald-200 border border-emerald-600/40">
                💰 Max Budget: <strong className="text-white">₹{lastResponse.extracted_intent.max_budget.toLocaleString('en-IN')}</strong>
              </span>
            )}

            {lastResponse.extracted_intent.use_case && (
              <span className="px-2.5 py-1 rounded-lg bg-purple-800/60 text-purple-200 border border-purple-600/40">
                🎯 Use Case: <strong className="text-white">{lastResponse.extracted_intent.use_case}</strong>
              </span>
            )}

            {lastResponse.extracted_intent.brand && (
              <span className="px-2.5 py-1 rounded-lg bg-blue-800/60 text-blue-200 border border-blue-600/40">
                🏷️ Brand: <strong className="text-white">{lastResponse.extracted_intent.brand}</strong>
              </span>
            )}

            {lastResponse.extracted_intent.keywords.length > 0 && (
              <span className="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 border border-slate-700">
                🔍 Keywords: {lastResponse.extracted_intent.keywords.join(', ')}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
