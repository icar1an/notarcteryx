'use client';

import { useState } from 'react';
import { Product } from '@/data/product';
import styles from './DescriptionSection.module.css';

interface DescriptionSectionProps {
  product: Product;
}

export function DescriptionSection({ product }: DescriptionSectionProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.grid}>
          <h2 className={styles.title}>{product.name}</h2>
          <div className={styles.content}>
            <p className={styles.description}>{product.longDescription}</p>
            {expanded && (
              <div className={styles.expanded}>
                <p className={styles.description}>
                  Made with 50% Merino Wool and 50% Recycled Polyester. Features a microfleece band
                  lining for added comfort against the skin.
                </p>
              </div>
            )}
            <button
              className={styles.readMore}
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? 'Read less' : 'Read more'}
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className={`${styles.readMoreChevron} ${expanded ? styles.readMoreChevronOpen : ''}`}
              >
                <path d="M9 18l6-6-6-6" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
