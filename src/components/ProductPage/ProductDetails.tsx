'use client';

import { useState } from 'react';
import styles from './ProductDetails.module.css';

interface ProductDetailsProps {
  materials: string;
}

export function ProductDetails({ materials }: ProductDetailsProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={styles.detailsSection}>
      <button
        className={styles.toggleBtn}
        onClick={() => setExpanded(!expanded)}
        aria-expanded={expanded}
      >
        <span className={styles.toggleLabel}>Product details</span>
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          className={`${styles.chevron} ${expanded ? styles.chevronOpen : ''}`}
        >
          <path d="M9 18l6-6-6-6" />
        </svg>
      </button>

      {expanded && (
        <div className={styles.detailsContent}>
          <div className={styles.detailRow}>
            <span className={styles.detailKey}>Materials</span>
            <span className={styles.detailValue}>{materials}</span>
          </div>
          <div className={styles.detailRow}>
            <span className={styles.detailKey}>Construction</span>
            <span className={styles.detailValue}>Microfleece band lining</span>
          </div>
          <div className={styles.detailRow}>
            <span className={styles.detailKey}>Weight</span>
            <span className={styles.detailValue}>70 g / 2.5 oz</span>
          </div>
          <div className={styles.detailRow}>
            <span className={styles.detailKey}>Care</span>
            <span className={styles.detailValue}>Machine wash cold, tumble dry low</span>
          </div>
        </div>
      )}
    </div>
  );
}
