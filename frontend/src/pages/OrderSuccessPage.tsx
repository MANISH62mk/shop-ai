import React, { useState, useEffect } from 'react';
import { useParams, useLocation, Link, useNavigate } from 'react-router-dom';
import { CheckCircle2, ArrowRight, Package, Shield, ExternalLink, Sparkles } from 'lucide-react';
import { Order } from '../types';
import { api } from '../services/api';

export const OrderSuccessPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const navigate = useNavigate();

  const [order, setOrder] = useState<Order | null>(
    (location.state as any)?.order || null
  );
  const [loading, setLoading] = useState(!order);

  useEffect(() => {
    if (!order && id) {
      const orderId = parseInt(id, 10);
      if (!isNaN(orderId)) {
        api.getOrderById(orderId)
          .then(setOrder)
          .catch((err) => console.error(err))
          .finally(() => setLoading(false));
      }
    }
  }, [id, order]);

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        <div className="w-8 h-8 border-4 border-indigo-600/30 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4" />
        <p className="text-sm text-slate-500">Retrieving order details...</p>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center space-y-4">
        <h2 className="text-2xl font-bold text-slate-900">Order not found</h2>
        <Link to="/" className="text-sm font-bold text-indigo-600">Return Home</Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12 space-y-8 animate-in fade-in duration-300">
      {/* Success Card Header */}
      <div className="text-center space-y-3">
        <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-3xl mx-auto flex items-center justify-center shadow-lg shadow-emerald-500/10">
          <CheckCircle2 className="w-10 h-10" />
        </div>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">
          Demo Order Confirmed!
        </h1>
        <p className="text-sm text-slate-600">
          Thank you, <strong className="text-slate-900">{order.customer_name}</strong>. Your order has been placed in the database.
        </p>
      </div>

      {/* Stock Decrement Verification Banner */}
      <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-2xl flex items-start gap-3 text-indigo-900 text-xs sm:text-sm">
        <Sparkles className="w-5 h-5 text-indigo-600 shrink-0 mt-0.5" />
        <div>
          <p className="font-bold text-indigo-950 mb-0.5">Automated Inventory Update Verified</p>
          <p className="text-indigo-800 leading-relaxed">
            Product stocks have automatically decreased in the SQLite database, and the Admin Dashboard now reflects the updated revenue, orders count, and inventory quantities.
          </p>
        </div>
      </div>

      {/* Order Summary Details Box */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-md p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-4">
          <div>
            <span className="text-xs text-slate-400 font-medium">Order Reference ID</span>
            <div className="text-lg font-black text-slate-900 font-mono">#ORD-{order.id}</div>
          </div>
          <div className="sm:text-right">
            <span className="text-xs text-slate-400 font-medium">Status</span>
            <div className="inline-block sm:block px-2.5 py-0.5 text-xs font-bold rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200">
              {order.status}
            </div>
          </div>
        </div>

        {/* Ordered Items List */}
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
            Items Ordered
          </h3>
          <div className="divide-y divide-slate-100">
            {order.items.map((item) => (
              <div key={item.id} className="py-3 flex items-center justify-between text-xs sm:text-sm">
                <div>
                  <p className="font-bold text-slate-900">{item.product_name}</p>
                  <p className="text-slate-500 text-xs">Qty: {item.quantity} × ₹{item.unit_price.toLocaleString('en-IN')}</p>
                </div>
                <span className="font-black text-slate-900">
                  ₹{item.subtotal.toLocaleString('en-IN')}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Metadata Details */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-100 text-xs">
          <div>
            <span className="font-semibold text-slate-400 block mb-1">Delivery Address</span>
            <p className="text-slate-700">{order.shipping_address}</p>
            <p className="text-slate-500 mt-1">Phone: {order.customer_phone}</p>
          </div>
          <div>
            <span className="font-semibold text-slate-400 block mb-1">Payment Method</span>
            <p className="font-bold text-slate-900">{order.payment_method}</p>
            <span className="font-semibold text-slate-400 block mt-2 mb-0.5">Total Amount Paid</span>
            <span className="text-xl font-black text-indigo-600">₹{order.total_amount.toLocaleString('en-IN')}</span>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row items-center gap-3">
        <Link
          to="/admin"
          className="w-full sm:w-1/2 py-3.5 px-6 rounded-2xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs sm:text-sm shadow-md shadow-purple-500/20 text-center flex items-center justify-center gap-2 transition-all"
        >
          <Shield className="w-4 h-4" />
          <span>Verify in Admin Dashboard</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </Link>

        <Link
          to="/orders"
          className="w-full sm:w-1/2 py-3.5 px-6 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs sm:text-sm shadow-md text-center flex items-center justify-center gap-2 transition-all"
        >
          <Package className="w-4 h-4" />
          <span>View All Orders</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
};
