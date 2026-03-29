import { CartIcon } from './CartIcon';
import styles from './Header.module.css';

export function Header() {
  return (
    <header className={styles.header}>
      <TopBar />
      <MainNav />
      <Breadcrumbs />
    </header>
  );
}

function TopBar() {
  return (
    <div className={styles.topBar}>
      <div className={styles.topBarInner}>
        <nav className={styles.topBarLeft}>
          <a href="/" className={styles.topBarLink + ' ' + styles.topBarLinkActive}>ARC&apos;TERYX</a>
          <a href="/outlet" className={styles.topBarLink}>OUTLET</a>
          <a href="/veilance" className={styles.topBarLink}>VEILANCE</a>
          <a href="/resale" className={styles.topBarLink}>RESALE</a>
        </nav>
        <div className={styles.topBarCenter}>
          <span>New spring arrivals | Free shipping &amp; returns</span>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className={styles.chevronDown}>
            <path d="M2 4L6 8L10 4" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <div className={styles.topBarRight}>
          <a href="/find-a-store" className={styles.topBarLink}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <path d="M3 9h18M9 3v18"/>
            </svg>
            Find a store
          </a>
          <span className={styles.topBarFlag}>🇺🇸</span>
          <span className={styles.topBarLink}>EN</span>
          <a href="/help" className={styles.topBarLink}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3M12 17h.01"/>
            </svg>
          </a>
        </div>
      </div>
    </div>
  );
}

function MainNav() {
  return (
    <nav className={styles.mainNav}>
      <div className={styles.mainNavInner}>
        <a href="/" className={styles.logo} aria-label="Arc'teryx Home">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/images/logo.png" alt="Arc'teryx" className={styles.logoImg} />
          <span className={styles.logoText}>ARC&apos;TERYX</span>
        </a>

        <div className={styles.navLinks}>
          <a href="/women" className={styles.navLink}>WOMEN</a>
          <a href="/men" className={styles.navLink}>MEN</a>
          <a href="/footwear" className={styles.navLink}>FOOTWEAR</a>
          <a href="/discover" className={styles.navLink}>DISCOVER</a>
        </div>

        <div className={styles.navIcons}>
          <button className={styles.iconBtn} aria-label="Search">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
              <circle cx="11" cy="11" r="8"/>
              <path d="M21 21l-4.35-4.35"/>
            </svg>
          </button>
          <button className={styles.iconBtn} aria-label="Account">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </button>
          <CartIcon />
        </div>
      </div>
    </nav>
  );
}

function Breadcrumbs() {
  return (
    <div className={styles.breadcrumbs}>
      <div className={styles.breadcrumbsInner}>
        <a href="/" className={styles.breadcrumbLink}>Arc&apos;teryx</a>
        <span className={styles.breadcrumbSep}>&gt;</span>
        <a href="/accessories" className={styles.breadcrumbLink}>Accessories</a>
        <span className={styles.breadcrumbSep}>&gt;</span>
        <span className={styles.breadcrumbCurrent}>Bird Head Toque</span>
      </div>
    </div>
  );
}
