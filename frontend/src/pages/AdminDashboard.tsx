import React, { useState, useEffect } from 'react';
import {
  Shield,
  Package,
  ShoppingCart,
  IndianRupee,
  AlertTriangle,
  TrendingUp,
  Plus,
  Edit2,
  Trash2,
  UploadCloud,
  FileSpreadsheet,
  Download,
  CheckCircle2,
  X,
  Search,
  RefreshCw,
  ExternalLink,
  Layers,
  BarChart3
} from 'lucide-react';
import {
  AdminStats,
  AdminAnalytics,
  Product,
  Order,
  CSVImportResult
} from '../types';
import { api } from '../services/api';
import { useApp } from '../context/AppContext';

export const AdminDashboard: React.FC = () => {
  const { showToast } = useApp();

  const [activeTab, setActiveTab] = useState<'analytics' | 'products' | 'inventory' | 'orders' | 'csv'>('analytics');
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [analytics, setAnalytics] = useState<AdminAnalytics | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  // Search in products / inventory
  const [productSearch, setProductSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  // Add / Edit Product Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    category: 'Laptops',
    brand: '',
    price: 0,
    stock_quantity: 10,
    description: '',
    tags: '',
    image_url: 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=600&auto=format&fit=crop&q=80',
    specs: '{}',
  });

  // CSV State
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [csvPreview, setCsvPreview] = useState<string[][]>([]);
  const [csvImportResult, setCsvImportResult] = useState<CSVImportResult | null>(null);
  const [csvImporting, setCsvImporting] = useState(false);

  // Inline Stock Edit State
  const [editingStockId, setEditingStockId] = useState<number | null>(null);
  const [tempStockValue, setTempStockValue] = useState<number>(0);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [analyticsData, productsData, ordersData] = await Promise.all([
        api.getAdminAnalytics(),
        api.getProducts(),
        api.getOrders(),
      ]);
      setAnalytics(analyticsData);
      setStats(analyticsData.stats);
      setProducts(productsData);
      setOrders(ordersData);
    } catch (err) {
      console.error('Failed to load admin data:', err);
      showToast('Error loading admin metrics', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Filtered products list
  const filteredProducts = products.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(productSearch.toLowerCase()) ||
      p.brand.toLowerCase().includes(productSearch.toLowerCase()) ||
      p.category.toLowerCase().includes(productSearch.toLowerCase());
    const matchesCat = selectedCategory === 'All' || p.category === selectedCategory;
    return matchesSearch && matchesCat;
  });

  // Handle Quick Stock Update
  const handleStockUpdate = async (productId: number, newStock: number) => {
    try {
      await api.updateProductStock(productId, newStock);
      showToast(`Stock updated to ${newStock} for item #${productId}`, 'success');
      // Update local state
      setProducts((prev) =>
        prev.map((p) => (p.id === productId ? { ...p, stock_quantity: newStock } : p))
      );
      setEditingStockId(null);
      // Refresh stats
      const newStats = await api.getAdminStats();
      setStats(newStats);
    } catch (err: any) {
      showToast(err.message || 'Failed to update stock', 'error');
    }
  };

  // Handle Add/Edit product submit
  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingProduct) {
        await api.updateProduct(editingProduct.id, formData);
        showToast(`Product '${formData.name}' updated!`, 'success');
      } else {
        await api.createProduct(formData);
        showToast(`Product '${formData.name}' added to catalog!`, 'success');
      }
      setIsModalOpen(false);
      setEditingProduct(null);
      fetchDashboardData();
    } catch (err: any) {
      showToast(err.message || 'Failed to save product', 'error');
    }
  };

  const handleOpenEdit = (p: Product) => {
    setEditingProduct(p);
    setFormData({
      name: p.name,
      category: p.category,
      brand: p.brand,
      price: p.price,
      stock_quantity: p.stock_quantity,
      description: p.description,
      tags: p.tags,
      image_url: p.image_url,
      specs: p.specs || '{}',
    });
    setIsModalOpen(true);
  };

  const handleOpenAdd = () => {
    setEditingProduct(null);
    setFormData({
      name: '',
      category: 'Laptops',
      brand: '',
      price: 49990,
      stock_quantity: 10,
      description: '',
      tags: 'coding, student, fast',
      image_url: 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=600&auto=format&fit=crop&q=80',
      specs: '{"Processor": "Intel Core i5", "RAM": "16 GB", "Storage": "512 GB SSD"}',
    });
    setIsModalOpen(true);
  };

  const handleDeleteProduct = async (productId: number, productName: string) => {
    if (!window.confirm(`Are you sure you want to delete '${productName}'?`)) return;
    try {
      await api.deleteProduct(productId);
      showToast('Product deleted successfully', 'info');
      fetchDashboardData();
    } catch (err: any) {
      showToast(err.message || 'Failed to delete product', 'error');
    }
  };

  // CSV Handling
  const handleCSVFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setCsvFile(file);
    setCsvImportResult(null);

    // Read preview lines
    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      const lines = text.split('\n').filter((l) => l.trim().length > 0);
      const rows = lines.slice(0, 5).map((l) => l.split(','));
      setCsvPreview(rows);
    };
    reader.readAsText(file);
  };

  const handleImportCSV = async () => {
    if (!csvFile) return;
    setCsvImporting(true);
    try {
      const res = await api.importCSV(csvFile);
      setCsvImportResult(res);
      showToast(`Imported ${res.imported_count} products from CSV!`, 'success');
      fetchDashboardData();
    } catch (err: any) {
      showToast(err.message || 'Failed to import CSV', 'error');
    } finally {
      setCsvImporting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-purple-600 text-white flex items-center justify-center shadow-xs">
              <Shield className="w-4 h-4" />
            </div>
            <h1 className="text-3xl font-black text-slate-900 tracking-tight">Admin Operations Center</h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time live inventory management, sales metrics, and CSV product bulk import.
          </p>
        </div>

        <button
          onClick={fetchDashboardData}
          className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors shadow-xs self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Live Data
        </button>
      </div>

      {/* KPI Stats Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {/* Total Products */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Products</span>
            <Package className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{stats?.total_products ?? 0}</div>
          <span className="text-[11px] text-slate-400">In database catalog</span>
        </div>

        {/* Total Orders */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Orders</span>
            <ShoppingCart className="w-4 h-4 text-purple-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{stats?.total_orders ?? 0}</div>
          <span className="text-[11px] text-slate-400">Placed orders</span>
        </div>

        {/* Total Revenue */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Revenue</span>
            <IndianRupee className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">
            ₹{stats?.total_revenue ? stats.total_revenue.toLocaleString('en-IN') : '0'}
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold">Total sales generated</span>
        </div>

        {/* Products Sold */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Units Sold</span>
            <TrendingUp className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{stats?.products_sold ?? 0}</div>
          <span className="text-[11px] text-slate-400">Dispatched units</span>
        </div>

        {/* Low Stock Items */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Low Stock</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-black text-amber-600">{stats?.low_stock_products ?? 0}</div>
          <span className="text-[11px] text-amber-700 font-medium">Stock &lt; 5 units</span>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="border-b border-slate-200 flex items-center gap-2 overflow-x-auto no-scrollbar">
        <button
          onClick={() => setActiveTab('analytics')}
          className={`py-3 px-4 font-bold text-xs sm:text-sm border-b-2 flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'analytics'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <BarChart3 className="w-4 h-4" /> Sales Analytics
        </button>

        <button
          onClick={() => setActiveTab('inventory')}
          className={`py-3 px-4 font-bold text-xs sm:text-sm border-b-2 flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'inventory'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Layers className="w-4 h-4" /> Fast Inventory Editor
        </button>

        <button
          onClick={() => setActiveTab('products')}
          className={`py-3 px-4 font-bold text-xs sm:text-sm border-b-2 flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'products'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Package className="w-4 h-4" /> Product Catalog (CRUD)
        </button>

        <button
          onClick={() => setActiveTab('orders')}
          className={`py-3 px-4 font-bold text-xs sm:text-sm border-b-2 flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'orders'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <ShoppingCart className="w-4 h-4" /> Customer Orders ({orders.length})
        </button>

        <button
          onClick={() => setActiveTab('csv')}
          className={`py-3 px-4 font-bold text-xs sm:text-sm border-b-2 flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'csv'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <FileSpreadsheet className="w-4 h-4" /> CSV Bulk Import
        </button>
      </div>

      {/* TAB 1: SALES ANALYTICS */}
      {activeTab === 'analytics' && analytics && (
        <div className="space-y-8 animate-in fade-in duration-200">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Sales Chart (Clean pure CSS/SVG bar chart) */}
            <div className="lg:col-span-2 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-slate-900">Revenue & Volume Over Time</h3>
                  <p className="text-xs text-slate-400">Actual transaction totals aggregated from SQLite</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-indigo-50 text-indigo-700">
                  Last 7 Days
                </span>
              </div>

              {/* Chart Visualizer */}
              <div className="h-64 flex items-end justify-between gap-3 pt-6 border-b border-slate-100 pb-2">
                {analytics.sales_over_time.map((d, idx) => {
                  const maxRev = Math.max(...analytics.sales_over_time.map((item) => item.revenue), 100000);
                  const heightPercent = Math.max(10, Math.round((d.revenue / maxRev) * 100));

                  return (
                    <div key={idx} className="flex-1 flex flex-col items-center gap-2 group h-full justify-end">
                      <div className="text-[10px] font-bold text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                        ₹{d.revenue.toLocaleString('en-IN')} ({d.orders_count})
                      </div>
                      <div
                        style={{ height: `${heightPercent}%` }}
                        className="w-full bg-gradient-to-t from-indigo-600 to-purple-500 group-hover:from-indigo-500 group-hover:to-purple-400 rounded-t-xl transition-all shadow-xs relative"
                      >
                        {d.orders_count > 0 && (
                          <span className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] font-bold bg-slate-900 text-white px-1 rounded">
                            {d.orders_count}
                          </span>
                        )}
                      </div>
                      <span className="text-[11px] font-semibold text-slate-500">{d.date}</span>
                    </div>
                  );
                })}
              </div>

              <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
                <span className="flex items-center gap-2">
                  <span className="w-3 h-3 bg-indigo-600 rounded" /> Daily Gross Sales
                </span>
                <span>Values generated dynamically from orders table</span>
              </div>
            </div>

            {/* Top Selling Products */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs space-y-4">
              <div>
                <h3 className="text-base font-bold text-slate-900">Top Performing Products</h3>
                <p className="text-xs text-slate-400">Ranked by volume sold</p>
              </div>

              <div className="space-y-3">
                {analytics.top_selling.length === 0 ? (
                  <p className="text-xs text-slate-400 py-6 text-center">No products sold yet</p>
                ) : (
                  analytics.top_selling.map((item, idx) => (
                    <div
                      key={item.product_id}
                      className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between gap-2"
                    >
                      <div className="flex items-center gap-2.5">
                        <span className="w-5 h-5 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold flex items-center justify-center">
                          {idx + 1}
                        </span>
                        <div>
                          <p className="font-bold text-xs text-slate-900 line-clamp-1">{item.product_name}</p>
                          <span className="text-[10px] text-slate-400">{item.category}</span>
                        </div>
                      </div>
                      <div className="text-right shrink-0">
                        <div className="text-xs font-bold text-slate-900">{item.units_sold} units</div>
                        <span className="text-[10px] text-indigo-600 font-semibold">
                          ₹{item.revenue_generated.toLocaleString('en-IN')}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: FAST INVENTORY EDITOR (Crucial for Demo Flow: toggle stock to 0) */}
      {activeTab === 'inventory' && (
        <div className="space-y-6 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs animate-in fade-in duration-200">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-black text-slate-900">Live Inventory Quick Manager</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Quickly adjust stock quantities or set stock to 0 with 1 click to demonstrate AI alternative recommendations.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="Filter inventory..."
                  value={productSearch}
                  onChange={(e) => setProductSearch(e.target.value)}
                  className="pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-300 bg-slate-50"
                />
              </div>

              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="py-1.5 px-3 text-xs rounded-xl border border-slate-300 bg-slate-50"
              >
                <option value="All">All Categories</option>
                <option value="Laptops">Laptops</option>
                <option value="Smartphones">Smartphones</option>
                <option value="Headphones">Headphones</option>
                <option value="Clothing">Clothing</option>
                <option value="Shoes">Shoes</option>
                <option value="Refrigerators">Refrigerators</option>
                <option value="Televisions">Televisions</option>
                <option value="Furniture">Furniture</option>
                <option value="Computer Accessories">Computer Accessories</option>
                <option value="Home Appliances">Home Appliances</option>
                <option value="Keyboards">Keyboards</option>
                <option value="Monitors">Monitors</option>
                <option value="Smartwatches">Smartwatches</option>
                <option value="Tablets">Tablets</option>
                <option value="Accessories">Accessories</option>
              </select>
            </div>
          </div>

          {/* Quick Demo Test Instructions Banner */}
          <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-2xl flex items-start gap-3 text-xs text-indigo-950">
            <Shield className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
            <div>
              <strong className="block text-indigo-900">Phase 11 Demo Tip:</strong>
              Click the red <strong>"Set to 0 (Test Demo)"</strong> button on any laptop (e.g. Acer Swift Go 14).
              Then go back to Home and search <em>"I need a lightweight laptop for coding under ₹60,000"</em>.
              The AI will detect that item is unavailable and automatically recommend in-stock alternatives!
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Product Name</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Price</th>
                  <th className="py-3 px-4">Current Stock</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Quick Stock Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {filteredProducts.map((p) => {
                  const isZero = p.stock_quantity <= 0;
                  const isEditingThis = editingStockId === p.id;

                  return (
                    <tr key={p.id} className="hover:bg-slate-50/70 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-slate-900">
                        <div className="flex items-center gap-2.5">
                          <img
                            src={p.image_url}
                            alt=""
                            className="w-8 h-8 rounded-lg object-cover bg-slate-100 shrink-0"
                          />
                          <span className="line-clamp-1">{p.name}</span>
                        </div>
                      </td>
                      <td className="py-3.5 px-4 text-slate-500">{p.category}</td>
                      <td className="py-3.5 px-4 font-bold text-slate-900">
                        ₹{p.price.toLocaleString('en-IN')}
                      </td>

                      {/* Stock Column with Inline edit */}
                      <td className="py-3.5 px-4">
                        {isEditingThis ? (
                          <div className="flex items-center gap-1.5">
                            <input
                              type="number"
                              min="0"
                              value={tempStockValue}
                              onChange={(e) => setTempStockValue(parseInt(e.target.value) || 0)}
                              className="w-16 px-2 py-1 text-xs border border-indigo-500 rounded bg-white font-bold"
                            />
                            <button
                              onClick={() => handleStockUpdate(p.id, tempStockValue)}
                              className="px-2 py-1 bg-indigo-600 text-white rounded font-bold"
                            >
                              Save
                            </button>
                            <button
                              onClick={() => setEditingStockId(null)}
                              className="px-1.5 py-1 text-slate-400 hover:text-slate-600"
                            >
                              ✕
                            </button>
                          </div>
                        ) : (
                          <button
                            onClick={() => {
                              setEditingStockId(p.id);
                              setTempStockValue(p.stock_quantity);
                            }}
                            className="font-bold text-slate-900 hover:text-indigo-600 underline decoration-dotted text-sm"
                            title="Click to edit stock number"
                          >
                            {p.stock_quantity} units
                          </button>
                        )}
                      </td>

                      <td className="py-3.5 px-4">
                        {isZero ? (
                          <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">
                            Out of Stock
                          </span>
                        ) : p.stock_quantity <= 3 ? (
                          <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">
                            Low ({p.stock_quantity})
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                            In Stock
                          </span>
                        )}
                      </td>

                      {/* Fast Action Buttons */}
                      <td className="py-3.5 px-4 text-right space-x-1.5">
                        <button
                          onClick={() => handleStockUpdate(p.id, 0)}
                          className="px-2.5 py-1 text-[11px] font-bold text-rose-600 hover:bg-rose-50 border border-rose-200 rounded-lg transition-colors"
                          title="Set stock to 0 to test out-of-stock alternative recommendation"
                        >
                          Set to 0 (Test Demo)
                        </button>

                        <button
                          onClick={() => handleStockUpdate(p.id, p.stock_quantity + 5)}
                          className="px-2.5 py-1 text-[11px] font-bold text-indigo-600 hover:bg-indigo-50 border border-indigo-200 rounded-lg transition-colors"
                        >
                          +5 Stock
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 3: PRODUCTS CRUD */}
      {activeTab === 'products' && (
        <div className="space-y-6 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs animate-in fade-in duration-200">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-black text-slate-900">Manage Catalog Products</h3>
              <p className="text-xs text-slate-500 mt-0.5">Add new items, update prices, specs, and descriptions.</p>
            </div>

            <button
              onClick={handleOpenAdd}
              className="flex items-center gap-1.5 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold shadow-md shadow-indigo-500/20 transition-all self-start sm:self-auto"
            >
              <Plus className="w-4 h-4" /> Add New Product
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Name</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Brand</th>
                  <th className="py-3 px-4">Price</th>
                  <th className="py-3 px-4">Stock</th>
                  <th className="py-3 px-4">Rating</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {filteredProducts.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-3.5 px-4 font-bold text-slate-900">
                      <div className="flex items-center gap-2.5">
                        <img
                          src={p.image_url}
                          alt=""
                          className="w-8 h-8 rounded-lg object-cover bg-slate-100 shrink-0"
                        />
                        <span className="line-clamp-1">{p.name}</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-500">{p.category}</td>
                    <td className="py-3.5 px-4 font-semibold text-slate-700">{p.brand}</td>
                    <td className="py-3.5 px-4 font-bold text-slate-900">
                      ₹{p.price.toLocaleString('en-IN')}
                    </td>
                    <td className="py-3.5 px-4 font-bold text-slate-800">{p.stock_quantity}</td>
                    <td className="py-3.5 px-4">{p.rating} ★</td>
                    <td className="py-3.5 px-4 text-right space-x-2">
                      <button
                        onClick={() => handleOpenEdit(p)}
                        className="p-1.5 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                        title="Edit Product"
                      >
                        <Edit2 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleDeleteProduct(p.id, p.name)}
                        className="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                        title="Delete Product"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 4: ORDERS LIST */}
      {activeTab === 'orders' && (
        <div className="space-y-6 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs animate-in fade-in duration-200">
          <div>
            <h3 className="text-lg font-black text-slate-900">Customer Orders Register</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Live record of orders placed via checkout with deducted line items.
            </p>
          </div>

          <div className="divide-y divide-slate-100">
            {orders.map((o) => (
              <div key={o.id} className="py-4 space-y-2 text-xs">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-900 font-mono text-sm">#ORD-{o.id}</span>
                    <span className="text-slate-500">• {o.customer_name} ({o.customer_email})</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-black text-slate-900 text-sm">
                      ₹{o.total_amount.toLocaleString('en-IN')}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      {o.status}
                    </span>
                  </div>
                </div>

                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <div className="text-[11px] font-semibold text-slate-500 mb-1">
                    Purchased Items:
                  </div>
                  <ul className="space-y-1">
                    {o.items.map((i) => (
                      <li key={i.id} className="flex justify-between text-slate-700">
                        <span>• {i.product_name} (x{i.quantity})</span>
                        <span className="font-bold">₹{i.subtotal.toLocaleString('en-IN')}</span>
                      </li>
                    ))}
                  </ul>
                  <div className="mt-2 pt-2 border-t border-slate-200/60 text-[10px] text-slate-400 flex justify-between">
                    <span>Address: {o.shipping_address}</span>
                    <span>Method: {o.payment_method}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 5: CSV BULK IMPORT */}
      {activeTab === 'csv' && (
        <div className="space-y-6 bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/80 shadow-xs animate-in fade-in duration-200">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-black text-slate-900">CSV Inventory Bulk Import</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Upload CSV files to batch import new inventory directly into SQLite.
              </p>
            </div>

            <a
              href={api.getSampleCSVUrl()}
              download="shopai_sample.csv"
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-xl transition-colors border border-indigo-200/60"
            >
              <Download className="w-3.5 h-3.5" /> Download Sample CSV Template
            </a>
          </div>

          {/* Upload Area */}
          <div className="border-2 border-dashed border-slate-300 hover:border-indigo-500 rounded-3xl p-8 text-center transition-colors bg-slate-50/50">
            <UploadCloud className="w-12 h-12 text-indigo-500 mx-auto mb-3" />
            <p className="text-sm font-bold text-slate-800">
              Drag & drop your CSV file here, or click to browse
            </p>
            <p className="text-xs text-slate-400 mt-1 mb-4">
              Required columns: name, category, brand, price, stock_quantity, description
            </p>
            <input
              type="file"
              accept=".csv"
              onChange={handleCSVFileChange}
              className="text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-indigo-600 file:text-white hover:file:bg-indigo-700 cursor-pointer"
            />
          </div>

          {/* CSV File Preview Table */}
          {csvPreview.length > 0 && (
            <div className="space-y-3 pt-4">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Preview Data (First 5 Rows)
              </h4>
              <div className="overflow-x-auto border border-slate-200 rounded-2xl">
                <table className="w-full text-left text-xs">
                  <tbody className="divide-y divide-slate-100">
                    {csvPreview.map((row, rIdx) => (
                      <tr key={rIdx} className={rIdx === 0 ? 'bg-slate-100 font-bold' : ''}>
                        {row.map((cell, cIdx) => (
                          <td key={cIdx} className="py-2 px-3 truncate max-w-xs">
                            {cell}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <button
                onClick={handleImportCSV}
                disabled={csvImporting}
                className="py-3 px-6 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white rounded-xl text-xs font-bold shadow-md shadow-indigo-500/20 transition-all flex items-center gap-2"
              >
                {csvImporting ? (
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <CheckCircle2 className="w-4 h-4" />
                )}
                <span>Confirm & Import Products</span>
              </button>
            </div>
          )}

          {/* Import Result Notification */}
          {csvImportResult && (
            <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-emerald-800 text-xs space-y-1">
              <p className="font-bold">
                ✓ Successfully imported {csvImportResult.imported_count} products into the catalog!
              </p>
              {csvImportResult.failed_count > 0 && (
                <p className="text-rose-600">
                  {csvImportResult.failed_count} row(s) had errors. Check headers and data types.
                </p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Add / Edit Product Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs animate-in fade-in duration-150">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setIsModalOpen(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <h3 className="text-xl font-black text-slate-900 mb-1">
              {editingProduct ? 'Edit Catalog Product' : 'Add New Product'}
            </h3>
            <p className="text-xs text-slate-500 mb-6">
              Enter product specifications, inventory count, and pricing.
            </p>

            <form onSubmit={handleFormSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Product Name</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl"
                  placeholder="e.g. Dell XPS 13 Ultrabook"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Category</label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl bg-white"
                  >
                    <option value="Laptops">Laptops</option>
                    <option value="Smartphones">Smartphones</option>
                    <option value="Headphones">Headphones</option>
                    <option value="Clothing">Clothing</option>
                    <option value="Shoes">Shoes</option>
                    <option value="Refrigerators">Refrigerators</option>
                    <option value="Televisions">Televisions</option>
                    <option value="Furniture">Furniture</option>
                    <option value="Computer Accessories">Computer Accessories</option>
                    <option value="Home Appliances">Home Appliances</option>
                    <option value="Keyboards">Keyboards</option>
                    <option value="Monitors">Monitors</option>
                    <option value="Smartwatches">Smartwatches</option>
                    <option value="Tablets">Tablets</option>
                    <option value="Accessories">Accessories</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Brand</label>
                  <input
                    type="text"
                    required
                    value={formData.brand}
                    onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
                    className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl"
                    placeholder="e.g. Dell"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Price (₹ INR)</label>
                  <input
                    type="number"
                    required
                    min="0"
                    value={formData.price}
                    onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) || 0 })}
                    className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl font-mono"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Initial Stock</label>
                  <input
                    type="number"
                    required
                    min="0"
                    value={formData.stock_quantity}
                    onChange={(e) => setFormData({ ...formData, stock_quantity: parseInt(e.target.value) || 0 })}
                    className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Description</label>
                <textarea
                  rows={2}
                  required
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl"
                  placeholder="Comprehensive description for semantic search..."
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Search Tags</label>
                <input
                  type="text"
                  value={formData.tags}
                  onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                  className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl"
                  placeholder="coding, programming, lightweight, oled..."
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Image URL</label>
                <input
                  type="url"
                  required
                  value={formData.image_url}
                  onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                  className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl text-slate-600"
                />
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  className="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold shadow-md transition-all"
                >
                  {editingProduct ? 'Update Product' : 'Add Product'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
