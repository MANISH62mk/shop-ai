import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  CreditCard,
  Truck,
  ShieldCheck,
  CheckCircle2,
  Lock,
  ArrowLeft,
  AlertCircle
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { api } from '../services/api';

export const CheckoutPage: React.FC = () => {
  const { cart, user, refreshCart, showToast } = useApp();
  const navigate = useNavigate();

  const [name, setName] = useState(user ? user.name : 'Rohan Verma');
  const [email, setEmail] = useState(user ? user.email : 'rohan.verma@example.com');
  const [phone, setPhone] = useState('+91 9876543210');
  const [address, setAddress] = useState('Flat 402, Green Glen Heights, Bellandur, Bengaluru, KA 560103');
  const [paymentMethod, setPaymentMethod] = useState<'Cash on Delivery' | 'Demo Card Payment'>('Demo Card Payment');

  // Simulated card details
  const [cardNumber, setCardNumber] = useState('4532 •••• •••• 8821');
  const [cardExpiry, setCardExpiry] = useState('08/29');
  const [cardCvv, setCardCvv] = useState('782');

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!cart || cart.items.length === 0) {
    navigate('/cart');
    return null;
  }

  const handleSubmitOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const order = await api.checkout({
        customer_name: name,
        customer_email: email,
        customer_phone: phone,
        shipping_address: address,
        payment_method: paymentMethod,
      });

      await refreshCart();
      showToast('Order successfully confirmed!', 'success');
      navigate(`/order-success/${order.id}`, { state: { order } });
    } catch (err: any) {
      setError(err.message || 'Failed to place order. Check inventory.');
      showToast(err.message || 'Checkout failed', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <button
          onClick={() => navigate('/cart')}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-indigo-600 mb-2 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Return to Cart
        </button>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">
          Demo Express Checkout
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Simulated college mini-project checkout. Live inventory will be deducted automatically.
        </p>
      </div>

      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-start gap-3 text-rose-700 text-sm">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-rose-600" />
          <div>
            <p className="font-bold">Inventory Alert</p>
            <p>{error}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmitOrder}>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left 2 Cols: Shipping & Payment Details */}
          <div className="lg:col-span-2 space-y-6">
            {/* Step 1: Shipping Info */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs space-y-4">
              <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
                <div className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center">
                  1
                </div>
                <h2 className="text-base font-bold text-slate-900">Delivery Address</h2>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 bg-slate-50/50"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 bg-slate-50/50"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Mobile Phone</label>
                  <input
                    type="tel"
                    required
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 bg-slate-50/50"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Complete Delivery Address</label>
                  <textarea
                    required
                    rows={2}
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 bg-slate-50/50"
                  />
                </div>
              </div>
            </div>

            {/* Step 2: Payment Options */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs space-y-4">
              <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
                <div className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center">
                  2
                </div>
                <h2 className="text-base font-bold text-slate-900">Payment Method (Simulated)</h2>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {/* Demo Card Payment Option */}
                <div
                  onClick={() => setPaymentMethod('Demo Card Payment')}
                  className={`p-4 rounded-2xl border-2 cursor-pointer transition-all ${
                    paymentMethod === 'Demo Card Payment'
                      ? 'border-indigo-600 bg-indigo-50/50 text-indigo-950 shadow-xs'
                      : 'border-slate-200 hover:border-slate-300 bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2 font-bold text-xs">
                      <CreditCard className="w-4 h-4 text-indigo-600" />
                      <span>Demo Card Payment</span>
                    </div>
                    {paymentMethod === 'Demo Card Payment' && (
                      <CheckCircle2 className="w-4 h-4 text-indigo-600" />
                    )}
                  </div>
                  <p className="text-[11px] text-slate-500">
                    Simulates credit/debit transaction without real gateway billing.
                  </p>
                </div>

                {/* Cash on Delivery Option */}
                <div
                  onClick={() => setPaymentMethod('Cash on Delivery')}
                  className={`p-4 rounded-2xl border-2 cursor-pointer transition-all ${
                    paymentMethod === 'Cash on Delivery'
                      ? 'border-indigo-600 bg-indigo-50/50 text-indigo-950 shadow-xs'
                      : 'border-slate-200 hover:border-slate-300 bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2 font-bold text-xs">
                      <Truck className="w-4 h-4 text-emerald-600" />
                      <span>Cash on Delivery</span>
                    </div>
                    {paymentMethod === 'Cash on Delivery' && (
                      <CheckCircle2 className="w-4 h-4 text-indigo-600" />
                    )}
                  </div>
                  <p className="text-[11px] text-slate-500">
                    Pay demo cash upon physical parcel receipt.
                  </p>
                </div>
              </div>

              {/* Card Inputs if Card chosen */}
              {paymentMethod === 'Demo Card Payment' && (
                <div className="mt-4 p-4 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-3">
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span className="font-semibold text-slate-700">Simulated Card Details</span>
                    <span className="flex items-center gap-1 text-[11px] text-emerald-600 font-semibold">
                      <Lock className="w-3 h-3" /> 256-bit Demo SSL
                    </span>
                  </div>
                  <div>
                    <label className="block text-[11px] font-semibold text-slate-600 mb-1">Card Number</label>
                    <input
                      type="text"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(e.target.value)}
                      className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl bg-white font-mono"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-[11px] font-semibold text-slate-600 mb-1">Expiry Date</label>
                      <input
                        type="text"
                        value={cardExpiry}
                        onChange={(e) => setCardExpiry(e.target.value)}
                        className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl bg-white font-mono"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] font-semibold text-slate-600 mb-1">CVV</label>
                      <input
                        type="password"
                        value={cardCvv}
                        onChange={(e) => setCardCvv(e.target.value)}
                        className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl bg-white font-mono"
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right 1 Col: Summary & Place Order */}
          <div className="space-y-4">
            <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-md space-y-4">
              <h2 className="text-lg font-black text-slate-900 border-b border-slate-100 pb-3">
                Review Items ({cart.item_count})
              </h2>

              <div className="space-y-3 max-h-60 overflow-y-auto pr-1">
                {cart.items.map((item) => (
                  <div key={item.id} className="flex items-center justify-between text-xs gap-2">
                    <div className="flex-1 truncate">
                      <p className="font-bold text-slate-800 truncate">{item.product.name}</p>
                      <span className="text-slate-400">Qty: {item.quantity}</span>
                    </div>
                    <span className="font-bold text-slate-900 shrink-0">
                      ₹{item.subtotal.toLocaleString('en-IN')}
                    </span>
                  </div>
                ))}
              </div>

              <div className="border-t border-slate-100 pt-3 space-y-2 text-xs text-slate-600">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span className="font-bold text-slate-900">₹{cart.subtotal.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between">
                  <span>Shipping</span>
                  <span className="font-bold text-emerald-600">FREE</span>
                </div>
              </div>

              <div className="border-t border-slate-200 pt-3 flex justify-between items-baseline">
                <div>
                  <span className="text-xs font-bold text-slate-700 block">Total Due</span>
                  <span className="text-[10px] text-slate-400">Indian Rupees</span>
                </div>
                <span className="text-2xl font-black text-slate-900">
                  ₹{cart.total.toLocaleString('en-IN')}
                </span>
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-4 px-6 rounded-2xl bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-black text-sm shadow-lg shadow-indigo-600/25 flex items-center justify-center gap-2 transition-all active:scale-95"
              >
                {isSubmitting ? (
                  <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <span>Place Demo Order (₹{cart.total.toLocaleString('en-IN')})</span>
                )}
              </button>

              <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-emerald-800 text-[11px] leading-relaxed flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>
                  Demo Mode Active: Product stock will automatically decrement in the SQLite database and update the Admin Dashboard.
                </span>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};
