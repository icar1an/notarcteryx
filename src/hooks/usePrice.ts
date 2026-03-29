'use client';

import { useState, useEffect, useCallback } from 'react';

interface PriceData {
  price: number;
  currency: string;
}

interface UsePriceReturn {
  price: number;
  currency: string;
  loading: boolean;
  error: string | null;
  refreshPrice: (quizAnswers?: Record<string, string>) => Promise<void>;
}

export function usePrice(productId: string, defaultPrice: number): UsePriceReturn {
  const [price, setPrice] = useState(defaultPrice);
  const [currency, setCurrency] = useState('USD');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPrice = useCallback(async (quizAnswers?: Record<string, string>) => {
    setLoading(true);
    setError(null);
    try {
      const url = `/api/price?productId=${encodeURIComponent(productId)}`;
      const res = quizAnswers
        ? await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quizAnswers }),
          })
        : await fetch(url);

      if (!res.ok) throw new Error('Failed to fetch price');

      const data: PriceData = await res.json();
      setPrice(data.price);
      setCurrency(data.currency);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      // Keep default price on error
    } finally {
      setLoading(false);
    }
  }, [productId]);

  useEffect(() => {
    fetchPrice();
  }, [fetchPrice]);

  return { price, currency, loading, error, refreshPrice: fetchPrice };
}
