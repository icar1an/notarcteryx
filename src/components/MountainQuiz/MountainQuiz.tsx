'use client';

import { useState, useRef, useEffect, useCallback } from 'react';
import { useQuiz, InputTracking } from '@/hooks/useQuiz';
import styles from './MountainQuiz.module.css';

interface MountainQuizProps {
  productId: string;
  onComplete: (finalPrice: number) => void;
  onClose: () => void;
}

interface AnswerState {
  text: string;
  answeredAt: Date | null;
  tracking: InputTracking;
  submitted: boolean;
}

function createEmptyAnswer(): AnswerState {
  return {
    text: '',
    answeredAt: null,
    tracking: { keystrokes: 0, pasted: false, focusLostMs: 0 },
    submitted: false,
  };
}

export function MountainQuiz({ productId, onComplete, onClose }: MountainQuizProps) {
  const quiz = useQuiz(productId);
  const [answers, setAnswers] = useState<AnswerState[]>(
    () => Array.from({ length: 5 }, createEmptyAnswer)
  );
  const [activeIndex, setActiveIndex] = useState(0);
  const [timeLeft, setTimeLeft] = useState(120);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);
  const focusLostStart = useRef<Record<number, number>>({});

  // Start quiz on mount
  useEffect(() => {
    quiz.startQuiz();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Countdown timer
  useEffect(() => {
    if (quiz.state !== 'active' || !quiz.expiresAt) return;

    const tick = () => {
      const remaining = Math.max(
        0,
        Math.ceil((quiz.expiresAt!.getTime() - Date.now()) / 1000)
      );
      setTimeLeft(remaining);
      if (remaining <= 0) {
        handleSubmit();
      }
    };

    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [quiz.state, quiz.expiresAt]); // eslint-disable-line react-hooks/exhaustive-deps

  // Auto-focus first input when quiz starts
  useEffect(() => {
    if (quiz.sessionId && inputRefs.current[0]) {
      inputRefs.current[0].focus();
    }
  }, [quiz.sessionId]);

  const updateAnswer = useCallback(
    (index: number, updates: Partial<AnswerState>) => {
      setAnswers((prev) => {
        const next = [...prev];
        next[index] = { ...next[index], ...updates };
        return next;
      });
    },
    []
  );

  const handleKeyDown = useCallback(
    (index: number) => {
      updateAnswer(index, {
        tracking: {
          ...answers[index].tracking,
          keystrokes: answers[index].tracking.keystrokes + 1,
        },
      });
    },
    [answers, updateAnswer]
  );

  const handlePaste = useCallback(
    (index: number) => {
      updateAnswer(index, {
        tracking: { ...answers[index].tracking, pasted: true },
      });
    },
    [answers, updateAnswer]
  );

  const handleBlur = useCallback(
    (index: number) => {
      focusLostStart.current[index] = Date.now();
    },
    []
  );

  const handleFocus = useCallback(
    (index: number) => {
      const start = focusLostStart.current[index];
      if (start) {
        const elapsed = Date.now() - start;
        updateAnswer(index, {
          tracking: {
            ...answers[index].tracking,
            focusLostMs: answers[index].tracking.focusLostMs + elapsed,
          },
        });
        delete focusLostStart.current[index];
      }
    },
    [answers, updateAnswer]
  );

  const handleInputChange = useCallback(
    (index: number, value: string) => {
      updateAnswer(index, { text: value });
    },
    [updateAnswer]
  );

  const handleInputSubmit = useCallback(
    (index: number) => {
      if (!answers[index].text.trim()) return;

      updateAnswer(index, {
        answeredAt: new Date(),
        submitted: true,
      });

      // Move to next empty input
      if (index < 4) {
        setActiveIndex(index + 1);
        setTimeout(() => inputRefs.current[index + 1]?.focus(), 50);
      }
    },
    [answers, updateAnswer]
  );

  const handleSubmit = useCallback(async () => {
    const filledAnswers = answers
      .map((a, i) => ({
        text: a.text.trim() || `unanswered-${i}`,
        answeredAt: a.answeredAt || new Date(),
        tracking: a.tracking,
      }));

    const result = await quiz.submitAnswers(filledAnswers);
    if (result) {
      onComplete(result.final_price);
    }
  }, [answers, quiz, onComplete]);

  const allAnswered = answers.every((a) => a.text.trim().length > 0);
  const answeredCount = answers.filter((a) => a.text.trim().length > 0).length;

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const isUrgent = timeLeft <= 30;

  return (
    <div className={styles.overlay} onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className={styles.modal}>
        {/* Header */}
        <div className={styles.header}>
          <h2 className={styles.title}>TRAIL VERIFICATION</h2>
          <button className={styles.closeBtn} onClick={onClose} aria-label="Close">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Timer */}
        {quiz.state === 'active' && (
          <div className={`${styles.timer} ${isUrgent ? styles.timerUrgent : ''}`}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            {formatTime(timeLeft)}
          </div>
        )}

        {/* Body */}
        <div className={styles.body}>
          {quiz.state === 'active' && quiz.sessionId && (
            <>
              <p className={styles.prompt}>
                Name 5 mountains you&apos;ve hiked recently.
              </p>
              <p className={styles.subtext}>
                Your answers determine the price you pay.
              </p>

              <div className={styles.inputs}>
                {answers.map((answer, i) => (
                  <div key={i} className={styles.inputRow}>
                    <span className={styles.inputNumber}>{i + 1}.</span>
                    <input
                      ref={(el) => { inputRefs.current[i] = el; }}
                      type="text"
                      className={`${styles.input} ${answer.submitted ? styles.inputSubmitted : ''}`}
                      placeholder="Mountain name..."
                      value={answer.text}
                      onChange={(e) => handleInputChange(i, e.target.value)}
                      onKeyDown={(e) => {
                        handleKeyDown(i);
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          handleInputSubmit(i);
                        }
                      }}
                      onPaste={() => handlePaste(i)}
                      onBlur={() => handleBlur(i)}
                      onFocus={() => handleFocus(i)}
                      disabled={quiz.state !== 'active'}
                      autoComplete="off"
                      autoCorrect="off"
                      spellCheck={false}
                    />
                    {answer.submitted && (
                      <svg className={styles.checkIcon} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    )}
                  </div>
                ))}
              </div>

              <div className={styles.progress}>
                {answeredCount}/5 answered
              </div>

              <button
                className={styles.submitBtn}
                onClick={handleSubmit}
                disabled={!allAnswered}
              >
                {allAnswered ? 'Submit Answers' : `Answer all 5 to continue`}
              </button>
            </>
          )}

          {quiz.state === 'submitting' && (
            <div className={styles.loading}>
              <div className={styles.spinner} />
              <p>Analyzing your trail knowledge...</p>
            </div>
          )}

          {quiz.state === 'result' && quiz.result && (
            <div className={styles.result}>
              <p className={styles.resultMessage}>{quiz.result.message}</p>

              <div className={styles.priceResult}>
                <span className={styles.resultLabel}>Your price</span>
                <span className={styles.resultPrice}>
                  ${quiz.result.final_price.toFixed(2)}
                </span>
                {quiz.result.surcharge_pct > 0 && (
                  <span className={styles.surcharge}>
                    +{quiz.result.surcharge_pct}% surcharge applied
                  </span>
                )}
              </div>

              <button className={styles.submitBtn} onClick={onClose}>
                Continue
              </button>
            </div>
          )}

          {quiz.state === 'active' && !quiz.sessionId && (
            <div className={styles.loading}>
              <div className={styles.spinner} />
              <p>Preparing your quiz...</p>
            </div>
          )}

          {quiz.error && (
            <p className={styles.error}>{quiz.error}</p>
          )}
        </div>
      </div>
    </div>
  );
}
