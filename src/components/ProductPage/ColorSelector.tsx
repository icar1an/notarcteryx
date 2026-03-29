'use client';

import { ColorOption } from '@/data/product';
import styles from './ColorSelector.module.css';

interface ColorSelectorProps {
  colors: ColorOption[];
  selected: string;
  onChange: (name: string) => void;
}

export function ColorSelector({ colors, selected, onChange }: ColorSelectorProps) {
  return (
    <div className={styles.colorSelector}>
      <p className={styles.colorLabel}>
        <span className={styles.colorLabelPrefix}>Colour:</span> {selected}
      </p>
      <div className={styles.swatches}>
        {colors.map((color) => (
          <button
            key={color.slug}
            className={`${styles.swatch} ${selected === color.name ? styles.swatchSelected : ''} ${!color.available ? styles.swatchUnavailable : ''}`}
            onClick={() => onChange(color.name)}
            aria-label={`${color.name}${!color.available ? ' - unavailable' : ''}`}
            title={color.name}
          >
            <svg viewBox="0 0 52 52" className={styles.swatchSvg}>
              {/* Left half */}
              <rect x="0" y="0" width="26" height="52" fill={color.leftColor} />
              {/* Right half */}
              <rect x="26" y="0" width="26" height="52" fill={color.rightColor} />
              {/* X overlay for unavailable */}
              {!color.available && (
                <>
                  <line x1="4" y1="4" x2="48" y2="48" stroke="#999" strokeWidth="1" opacity="0.6" />
                  <line x1="48" y1="4" x2="4" y2="48" stroke="#999" strokeWidth="1" opacity="0.6" />
                </>
              )}
            </svg>
          </button>
        ))}
      </div>
    </div>
  );
}
