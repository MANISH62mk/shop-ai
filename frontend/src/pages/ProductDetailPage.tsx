import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  Star,
  ShoppingCart,
  Zap,
  ShieldCheck,
  Truck,
  RotateCcw,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  ArrowLeft,
  Share2
} from 'lucide-react';
import { Product } from '../types';
import { api } from '../services/api';
import { useApp } from '../context/AppContext';
import { ProductCard } from '../components/ProductCard';

export const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { addToCart, recordProductView, showToast } = useApp();

  const [product, setProduct] = useState<Product | null>(null);
  const [relatedProducts, setRelatedProducts] = useState<Product[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [addingToCart, setAddingToCart] = useState(false);

  useEffect(() => {
    if (!id) return;
    const prodId = parseInt(id, 10);
    if (isNaN(prodId)) return;

    recordProductView(prodId);

    const loadProductDetails = async () => {
      setLoading(true);
      try {
        const [prodData, relatedData] = await Promise.all([
          api.getProductById(prodId),
          api.getRelatedProducts(prodId),
        ]);
        setProduct(prodData);
        setRelatedProducts(relatedData);
        setQuantity(1);
      } catch (err) {
        console.error('Failed to load product:', err);
        showToast('Product not found', 'error');
        navigate('/discover');
      } finally {
        setLoading(false);
      }
    };

    loadProductDetails();
  }, [id]);

  if (loading || !product) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-indigo-600/30 border-t-indigo-600 rounded-full animate-spin mb-4" />
        <p className="text-sm font-semibold text-slate-600">Loading product details...</p>
      </div>
    );
  }

  const isOutOfStock = product.stock_quantity <= 0;
  const isLowStock = product.stock_quantity > 0 && product.stock_quantity <= 3;

  // Parse specifications JSON
  let specsObj: Record<string, string> = {};
  try {
    if (product.specs) {
      specsObj = JSON.parse(product.specs);
    }
  } catch (e) {
    specsObj = {};
  }

  const handleAddToCart = async () => {
    if (isOutOfStock) return;
    setAddingToCart(true);
    try {
      await addToCart(product.id, quantity);
    } finally {
      setAddingToCart(false);
    }
  };

  const handleBuyNow = async () => {
    if (isOutOfStock) return;
    try {
      await addToCart(product.id, quantity);
      navigate('/checkout');
    } catch (e) {
      // Error handled by addToCart
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
      {/* Breadcrumb / Back button */}
      <div>
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-indigo-600 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Catalog
        </button>
      </div>

      {/* Main Product Showcase */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
        {/* Left: Product Image */}
        <div className="space-y-4">
          <div className="relative aspect-4/3 sm:aspect-square w-full rounded-3xl overflow-hidden bg-slate-100 border border-slate-200/80 shadow-md">
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-full object-cover object-center"
              onError={(e) => {
                (e.target as HTMLImageElement).src =
                  'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=600&auto=format&fit=crop&q=80';
              }}
            />

            {/* Floating Stock Badge */}
            <div className="absolute top-4 left-4">
              {isOutOfStock ? (
                <span className="px-3.5 py-1.5 text-xs font-bold rounded-xl bg-rose-600 text-white shadow-lg">
                  Out of Stock
                </span>
              ) : isLowStock ? (
                <span className="px-3.5 py-1.5 text-xs font-bold rounded-xl bg-amber-500 text-white shadow-lg">
                  Only {product.stock_quantity} Left in Stock!
                </span>
              ) : (
                <span className="px-3.5 py-1.5 text-xs font-bold rounded-xl bg-emerald-600 text-white shadow-lg">
                  In Stock ({product.stock_quantity} available)
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Right: Product Info & Actions */}
        <div className="space-y-6">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-md border border-indigo-200/60">
                {product.brand} • {product.category}
              </span>

              <div className="flex items-center gap-1.5 bg-amber-50 px-2.5 py-1 rounded-md border border-amber-200/70">
                <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
                <span className="text-xs font-bold text-slate-800">{product.rating.toFixed(1)} / 5.0</span>
                <span className="text-[10px] text-slate-400">(Verified ratings)</span>
              </div>
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 leading-tight">
              {product.name}
            </h1>
          </div>

          {/* Pricing Card */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
            <div>
              <span className="text-xs text-slate-500 font-medium block">Special Price</span>
              <div className="text-3xl font-black text-slate-900">
                ₹{product.price.toLocaleString('en-IN')}
              </div>
              <span className="text-[11px] text-emerald-700 font-semibold">
                ✓ Inclusive of all taxes & free shipping
              </span>
            </div>

            <div className="text-right">
              <span className="text-xs text-slate-500 block">Inventory Status</span>
              <span className={`text-sm font-bold ${isOutOfStock ? 'text-rose-600' : 'text-emerald-600'}`}>
                {isOutOfStock ? 'Currently Unavailable' : `${product.stock_quantity} units ready to dispatch`}
              </span>
            </div>
          </div>

          {/* Description */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
              Product Overview
            </h3>
            <p className="text-sm text-slate-700 leading-relaxed">
              {product.description}
            </p>
          </div>

          {/* Why ShopAI Recommends This */}
          <div className="p-5 bg-gradient-to-br from-indigo-50/80 via-purple-50/50 to-slate-50 rounded-2xl border border-indigo-200/80 shadow-xs">
            <div className="flex items-center gap-2 text-indigo-900 font-bold text-sm mb-3">
              <Sparkles className="w-4 h-4 text-indigo-600" />
              <span>Why ShopAI Recommends This:</span>
            </div>
            <ul className="space-y-2 text-xs text-slate-700">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>Verified in live inventory ({product.stock_quantity} units available)</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>High rating of {product.rating} ★ based on customer feedback</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>Authentic {product.brand} hardware backed by warranty</span>
              </li>
            </ul>
          </div>

          {/* Quantity Selector and CTA buttons */}
          <div className="space-y-4 pt-2">
            {!isOutOfStock && (
              <div className="flex items-center gap-4">
                <span className="text-xs font-bold text-slate-700">Quantity:</span>
                <div className="flex items-center border border-slate-300 rounded-xl bg-white shadow-xs">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    disabled={quantity <= 1}
                    className="px-3.5 py-1.5 text-slate-600 hover:bg-slate-100 disabled:opacity-30 rounded-l-xl font-bold transition-colors"
                  >
                    -
                  </button>
                  <span className="px-4 py-1.5 text-sm font-bold text-slate-800">{quantity}</span>
                  <button
                    onClick={() => setQuantity(Math.min(product.stock_quantity, quantity + 1))}
                    disabled={quantity >= product.stock_quantity}
                    className="px-3.5 py-1.5 text-slate-600 hover:bg-slate-100 disabled:opacity-30 rounded-r-xl font-bold transition-colors"
                  >
                    +
                  </button>
                </div>
                <span className="text-xs text-slate-400">
                  (Max {product.stock_quantity})
                </span>
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={handleAddToCart}
                disabled={isOutOfStock || addingToCart}
                className="flex-1 py-3.5 px-6 rounded-2xl bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-200 disabled:text-slate-400 disabled:cursor-not-allowed text-white font-bold text-sm shadow-md shadow-indigo-500/20 flex items-center justify-center gap-2 transition-all active:scale-95"
              >
                {addingToCart ? (
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <ShoppingCart className="w-4 h-4" />
                )}
                <span>{isOutOfStock ? 'Out of Stock' : 'Add to Cart'}</span>
              </button>

              <button
                onClick={handleBuyNow}
                disabled={isOutOfStock}
                className="flex-1 py-3.5 px-6 rounded-2xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 disabled:bg-slate-200 disabled:text-slate-400 disabled:cursor-not-allowed text-white font-bold text-sm shadow-md shadow-purple-500/20 flex items-center justify-center gap-2 transition-all active:scale-95"
              >
                <Zap className="w-4 h-4" />
                <span>Buy Now (Demo Checkout)</span>
              </button>
            </div>
          </div>

          {/* Trust Guarantees */}
          <div className="grid grid-cols-3 gap-3 pt-4 border-t border-slate-200 text-center text-[11px] text-slate-500">
            <div className="flex flex-col items-center gap-1">
              <Truck className="w-4 h-4 text-indigo-600" />
              <span>Fast Dispatch</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Genuine Device</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <RotateCcw className="w-4 h-4 text-purple-600" />
              <span>Demo Checkout</span>
            </div>
          </div>
        </div>
      </div>

      {/* Specifications Table */}
      {Object.keys(specsObj).length > 0 && (
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm">
          <h2 className="text-xl font-black text-slate-900 mb-6">
            Technical Specifications
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-3">
            {Object.entries(specsObj).map(([key, val]) => (
              <div
                key={key}
                className="flex items-center justify-between py-2.5 border-b border-slate-100 text-xs sm:text-sm"
              >
                <span className="font-semibold text-slate-500">{key}</span>
                <span className="font-bold text-slate-900 text-right">{val}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Related & In-Stock Alternatives */}
      {relatedProducts.length > 0 && (
        <div className="space-y-6 pt-6">
          <div>
            <h2 className="text-2xl font-black text-slate-900">
              Related & In-Stock Alternatives
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              Other top-rated devices available in {product.category}
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {relatedProducts.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
