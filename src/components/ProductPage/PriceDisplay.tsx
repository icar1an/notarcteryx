'use client';

import styles from './PriceDisplay.module.css';

interface PriceDisplayProps {
  productId: string;
  defaultPrice: number;
  quizPrice?: number | null;
}

export function PriceDisplay({ productId, defaultPrice, quizPrice }: PriceDisplayProps) {
  const price = quizPrice ?? defaultPrice;
  const installment = (price / 4).toFixed(2);
  const hasSurcharge = quizPrice !== null && quizPrice !== undefined && quizPrice > defaultPrice;

  return (
    <div className={styles.priceWrap} data-price={price}>
      <p className={styles.price}>
        {quizPrice === null || quizPrice === undefined ? (
          <span className={styles.hiddenPrice}>Price revealed at checkout</span>
        ) : (
          `$${price.toFixed(2)}`
        )}
      </p>
      {hasSurcharge && (
        <p className={styles.surchargeNote}>
          Includes trail verification adjustment
        </p>
      )}
      {quizPrice !== null && quizPrice !== undefined && (
        <p className={styles.klarna}>
          4 payments of <strong>${installment}</strong> at 0% interest with{' '}
          <strong className={styles.klarnaLogo}>Klarna</strong>
        </p>
      )}
      {(quizPrice === null || quizPrice === undefined) && (
        <p className={styles.klarna}>
          Klarna available after price is revealed
        </p>
      )}
    </div>
  );
}
