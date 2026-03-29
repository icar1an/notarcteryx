import type { ReactElement } from 'react';
import styles from './FeatureIcons.module.css';

interface Feature {
  icon: string;
  title: string;
  description: string;
}

interface FeatureIconsProps {
  features: Feature[];
}

const iconMap: Record<string, ReactElement> = {
  'natural-fibre': (
    <svg width="40" height="40" viewBox="0 0 48 48" fill="none" stroke="#1A1A1A" strokeWidth="1.5">
      <path d="M24 44c0-11-8-16-8-24a8 8 0 1116 0c0 8-8 13-8 24z" />
      <path d="M20 24c2 2 6 2 8 0" />
      <circle cx="24" cy="14" r="2" fill="#1A1A1A" stroke="none" />
    </svg>
  ),
  'synthetic-fibre': (
    <svg width="40" height="40" viewBox="0 0 48 48" fill="none" stroke="#1A1A1A" strokeWidth="1.5">
      <path d="M24 4l4 8-4 8 4 8-4 8 4 8" />
      <path d="M16 8l4 8-4 8 4 8-4 8" />
      <path d="M32 8l-4 8 4 8-4 8 4 8" />
    </svg>
  ),
  'multi-use': (
    <svg width="40" height="40" viewBox="0 0 48 48" fill="none" stroke="#1A1A1A" strokeWidth="1.5">
      <path d="M24 4L4 18l20 14 20-14L24 4z" />
      <path d="M4 26l20 14 20-14" />
      <path d="M4 34l20 14 20-14" />
    </svg>
  ),
};

export function FeatureIcons({ features }: FeatureIconsProps) {
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.grid}>
          {features.map((feature, i) => (
            <div key={i} className={styles.feature}>
              <div className={styles.icon}>
                {iconMap[feature.icon] || null}
              </div>
              <h3 className={styles.featureTitle}>{feature.title}</h3>
              <p className={styles.featureDesc}>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
