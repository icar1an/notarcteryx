'use client';

import { useState, useRef, useCallback, useEffect } from 'react';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

interface QuizAnswer {
  mountain_name: string;
  answered_at: string;
  keystroke_count: number;
  paste_detected: boolean;
  focus_lost_ms: number;
}

interface QuizResult {
  truthfulness_score: number;
  final_price: number;
  base_price: number;
  surcharge_pct: number;
  message: string;
  score_breakdown: Record<string, number>;
}

type QuizState = 'idle' | 'active' | 'submitting' | 'result';

export interface InputTracking {
  keystrokes: number;
  pasted: boolean;
  focusLostMs: number;
}

export function useQuiz(productId: string) {
  const [state, setState] = useState<QuizState>('idle');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [expiresAt, setExpiresAt] = useState<Date | null>(null);
  const [result, setResult] = useState<QuizResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const tabAwayCount = useRef(0);
  const tabAwayStart = useRef<number | null>(null);

  // Track tab-away events while quiz is active
  useEffect(() => {
    if (state !== 'active') return;

    const handleVisibility = () => {
      if (document.hidden) {
        tabAwayCount.current += 1;
        tabAwayStart.current = Date.now();
      }
    };

    document.addEventListener('visibilitychange', handleVisibility);
    return () => document.removeEventListener('visibilitychange', handleVisibility);
  }, [state]);

  const startQuiz = useCallback(async () => {
    setState('active');
    setError(null);
    setResult(null);
    tabAwayCount.current = 0;

    try {
      const res = await fetch(`${BACKEND_URL}/api/quiz/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId }),
      });

      if (!res.ok) throw new Error('Failed to start quiz');

      const data = await res.json();
      setSessionId(data.session_id);
      setExpiresAt(new Date(data.expires_at));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start quiz');
      setState('idle');
    }
  }, [productId]);

  const submitAnswers = useCallback(
    async (
      answers: { text: string; answeredAt: Date; tracking: InputTracking }[]
    ) => {
      if (!sessionId) return;

      setState('submitting');
      setError(null);

      const payload = {
        answers: answers.map((a) => ({
          mountain_name: a.text,
          answered_at: a.answeredAt.toISOString(),
          keystroke_count: a.tracking.keystrokes,
          paste_detected: a.tracking.pasted,
          focus_lost_ms: a.tracking.focusLostMs,
        })),
        tab_away_count: tabAwayCount.current,
      };

      try {
        const res = await fetch(
          `${BACKEND_URL}/api/quiz/${sessionId}/submit`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          }
        );

        if (res.status === 410) {
          setError('Time expired. Try again.');
          setState('idle');
          return null;
        }

        if (!res.ok) throw new Error('Failed to submit quiz');

        const data: QuizResult = await res.json();
        setResult(data);
        setState('result');
        return data;
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Submission failed');
        setState('idle');
        return null;
      }
    },
    [sessionId]
  );

  const reset = useCallback(() => {
    setState('idle');
    setSessionId(null);
    setExpiresAt(null);
    setResult(null);
    setError(null);
  }, []);

  return {
    state,
    sessionId,
    expiresAt,
    result,
    error,
    startQuiz,
    submitAnswers,
    reset,
  };
}
