'use client';

import { useCart } from '@/hooks/useCart';
import styles from './Header.module.css';

export function CartIcon() {
  const { totalItems } = useCart();

  return (
    <a href="/cart" className={styles.iconBtn} aria-label="Cart">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" />
        <line x1="3" y1="6" x2="21" y2="6" />
        <path d="M16 10a4 4 0 01-8 0" />
      </svg>
      <span className={styles.cartCount}>{totalItems}</span>
    </a>
  );
}
