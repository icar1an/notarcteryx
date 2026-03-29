'use client';

import { useState, useEffect, useCallback } from 'react';

export interface CartItem {
  productId: string;
  name: string;
  color: string;
  size: string;
  quantity: number;
  price: number;
  image: string;
}

const STORAGE_KEY = 'arcteryx-cart';

function loadCart(): CartItem[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveCart(items: CartItem[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  window.dispatchEvent(new Event('cart-updated'));
}

export function useCart() {
  const [items, setItems] = useState<CartItem[]>([]);

  useEffect(() => {
    setItems(loadCart());
    const handler = () => setItems(loadCart());
    window.addEventListener('cart-updated', handler);
    window.addEventListener('storage', handler);
    return () => {
      window.removeEventListener('cart-updated', handler);
      window.removeEventListener('storage', handler);
    };
  }, []);

  const addItem = useCallback((item: Omit<CartItem, 'quantity'>) => {
    const current = loadCart();
    const idx = current.findIndex(
      (i) => i.productId === item.productId && i.color === item.color
    );
    if (idx >= 0) {
      current[idx].quantity += 1;
      current[idx].price = item.price;
    } else {
      current.push({ ...item, quantity: 1 });
    }
    saveCart(current);
    setItems(current);
  }, []);

  const removeItem = useCallback((productId: string, color: string) => {
    const current = loadCart().filter(
      (i) => !(i.productId === productId && i.color === color)
    );
    saveCart(current);
    setItems(current);
  }, []);

  const updateQuantity = useCallback(
    (productId: string, color: string, quantity: number) => {
      const current = loadCart();
      const idx = current.findIndex(
        (i) => i.productId === productId && i.color === color
      );
      if (idx >= 0) {
        if (quantity <= 0) {
          current.splice(idx, 1);
        } else {
          current[idx].quantity = quantity;
        }
      }
      saveCart(current);
      setItems(current);
    },
    []
  );

  const clearCart = useCallback(() => {
    saveCart([]);
    setItems([]);
  }, []);

  const totalItems = items.reduce((sum, i) => sum + i.quantity, 0);
  const subtotal = items.reduce((sum, i) => sum + i.price * i.quantity, 0);

  return { items, addItem, removeItem, updateQuantity, clearCart, totalItems, subtotal };
}
