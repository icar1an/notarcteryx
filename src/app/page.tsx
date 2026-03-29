import { Header } from '@/components/Header/Header';
import { ProductPage } from '@/components/ProductPage/ProductPage';
import { DescriptionSection } from '@/components/ProductDescription/DescriptionSection';
import { FeatureIcons } from '@/components/ProductDescription/FeatureIcons';
import { product } from '@/data/product';

export default function Home() {
  return (
    <>
      <Header />
      <ProductPage product={product} />
      <DescriptionSection product={product} />
      <FeatureIcons features={product.features} />
    </>
  );
}
