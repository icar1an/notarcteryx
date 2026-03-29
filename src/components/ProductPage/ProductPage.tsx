'use client';

import { useState } from 'react';
import { Product } from '@/data/product';
import { ImageGallery } from './ImageGallery';
import { ProductInfo } from './ProductInfo';
import styles from './ProductPage.module.css';

interface ProductPageProps {
  product: Product;
}

export function ProductPage({ product }: ProductPageProps) {
  const [selectedColor, setSelectedColor] = useState(product.selectedColor);

  return (
    <main className={styles.productPage}>
      <div className={styles.container}>
        <div className={styles.grid}>
          <ImageGallery images={product.images} />
          <ProductInfo
            product={product}
            selectedColor={selectedColor}
            onColorChange={setSelectedColor}
          />
        </div>
      </div>
    </main>
  );
}
