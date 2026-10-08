import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, CartSummary } from '../types';
import { api } from '../services/api';

export interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

interface AppContextType {
  user: User | null;
  login: (email: string, pass: string) => Promise<void>;
  logout: () => void;
  cart: CartSummary | null;
  cartCount: number;
  refreshCart: () => Promise<void>;
  addToCart: (productId: number, qty?: number) => Promise<void>;
  updateCartQuantity: (itemId: number, qty: number) => Promise<void>;
  removeFromCart: (itemId: number) => Promise<void>;
  clearCart: () => Promise<void>;
  viewedProductIds: number[];
  recordProductView: (id: number) => void;
  toasts: Toast[];
  showToast: (message: string, type?: 'success' | 'error' | 'info') => void;
  removeToast: (id: string) => void;
  isAuthModalOpen: boolean;
  setIsAuthModalOpen: (open: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Demo User session
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('shopai_user');
    return saved ? JSON.parse(saved) : null;
  });

  const [cart, setCart] = useState<CartSummary | null>(null);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  // Viewed products tracking
  const [viewedProductIds, setViewedProductIds] = useState<number[]>(() => {
    const saved = localStorage.getItem('shopai_viewed_ids');
    return saved ? JSON.parse(saved) : [];
  });

  const showToast = (message: string, type: 'success' | 'error' | 'info' = 'success') => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const recordProductView = (id: number) => {
    setViewedProductIds((prev) => {
      const updated = [id, ...prev.filter((item) => item !== id)].slice(0, 10);
      localStorage.setItem('shopai_viewed_ids', JSON.stringify(updated));
      return updated;
    });
  };

  const refreshCart = async () => {
    try {
      const data = await api.getCart();
      setCart(data);
    } catch (err) {
      console.error('Error fetching cart:', err);
    }
  };

  useEffect(() => {
    refreshCart();
  }, []);

  const login = async (email: string, pass: string) => {
    try {
      const loggedUser = await api.login(email, pass);
      setUser(loggedUser);
      localStorage.setItem('shopai_user', JSON.stringify(loggedUser));
      showToast(`Welcome back, ${loggedUser.name}! (${loggedUser.role.toUpperCase()})`, 'success');
      setIsAuthModalOpen(false);
    } catch (err: any) {
      showToast(err.message || 'Login failed', 'error');
      throw err;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('shopai_user');
    showToast('Signed out successfully', 'info');
  };

  const addToCart = async (productId: number, qty: number = 1) => {
    try {
      const updated = await api.addToCart(productId, qty);
      setCart(updated);
      showToast('Added product to cart!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Could not add to cart', 'error');
      throw err;
    }
  };

  const updateCartQuantity = async (itemId: number, qty: number) => {
    try {
      const updated = await api.updateCartQuantity(itemId, qty);
      setCart(updated);
    } catch (err: any) {
      showToast(err.message || 'Could not update quantity', 'error');
    }
  };

  const removeFromCart = async (itemId: number) => {
    try {
      const updated = await api.removeFromCart(itemId);
      setCart(updated);
      showToast('Item removed from cart', 'info');
    } catch (err: any) {
      showToast(err.message || 'Could not remove item', 'error');
    }
  };

  const clearCart = async () => {
    try {
      const updated = await api.clearCart();
      setCart(updated);
    } catch (err: any) {
      console.error('Failed to clear cart:', err);
    }
  };

  const cartCount = cart ? cart.item_count : 0;

  return (
    <AppContext.Provider
      value={{
        user,
        login,
        logout,
        cart,
        cartCount,
        refreshCart,
        addToCart,
        updateCartQuantity,
        removeFromCart,
        clearCart,
        viewedProductIds,
        recordProductView,
        toasts,
        showToast,
        removeToast,
        isAuthModalOpen,
        setIsAuthModalOpen,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within AppProvider');
  return context;
};
