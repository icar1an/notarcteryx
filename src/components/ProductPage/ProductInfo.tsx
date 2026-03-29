'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Product } from '@/data/product';
import { useCart } from '@/hooks/useCart';
import { PriceDisplay } from './PriceDisplay';
import { ColorSelector } from './ColorSelector';
import { StoreAvailability } from './StoreAvailability';
import { ProductDetails } from './ProductDetails';
import { MountainQuiz } from '@/components/MountainQuiz/MountainQuiz';
import styles from './ProductInfo.module.css';

interface ProductInfoProps {
  product: Product;
  selectedColor: string;
  onColorChange: (color: string) => void;
}

export function ProductInfo({ product, selectedColor, onColorChange }: ProductInfoProps) {
  const router = useRouter();
  const { addItem } = useCart();
  const currentColor = product.colors.find(c => c.name === selectedColor);
  const isAvailable = currentColor?.available ?? false;
  const [showQuiz, setShowQuiz] = useState(false);
  const [quizPrice, setQuizPrice] = useState<number | null>(null);

  const displayPrice = quizPrice ?? product.price;

  const handleAddToCart = () => {
    // If they haven't taken the quiz yet, show it
    if (quizPrice === null) {
      setShowQuiz(true);
      return;
    }

    // Already have a price from the quiz — add to cart
    addItem({
      productId: product.slug,
      name: product.name,
      color: selectedColor,
      size: 'NA',
      price: displayPrice,
      image: product.images[0]?.src || '',
    });
    router.push('/cart');
  };

  const handleQuizComplete = (finalPrice: number) => {
    setQuizPrice(finalPrice);
  };

  const handleQuizClose = () => {
    setShowQuiz(false);
    // If they got a result, add to cart automatically
    if (quizPrice !== null) {
      addItem({
        productId: product.slug,
        name: product.name,
        color: selectedColor,
        size: 'NA',
        price: quizPrice,
        image: product.images[0]?.src || '',
      });
      router.push('/cart');
    }
  };

  return (
    <aside className={styles.sidebar}>
      <div className={styles.inner}>
        {/* Title + Rating */}
        <h1 className={styles.title}>{product.name.toUpperCase()}</h1>
        <div className={styles.rating}>
          <div className={styles.stars}>
            {[...Array(5)].map((_, i) => (
              <svg key={i} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" strokeWidth="1.5">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
            ))}
          </div>
          <a href="#reviews" className={styles.reviewLink}>Leave a review</a>
        </div>

        {/* Description */}
        <p className={styles.description}>{product.shortDescription}</p>

        <div className={styles.divider} />

        {/* Price */}
        <PriceDisplay
          productId={product.slug}
          defaultPrice={product.price}
          quizPrice={quizPrice}
        />

        <div className={styles.divider} />

        {/* Color Selector */}
        <ColorSelector
          colors={product.colors}
          selected={selectedColor}
          onChange={onColorChange}
        />

        <div className={styles.divider} />

        {/* Add to Cart / Notify Me */}
        {isAvailable ? (
          <button className={styles.addToCart} onClick={handleAddToCart}>
            {quizPrice === null ? 'Add to Cart' : `Add to Cart — $${displayPrice.toFixed(2)}`}
          </button>
        ) : (
          <button className={styles.notifyBtn}>Notify me</button>
        )}

        <div className={styles.divider} />

        {/* Store Availability */}
        <StoreAvailability stores={product.storeAvailability} />

        <div className={styles.divider} />

        {/* Product Details */}
        <ProductDetails materials={product.materials} />
      </div>

      {/* Quiz Modal */}
      {showQuiz && (
        <MountainQuiz
          productId={product.slug}
          onComplete={handleQuizComplete}
          onClose={handleQuizClose}
        />
      )}
    </aside>
  );
}
