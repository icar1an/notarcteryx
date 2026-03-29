export interface ColorOption {
  name: string;
  leftColor: string;
  rightColor: string;
  available: boolean;
  slug: string;
}

export interface ProductImage {
  src: string;
  alt: string;
  width: number;
  height: number;
}

export interface Product {
  name: string;
  slug: string;
  breadcrumbs: { label: string; href: string }[];
  shortDescription: string;
  longDescription: string;
  price: number;
  currency: string;
  colors: ColorOption[];
  selectedColor: string;
  images: ProductImage[];
  features: { icon: string; title: string; description: string }[];
  materials: string;
  storeAvailability: { name: string; inStock: boolean }[];
}

const CDN = 'https://images.arcteryx.com/details/1350x1710';

function proxyUrl(cdnUrl: string): string {
  return `/api/image?url=${encodeURIComponent(cdnUrl)}`;
}

export const product: Product = {
  name: 'Bird Head Toque',
  slug: 'bird-head-toque',
  breadcrumbs: [
    { label: "Arc'teryx", href: '/' },
    { label: 'Accessories', href: '/accessories' },
    { label: 'Bird Head Toque', href: '/bird-head-toque' },
  ],
  shortDescription: 'Warm, comfortable toque made from a blend of wool and recycled polyester.',
  longDescription:
    "Optimized for warmth, our classic logo toque is made with a wool and recycled polyester blend for natural thermal performance and comfort. A brushed polyester band adds technical performance and a layer of softness. Packs easily for warmth anywhere.",
  price: 60.0,
  currency: 'USD',
  colors: [
    { name: 'Mantis / Arctic Silk', leftColor: '#A3C23D', rightColor: '#EDE9E0', available: false, slug: 'mantis-arctic-silk' },
    { name: 'Moondrop / Mallow', leftColor: '#483D4B', rightColor: '#B0A8C0', available: false, slug: 'moondrop-mallow' },
    { name: 'Mallow / Euphoria', leftColor: '#B0A8C0', rightColor: '#E0E040', available: false, slug: 'mallow-euphoria' },
    { name: 'Pineberry / Sea Salt', leftColor: '#EDAAC9', rightColor: '#D3CFC6', available: false, slug: 'pineberry-sea-salt' },
    { name: 'Blk Sapphire / Alpine', leftColor: '#4B576D', rightColor: '#C8D2DB', available: false, slug: 'blk-sapphire-alpine' },
    { name: 'Black / Void', leftColor: '#090E0D', rightColor: '#747676', available: true, slug: 'black-void' },
    { name: 'Cloud / Forage', leftColor: '#BFBFBF', rightColor: '#D9D9D9', available: false, slug: 'cloud-forage' },
  ],
  selectedColor: 'Black / Void',
  images: [
    { src: proxyUrl(`${CDN}/F24-X000006756-Bird-Head-Toque-Black-Void-Front.jpg`), alt: 'Bird Head Toque - Black/Void', width: 1350, height: 1710 },
    { src: proxyUrl(`${CDN}/F24-X000006756-Bird-Head-Toque-Black-Void-Front-View.jpg`), alt: 'Bird Head Toque - Front View', width: 1350, height: 1710 },
    { src: proxyUrl(`${CDN}/F24-X000006756-Bird-Head-Toque-Black-Void-Hover.jpg`), alt: 'Bird Head Toque - Side View', width: 1350, height: 1710 },
    { src: proxyUrl(`${CDN}/F24-X000006756-Bird-Head-Toque-Black-Void-Side-View.jpg`), alt: 'Bird Head Toque - Back View', width: 1350, height: 1710 },
    { src: proxyUrl(`${CDN}/F24-X000006756-Bird-Head-Toque-Black-Void-Back-View.jpg`), alt: 'Bird Head Toque - Detail', width: 1350, height: 1710 },
  ],
  features: [
    {
      icon: 'natural-fibre',
      title: 'Natural fibre',
      description: 'Textiles made from natural fibres provide inherent benefits and next-to-skin comfort.',
    },
    {
      icon: 'synthetic-fibre',
      title: 'Synthetic fibre',
      description: 'Engineered materials that offer enhanced properties or performance.',
    },
    {
      icon: 'multi-use',
      title: 'Multi-use',
      description: 'Versatile high performance designs for diverse activities and conditions.',
    },
  ],
  materials: '50% Merino Wool, 50% Recycled Polyester',
  storeAvailability: [
    { name: "Arc'teryx Stanford Center", inStock: false },
  ],
};
