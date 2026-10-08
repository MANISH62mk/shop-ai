import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingBag, Trash2, ArrowRight, ArrowLeft, ShieldCheck, AlertCircle } from 'lucide-react';
import { useApp } from '../context/AppContext';

export const CartPage: React.FC = () => {
  const { cart, updateCartQuantity, removeFromCart, clearCart } = useApp();
  const navigate = useNavigate();

  if (!cart || cart.items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="w-20 h-20 bg-indigo-50 text-indigo-600 rounded-3xl mx-auto flex items-center justify-center">
          <ShoppingBag className="w-10 h-10" />
        </div>
        <h2 className="text-2xl font-black text-slate-900">Your cart is empty</h2>
        <p className="text-sm text-slate-500 max-w-sm mx-auto">
          You haven't added any items yet. Search with ShopAI or browse our catalog!
        </p>
        <div className="pt-2">
          <Link
            to="/discover"
            className="inline-flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl shadow-md shadow-indigo-500/20 transition-all"
          >
            Start Shopping
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">Shopping Cart</h1>
          <p className="text-xs text-slate-500 mt-1">
            {cart.item_count} items reserved in your session
          </p>
        </div>
        <button
          onClick={clearCart}
          className="text-xs font-semibold text-rose-600 hover:text-rose-700 self-start sm:self-auto flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-rose-200 hover:bg-rose-50 transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" /> Clear Cart
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Cart Item List */}
        <div className="lg:col-span-2 space-y-4">
          {cart.items.map((item) => {
            const product = item.product;
            const isLowStock = product.stock_quantity > 0 && product.stock_quantity <= 3;
            const isOutOfStock = product.stock_quantity <= 0;

            return (
              <div
                key={item.id}
                className="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200/80 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                {/* Image & Title */}
                <div className="flex items-center gap-4 flex-1">
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-20 h-20 sm:w-24 sm:h-24 rounded-xl object-cover bg-slate-100 shrink-0"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src =
                        'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=600&auto=format&fit=crop&q=80';
                    }}
                  />
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                      {product.brand}
                    </span>
                    <Link
                      to={`/product/${product.id}`}
                      className="block font-bold text-sm sm:text-base text-slate-900 hover:text-indigo-600 transition-colors line-clamp-1"
                    >
                      {product.name}
                    </Link>
                    <div className="text-xs text-slate-500 font-medium">
                      Unit Price: ₹{product.price.toLocaleString('en-IN')}
                    </div>

                    {/* Stock Alert */}
                    {isOutOfStock ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-rose-600">
                        <AlertCircle className="w-3 h-3" /> Out of stock! Please remove.
                      </span>
                    ) : isLowStock ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-amber-600">
                        Only {product.stock_quantity} left in stock
                      </span>
                    ) : (
                      <span className="text-[11px] font-medium text-emerald-600">
                        ✓ In Stock ({product.stock_quantity} available)
                      </span>
                    )}
                  </div>
                </div>

                {/* Quantity Controls & Line Total */}
                <div className="flex items-center justify-between sm:justify-end gap-6 w-full sm:w-auto pt-3 sm:pt-0 border-t sm:border-0 border-slate-100">
                  {/* Quantity picker */}
                  <div className="flex items-center border border-slate-300 rounded-xl bg-slate-50">
                    <button
                      onClick={() => updateCartQuantity(item.id, item.quantity - 1)}
                      className="px-3 py-1 text-slate-600 hover:bg-slate-200 rounded-l-xl font-bold transition-colors"
                      title="Decrease quantity"
                    >
                      -
                    </button>
                    <span className="px-3 py-1 text-xs font-bold text-slate-900">{item.quantity}</span>
                    <button
                      onClick={() => updateCartQuantity(item.id, item.quantity + 1)}
                      disabled={item.quantity >= product.stock_quantity}
                      className="px-3 py-1 text-slate-600 hover:bg-slate-200 disabled:opacity-30 rounded-r-xl font-bold transition-colors"
                      title="Increase quantity"
                    >
                      +
                    </button>
                  </div>

                  {/* Subtotal */}
                  <div className="text-right">
                    <span className="text-[10px] text-slate-400 block uppercase">Subtotal</span>
                    <span className="text-base font-black text-slate-900">
                      ₹{item.subtotal.toLocaleString('en-IN')}
                    </span>
                  </div>

                  {/* Delete Button */}
                  <button
                    onClick={() => removeFromCart(item.id)}
                    className="p-2 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-rose-50 transition-colors"
                    title="Remove item"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}

          <div className="pt-2">
            <Link
              to="/discover"
              className="inline-flex items-center gap-1.5 text-xs font-bold text-indigo-600 hover:text-indigo-800"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Continue Shopping
            </Link>
          </div>
        </div>

        {/* Right 1 Col: Summary & Checkout */}
        <div className="space-y-4">
          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-md space-y-4">
            <h2 className="text-lg font-black text-slate-900 border-b border-slate-100 pb-3">
              Order Summary
            </h2>

            <div className="space-y-2.5 text-xs sm:text-sm text-slate-600">
              <div className="flex justify-between">
                <span>Subtotal ({cart.item_count} items)</span>
                <span className="font-bold text-slate-900">
                  ₹{cart.subtotal.toLocaleString('en-IN')}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Delivery Charges</span>
                <span className="font-bold text-emerald-600">FREE Demo Delivery</span>
              </div>
              <div className="flex justify-between">
                <span>Taxes & GST</span>
                <span className="font-medium text-slate-500">Included</span>
              </div>
            </div>

            <div className="border-t border-slate-200 pt-3 flex justify-between items-baseline">
              <div>
                <span className="text-xs font-bold text-slate-700 block">Total Amount</span>
                <span className="text-[10px] text-slate-400">INR (Indian Rupees)</span>
              </div>
              <span className="text-2xl font-black text-slate-900">
                ₹{cart.total.toLocaleString('en-IN')}
              </span>
            </div>

            <button
              onClick={() => navigate('/checkout')}
              className="w-full py-3.5 px-6 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-500/20 flex items-center justify-center gap-2 transition-all active:scale-95"
            >
              <span>Proceed to Checkout</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <div className="flex items-center justify-center gap-2 text-[11px] text-slate-400 pt-1">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Simulated Demo Payment • Zero Real Charges</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
