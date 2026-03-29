import { ProductImage } from '@/data/product';
import styles from './ImageGallery.module.css';

interface ImageGalleryProps {
  images: ProductImage[];
}

export function ImageGallery({ images }: ImageGalleryProps) {
  const [hero, ...grid] = images;

  return (
    <div className={styles.gallery}>
      <div className={styles.heroWrap}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={hero.src}
          alt={hero.alt}
          className={styles.heroImage}
          loading="eager"
        />
      </div>
      <div className={styles.gridImages}>
        {grid.map((img, i) => (
          <div key={i} className={styles.gridItem}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={img.src}
              alt={img.alt}
              className={styles.gridImage}
              loading="lazy"
            />
          </div>
        ))}
      </div>
    </div>
  );
}
