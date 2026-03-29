'use client';

import { useState } from 'react';
import styles from './StoreAvailability.module.css';

interface StoreAvailabilityProps {
  stores: { name: string; inStock: boolean }[];
}

export function StoreAvailability({ stores }: StoreAvailabilityProps) {
  const [expanded, setExpanded] = useState(true);

  return (
    <div className={styles.storeSection}>
      <button
        className={styles.toggleBtn}
        onClick={() => setExpanded(!expanded)}
        aria-expanded={expanded}
      >
        <span className={styles.toggleLabel}>In-store availability</span>
        <span className={styles.toggleIcon}>{expanded ? '−' : '+'}</span>
      </button>

      {expanded && (
        <div className={styles.storeList}>
          {stores.map((store, i) => (
            <div key={i} className={styles.storeItem}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className={styles.storeIcon}>
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <path d="M3 9h18M9 3v18" />
              </svg>
              <span className={styles.storeName}>{store.name}</span>
              <span className={styles.storeStatus}>
                – {store.inStock ? 'In stock' : 'Out of stock'}
                <span className={`${styles.statusDot} ${store.inStock ? styles.statusInStock : styles.statusOutOfStock}`} />
              </span>
            </div>
          ))}
          <a href="#pickup" className={styles.pickupLink}>Pickup information</a>
        </div>
      )}
    </div>
  );
}
