import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Star, ShoppingCart, CheckCircle, ChevronDown, ChevronUp, Eye } from 'lucide-react';
import { Product } from '../types';
import { useApp } from '../context/AppContext';

interface ProductCardProps {
  product: Product;
  highlightReasons?: boolean;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, highlightReasons = false }) => {
  const { addToCart, recordProductView } = useApp();
  const [showReasons, setShowReasons] = useState(highlightReasons);
  const [adding, setAdding] = useState(false);

  const isOutOfStock = product.stock_quantity <= 0;
  const isLowStock = product.stock_quantity > 0 && product.stock_quantity <= 3;

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (isOutOfStock) return;
    setAdding(true);
    try {
      await addToCart(product.id, 1);
    } finally {
      setAdding(false);
    }
  };

  const handleCardClick = () => {
    recordProductView(product.id);
  };

  return (
    <div
      onClick={handleCardClick}
      className={`group bg-white rounded-2xl border transition-all duration-300 flex flex-col overflow-hidden relative ${
        isOutOfStock
          ? 'border-slate-200 opacity-80'
          : 'border-slate-200/80 hover:border-indigo-300 hover:shadow-xl hover:shadow-indigo-500/5'
      }`}
    >
      {/* Product Image Area */}
      <div className="relative aspect-4/3 w-full overflow-hidden bg-slate-100">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
          onError={(e) => {
            // Fallback image if unsplash link fails
            (e.target as HTMLImageElement).src =
              'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=600&auto=format&fit=crop&q=80';
          }}
        />

        {/* Stock Badge Overlay */}
        <div className="absolute top-3 left-3 flex flex-col gap-1.5 items-start">
          {isOutOfStock ? (
            <span className="px-2.5 py-1 text-xs font-bold rounded-lg bg-rose-600/95 text-white shadow-sm backdrop-blur-xs">
              Out of Stock
            </span>
          ) : isLowStock ? (
            <span className="px-2.5 py-1 text-xs font-bold rounded-lg bg-amber-500 text-white shadow-sm">
              Only {product.stock_quantity} Left!
            </span>
          ) : (
            <span className="px-2 py-0.5 text-[11px] font-semibold rounded-md bg-emerald-600/90 text-white shadow-xs">
              In Stock ({product.stock_quantity})
            </span>
          )}

          {product.relevance_score && (
            <span className="px-2 py-0.5 text-[10px] font-bold rounded-md bg-indigo-900/90 text-indigo-100 border border-indigo-400/30">
              {Math.round(product.relevance_score)}% Match
            </span>
          )}
        </div>

        {/* Category Pill */}
        <span className="absolute top-3 right-3 px-2 py-0.5 text-[11px] font-medium rounded-md bg-white/90 text-slate-700 shadow-xs backdrop-blur-xs">
          {product.category}
        </span>
      </div>

      {/* Product Body */}
      <div className="p-4 sm:p-5 flex-1 flex flex-col justify-between">
        <div>
          {/* Brand & Rating */}
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1.5">
            <span className="font-semibold text-indigo-700 tracking-wide uppercase text-[11px]">
              {product.brand}
            </span>
            <div className="flex items-center gap-1 font-semibold text-slate-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200/60">
              <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
              <span>{product.rating.toFixed(1)}</span>
            </div>
          </div>

          {/* Product Title */}
          <Link
            to={`/product/${product.id}`}
            className="block font-bold text-slate-900 text-sm sm:text-base leading-snug line-clamp-2 hover:text-indigo-600 transition-colors mb-2"
          >
            {product.name}
          </Link>

          {/* Short Description */}
          <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed mb-3">
            {product.description}
          </p>

          {/* Why Recommended Accordion if present */}
          {product.why_recommended && product.why_recommended.length > 0 && (
            <div className="mb-4 bg-indigo-50/70 border border-indigo-100 rounded-xl p-3">
              <button
                type="button"
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  setShowReasons(!showReasons);
                }}
                className="w-full flex items-center justify-between text-left text-xs font-bold text-indigo-900"
              >
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-indigo-600 animate-ping" />
                  Why ShopAI Recommends This:
                </span>
                {showReasons ? (
                  <ChevronUp className="w-3.5 h-3.5 text-indigo-600" />
                ) : (
                  <ChevronDown className="w-3.5 h-3.5 text-indigo-600" />
                )}
              </button>

              {showReasons && (
                <ul className="mt-2 space-y-1 text-[11px] text-indigo-950/80 pl-1">
                  {product.why_recommended.map((reason, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>

        {/* Pricing & Actions */}
        <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-2 mt-auto">
          <div>
            <span className="text-[10px] text-slate-400 block uppercase font-medium">Price</span>
            <div className="text-lg sm:text-xl font-black text-slate-900">
              ₹{product.price.toLocaleString('en-IN')}
            </div>
          </div>

          <div className="flex items-center gap-1.5">
            <Link
              to={`/product/${product.id}`}
              className="px-2.5 py-1.5 sm:px-3 sm:py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors flex items-center gap-1"
              title="View Product Details"
            >
              <Eye className="w-3.5 h-3.5 text-slate-600" />
              <span>View Details</span>
            </Link>

            <button
              onClick={handleAddToCart}
              disabled={isOutOfStock || adding}
              className={`px-2.5 py-1.5 sm:px-3 sm:py-2 text-xs font-semibold rounded-xl flex items-center gap-1.5 transition-all shadow-sm ${
                isOutOfStock
                  ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                  : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-500/20 active:scale-95'
              }`}
            >
              {adding ? (
                <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <ShoppingCart className="w-3.5 h-3.5" />
              )}
              <span>
                {isOutOfStock ? 'Sold Out' : 'Add to Cart'}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
