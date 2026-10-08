import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  Laptop,
  Smartphone,
  Headphones,
  Keyboard,
  Monitor,
  Watch,
  Tablet,
  Mouse,
  TrendingUp,
  Flame,
  CheckCircle2,
  RefreshCw,
  Shirt,
  Footprints,
  Tv,
  Armchair,
  Home,
  Package
} from 'lucide-react';
import { AISearchBar } from '../components/AISearchBar';
import { ProductCard } from '../components/ProductCard';
import { Product, AISearchResponse } from '../types';
import { api } from '../services/api';
import { useApp } from '../context/AppContext';

export const HomePage: React.FC = () => {
  const { viewedProductIds } = useApp();
  const [aiResult, setAiResult] = useState<AISearchResponse | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [popularProducts, setPopularProducts] = useState<Product[]>([]);
  const [recommendedProducts, setRecommendedProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<{ name: string; count: number }[]>([]);
  const [loadingInitial, setLoadingInitial] = useState(true);

  useEffect(() => {
    const loadHomeData = async () => {
      try {
        const [popular, categoriesData] = await Promise.all([
          api.getProducts({ sort: 'rating_desc' }),
          api.getCategories(),
        ]);
        setPopularProducts(popular.slice(0, 8));
        setCategories(categoriesData);

        // Load initial recommendations
        const recs = await api.getRecommendations(viewedProductIds);
        setRecommendedProducts(recs.slice(0, 4));
      } catch (err) {
        console.error('Error loading home data:', err);
      } finally {
        setLoadingInitial(false);
      }
    };

    loadHomeData();
  }, []);

  // Category Icon Mapper
  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Laptops': return Laptop;
      case 'Smartphones': return Smartphone;
      case 'Headphones': return Headphones;
      case 'Clothing': return Shirt;
      case 'Shoes': return Footprints;
      case 'Refrigerators': return Home;
      case 'Televisions': return Tv;
      case 'Furniture': return Armchair;
      case 'Computer Accessories': return Mouse;
      case 'Home Appliances': return Home;
      case 'Keyboards': return Keyboard;
      case 'Monitors': return Monitor;
      case 'Smartwatches': return Watch;
      case 'Tablets': return Tablet;
      default: return Package;
    }
  };

  return (
    <div className="space-y-16 pb-12">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-16 md:pt-16 md:pb-24 bg-gradient-to-b from-indigo-50/70 via-slate-50 to-white border-b border-slate-200/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-100/80 border border-indigo-200 text-indigo-800 text-xs font-bold tracking-wide uppercase mb-6 shadow-xs animate-bounce">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            AI-Driven Semantic Search & Real-Time Inventory
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-black text-slate-900 tracking-tight leading-tight max-w-4xl mx-auto">
            Search smarter.{' '}
            <span className="bg-gradient-to-r from-indigo-600 via-indigo-700 to-purple-600 bg-clip-text text-transparent">
              Shop smarter.
            </span>
          </h1>

          <p className="mt-4 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Tell us what you need. ShopAI understands your intent and finds the right products from live inventory.
          </p>

          {/* AI Search Box */}
          <div className="mt-8 sm:mt-10">
            <AISearchBar
              onSearchComplete={setAiResult}
              isLoading={isSearching}
              setIsLoading={setIsSearching}
            />
          </div>
        </div>

        {/* Decorative backdrop glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-indigo-400/10 blur-[100px] pointer-events-none rounded-full" />
      </section>

      {/* AI Search Results Section (Renders immediately when query executed) */}
      {aiResult && (
        <section id="ai-results" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 pb-4 border-b border-slate-200">
            <div>
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-indigo-600" />
                <h2 className="text-2xl font-black text-slate-900">
                  ShopAI Recommendations
                </h2>
              </div>
              <p className="text-sm text-slate-500 mt-1">
                Showing {aiResult.products.length} live in-stock match(es) for "{aiResult.query}"
              </p>
            </div>

            <button
              onClick={() => setAiResult(null)}
              className="text-xs font-semibold text-slate-500 hover:text-slate-800 self-start sm:self-auto px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 transition-colors"
            >
              Clear AI Results
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {aiResult.products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                highlightReasons={true}
              />
            ))}
          </div>
        </section>
      )}

      {/* Categories Browse Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-black text-slate-900 tracking-tight">Browse Categories</h2>
            <p className="text-xs text-slate-500 mt-0.5">Explore 30+ verified devices with live stock counts</p>
          </div>
          <Link
            to="/discover"
            className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
          >
            View All →
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3 sm:gap-4">
          {categories.map((cat) => {
            const Icon = getCategoryIcon(cat.name);
            return (
              <Link
                key={cat.name}
                to={`/discover?category=${encodeURIComponent(cat.name)}`}
                className="group p-4 bg-white rounded-2xl border border-slate-200/80 hover:border-indigo-400 hover:shadow-lg hover:shadow-indigo-500/5 transition-all text-center flex flex-col items-center justify-center gap-2"
              >
                <div className="w-12 h-12 rounded-xl bg-indigo-50 group-hover:bg-indigo-600 text-indigo-600 group-hover:text-white flex items-center justify-center transition-all duration-300">
                  <Icon className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xs font-bold text-slate-800 group-hover:text-indigo-600 transition-colors">
                    {cat.name}
                  </h3>
                  <span className="text-[10px] text-slate-400">
                    {cat.count} items
                  </span>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Recommended For You Section */}
      {recommendedProducts.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-indigo-50/50 via-purple-50/40 to-slate-50 p-6 sm:p-8 rounded-3xl border border-indigo-100">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-indigo-600 text-white rounded-xl shadow-xs">
                  <TrendingUp className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-2xl font-black text-slate-900 tracking-tight">
                    Recommended For You
                  </h2>
                  <p className="text-xs text-slate-600">
                    Personalized based on current inventory, ratings, and browsing interest.
                  </p>
                </div>
              </div>

              <Link
                to="/discover"
                className="text-xs font-bold text-indigo-600 hover:text-indigo-800 self-start sm:self-auto"
              >
                Explore More →
              </Link>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {recommendedProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Popular Products Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <Flame className="w-6 h-6 text-amber-500 fill-amber-500" />
            <div>
              <h2 className="text-2xl font-black text-slate-900 tracking-tight">
                Popular Products
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">Top-rated tech devices ready for delivery</p>
            </div>
          </div>
          <Link
            to="/discover"
            className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
          >
            See All Products →
          </Link>
        </div>

        {loadingInitial ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-white rounded-2xl h-80 border border-slate-200 animate-pulse p-4 flex flex-col justify-between">
                <div className="bg-slate-100 rounded-xl h-44 w-full" />
                <div className="space-y-2 mt-4">
                  <div className="h-4 bg-slate-100 rounded w-3/4" />
                  <div className="h-3 bg-slate-100 rounded w-1/2" />
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {popularProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </section>

      {/* Why Choose ShopAI Trust Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-8 bg-slate-900 text-white rounded-3xl border border-slate-800 shadow-xl">
          <div className="flex items-start gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0 border border-indigo-500/30">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-base font-bold text-white mb-1">Intent-Based Search</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Queries are parsed by category, maximum budget, use cases, and hardware features rather than basic keyword lookups.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0 border border-emerald-500/30">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-base font-bold text-white mb-1">Live Stock Guarantees</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                ShopAI never recommends items with zero inventory and automatically recommends in-stock alternatives.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center shrink-0 border border-purple-500/30">
              <RefreshCw className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-base font-bold text-white mb-1">Instant Demo Checkout</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Place orders with Cash on Delivery or Demo Card. Stocks decrement atomically and reflect on the Admin Dashboard.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
