import React, { useState, useEffect } from 'react';
import { Package, Calendar, CreditCard, ChevronRight, ShoppingBag } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Order } from '../types';
import { api } from '../services/api';
import { useApp } from '../context/AppContext';

export const OrdersPage: React.FC = () => {
  const { user } = useApp();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      setLoading(true);
      try {
        const data = await api.getOrders(user ? user.email : undefined);
        setOrders(data);
      } catch (err) {
        console.error('Failed to load orders:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [user]);

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16 text-center">
        <div className="w-8 h-8 border-4 border-indigo-600/30 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4" />
        <p className="text-sm text-slate-500">Loading order history...</p>
      </div>
    );
  }

  if (orders.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="w-16 h-16 bg-slate-100 text-slate-400 rounded-2xl mx-auto flex items-center justify-center">
          <Package className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-black text-slate-900">No orders placed yet</h2>
        <p className="text-xs text-slate-500 max-w-sm mx-auto">
          Explore products or test checkout to see your placed orders and stock deductions live here.
        </p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-xl text-xs font-bold shadow-md hover:bg-indigo-700 transition-colors"
        >
          <ShoppingBag className="w-4 h-4" /> Shop Now
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <div>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Order History</h1>
        <p className="text-xs text-slate-500 mt-1">
          Review placed orders, purchased line items, and delivery status.
        </p>
      </div>

      <div className="space-y-4">
        {orders.map((order) => (
          <div
            key={order.id}
            className="bg-white rounded-2xl border border-slate-200/80 shadow-xs p-5 sm:p-6 space-y-4 hover:border-indigo-200 transition-colors"
          >
            {/* Header info */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
                  <Package className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-900 font-mono text-sm">#ORD-{order.id}</span>
                    <span className="px-2 py-0.5 text-[10px] font-bold rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200">
                      {order.status}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-slate-400 mt-0.5">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {new Date(order.created_at).toLocaleDateString('en-IN', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                      })}
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <CreditCard className="w-3.5 h-3.5" />
                      {order.payment_method}
                    </span>
                  </div>
                </div>
              </div>

              <div className="text-left sm:text-right">
                <span className="text-[10px] text-slate-400 block uppercase">Total Paid</span>
                <span className="text-base sm:text-lg font-black text-slate-900">
                  ₹{order.total_amount.toLocaleString('en-IN')}
                </span>
              </div>
            </div>

            {/* Line items */}
            <div className="divide-y divide-slate-100">
              {order.items.map((item) => (
                <div key={item.id} className="py-2.5 flex items-center justify-between text-xs sm:text-sm">
                  <div className="flex-1 pr-4">
                    <span className="font-bold text-slate-800">{item.product_name}</span>
                    <span className="text-slate-400 ml-2">Qty: {item.quantity}</span>
                  </div>
                  <span className="font-bold text-slate-900">
                    ₹{item.subtotal.toLocaleString('en-IN')}
                  </span>
                </div>
              ))}
            </div>

            {/* Footer details */}
            <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-slate-500 bg-slate-50/80 p-3 rounded-xl border border-slate-100">
              <div>
                <span className="font-semibold text-slate-600">Shipped to: </span>
                <span>{order.customer_name} ({order.shipping_address})</span>
              </div>
              <Link
                to={`/order-success/${order.id}`}
                className="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1 self-start sm:self-auto"
              >
                View Receipt <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
