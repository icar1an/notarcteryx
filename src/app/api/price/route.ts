import { NextRequest, NextResponse } from 'next/server';

/**
 * Dynamic pricing endpoint.
 *
 * GET  /api/price?productId=bird-head-toque  → returns default price
 * POST /api/price?productId=bird-head-toque  → accepts quiz answers, returns adjusted price
 *
 * ★ This is the integration point for the custom backend.
 * Replace the pricing logic below with your quiz-based pricing algorithm.
 */

const DEFAULT_PRICES: Record<string, number> = {
  'bird-head-toque': 60.0,
};

export async function GET(request: NextRequest) {
  const productId = request.nextUrl.searchParams.get('productId') || 'bird-head-toque';
  const price = DEFAULT_PRICES[productId] ?? 60.0;

  return NextResponse.json({
    price,
    currency: 'USD',
  });
}

export async function POST(request: NextRequest) {
  const productId = request.nextUrl.searchParams.get('productId') || 'bird-head-toque';
  const body = await request.json();
  const { quizAnswers } = body;

  // ★ TODO: Replace this with your quiz-based pricing logic
  // Example: adjust price based on quiz responses
  let price = DEFAULT_PRICES[productId] ?? 60.0;

  if (quizAnswers) {
    // Placeholder: apply a discount based on quiz completion
    // Replace this with real pricing logic
    const answerCount = Object.keys(quizAnswers).length;
    if (answerCount > 0) {
      price = price * (1 - answerCount * 0.05); // 5% discount per answer
      price = Math.max(price, 30); // Floor price
    }
  }

  return NextResponse.json({
    price: Math.round(price * 100) / 100,
    currency: 'USD',
  });
}
