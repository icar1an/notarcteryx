'use client';

import { useState } from 'react';
import { useCart } from '@/hooks/useCart';
import styles from './Cart.module.css';

export function Cart() {
  const { items, removeItem, updateQuantity, totalItems, subtotal } = useCart();
  const [promoOpen, setPromoOpen] = useState(false);

  if (items.length === 0) {
    return (
      <main className={styles.cart}>
        <div className={styles.container}>
          <div className={styles.emptyCart}>
            <h1 className={styles.emptyTitle}>Your cart is empty</h1>
            <p className={styles.emptyText}>
              Items in your cart are not reserved. Complete checkout to secure your gear.
            </p>
            <a href="/" className={styles.continueShopping}>
              Continue shopping
            </a>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className={styles.cart}>
      <div className={styles.container}>
        <p className={styles.notice}>
          Items in your cart are not reserved. Complete checkout to secure your gear.
        </p>

        <div className={styles.grid}>
          {/* Left: Cart Items */}
          <div className={styles.itemsSection}>
            <h1 className={styles.cartTitle}>My cart ({totalItems})</h1>

            <div className={styles.tableHeader}>
              <span className={styles.colItem}>Item</span>
              <span className={styles.colQty}>Quantity</span>
              <span className={styles.colPrice}>Price</span>
              <span className={styles.colRemove}></span>
            </div>

            <div className={styles.divider} />

            {items.map((item) => (
              <div key={`${item.productId}-${item.color}`} className={styles.cartItem}>
                <div className={styles.itemInfo}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={item.image}
                    alt={item.name}
                    className={styles.itemImage}
                  />
                  <div className={styles.itemDetails}>
                    <p className={styles.itemName}>{item.name}</p>
                    <p className={styles.itemMeta}>
                      {item.color}
                      {item.size !== 'NA' && ` (${item.size})`}
                    </p>
                  </div>
                </div>

                <div className={styles.qtyControl}>
                  <button
                    className={styles.qtyBtn}
                    onClick={() =>
                      updateQuantity(item.productId, item.color, item.quantity - 1)
                    }
                    aria-label="Decrease quantity"
                  >
                    &minus;
                  </button>
                  <input
                    type="number"
                    className={styles.qtyInput}
                    value={item.quantity}
                    min={1}
                    onChange={(e) =>
                      updateQuantity(
                        item.productId,
                        item.color,
                        parseInt(e.target.value) || 1
                      )
                    }
                  />
                  <button
                    className={styles.qtyBtn}
                    onClick={() =>
                      updateQuantity(item.productId, item.color, item.quantity + 1)
                    }
                    aria-label="Increase quantity"
                  >
                    +
                  </button>
                </div>

                <span className={styles.itemPrice}>
                  ${(item.price * item.quantity).toFixed(2)}
                </span>

                <button
                  className={styles.removeBtn}
                  onClick={() => removeItem(item.productId, item.color)}
                >
                  Remove
                </button>
              </div>
            ))}

            <div className={styles.divider} />

            <div className={styles.cartFooter}>
              <span className={styles.freeShipping}>
                Free shipping and free returns
              </span>
              <button className={styles.emailCart}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <rect x="2" y="4" width="20" height="16" rx="2" />
                  <path d="M22 4L12 13 2 4" />
                </svg>
                Email my cart
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <path d="M2 4L6 8L10 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </div>
          </div>

          {/* Right: Order Summary */}
          <div className={styles.summarySection}>
            <h2 className={styles.summaryTitle}>Order summary</h2>

            <div className={styles.divider} />

            <div className={styles.summaryRow}>
              <span>Subtotal:</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className={styles.summaryRow}>
              <span className={styles.shippingLabel}>
                Shipping:
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className={styles.infoIcon}>
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 16v-4M12 8h.01" />
                </svg>
              </span>
              <span className={styles.freeText}>Free</span>
            </div>
            <div className={styles.summaryRow}>
              <span>Tax:</span>
              <span className={styles.calcText}>Calculated at checkout</span>
            </div>

            <div className={styles.divider} />

            <div className={`${styles.summaryRow} ${styles.totalRow}`}>
              <span>Estimated total:</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>

            <div className={styles.divider} />

            <button
              className={styles.promoToggle}
              onClick={() => setPromoOpen(!promoOpen)}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z" />
                <line x1="7" y1="7" x2="7.01" y2="7" />
              </svg>
              Have a promo code?
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className={promoOpen ? styles.chevronOpen : ''}>
                <path d="M2 4L6 8L10 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>

            {promoOpen && (
              <div className={styles.promoInput}>
                <input type="text" placeholder="Enter promo code" className={styles.promoField} />
                <button className={styles.promoApply}>Apply</button>
              </div>
            )}

            <button className={styles.checkoutBtn}>
              Continue to checkout
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0110 0v4" />
              </svg>
            </button>

            <div className={styles.paymentMethods}>
              <p className={styles.paymentLabel}>Available payment methods</p>
              <div className={styles.paymentIcons}>
                {['Apple Pay', 'PayPal', 'Mastercard', 'SVS', 'Visa', 'G Pay', 'Amex', 'Klarna'].map(
                  (method) => (
                    <span key={method} className={styles.paymentBadge}>
                      {method}
                    </span>
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
