<script lang="ts">
  import { page } from '$app/state';
  import { cart } from '$lib/stores/cart.svelte';
  import { theme } from '$lib/stores/theme.svelte';
  import { ShoppingBag, Menu, X, Search, User, Sun, Moon, Heart, ChevronDown } from '@lucide/svelte';

  let scrolled = $state(false);
  let mobileMenuOpen = $state(false);
  let searchOpen = $state(false);

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/shop', label: 'Shop' },
    { href: '/about', label: 'About' },
    { href: '/contact', label: 'Contact' }
  ];

  function handleScroll() {
    scrolled = window.scrollY > 20;
  }

  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }

  function closeMobileMenu() {
    mobileMenuOpen = false;
    document.body.style.overflow = '';
  }

  $effect(() => {
    // Close mobile menu on route change
    closeMobileMenu();
  });
</script>

<svelte:window onscroll={handleScroll} />

<header
  class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 glass shadow-sm"
>
  <nav class="container-luxury" aria-label="Main navigation">
    <div class="flex h-16 items-center justify-between lg:h-20">
      <!-- Logo -->
      <a href="/" class="flex items-center gap-2 group" aria-label="PerfumeDecantsBD Home">
        <img
          src="/logo.jpg"
          alt="PerfumeDecantsBD"
          class="h-10 w-10 rounded-full object-cover transition-transform duration-300 group-hover:scale-105 lg:h-12 lg:w-12"
        />
        <div class="hidden sm:block">
          <span class="font-heading text-lg font-bold tracking-wide text-burgundy-800 dark:text-cream-200 lg:text-xl">
            PerfumeDecants
          </span>
          <span class="font-heading text-lg font-bold text-gold-500 lg:text-xl">BD</span>
        </div>
      </a>

      <!-- Desktop Navigation -->
      <div class="hidden items-center gap-8 lg:flex">
        {#each navLinks as link}
          <a
            href={link.href}
            class="relative text-sm font-medium tracking-wide uppercase transition-colors duration-200 hover:text-burgundy-700 dark:hover:text-gold-400 {page.url
              .pathname === link.href
              ? 'text-burgundy-700 dark:text-gold-400'
              : 'text-gray-700 dark:text-gray-300'}"
          >
            {link.label}
            {#if page.url.pathname === link.href}
              <span
                class="absolute -bottom-1 left-0 h-0.5 w-full bg-gradient-to-r from-burgundy-600 to-gold-500 rounded-full"
              ></span>
            {/if}
          </a>
        {/each}
      </div>

      <!-- Right Actions -->
      <div class="flex items-center gap-1 sm:gap-2">
        <!-- Search Button -->
        <button
          onclick={() => (searchOpen = !searchOpen)}
          class="btn-press flex h-10 w-10 items-center justify-center rounded-full text-gray-700 transition-colors hover:bg-burgundy-50 hover:text-burgundy-700 dark:text-gray-300 dark:hover:bg-burgundy-950 dark:hover:text-gold-400"
          aria-label="Search"
        >
          <Search class="h-5 w-5" />
        </button>

        <!-- Wishlist Placeholder -->
        <a
          href="/shop"
          class="btn-press hidden h-10 w-10 items-center justify-center rounded-full text-gray-700 transition-colors hover:bg-burgundy-50 hover:text-burgundy-700 dark:text-gray-300 dark:hover:bg-burgundy-950 dark:hover:text-gold-400 sm:flex"
          aria-label="Wishlist"
        >
          <Heart class="h-5 w-5" />
        </a>

        <!-- Theme Toggle -->
        <button
          onclick={() => theme.toggle()}
          class="btn-press flex h-10 w-10 items-center justify-center rounded-full text-gray-700 transition-colors hover:bg-burgundy-50 hover:text-burgundy-700 dark:text-gray-300 dark:hover:bg-burgundy-950 dark:hover:text-gold-400"
          aria-label="Toggle theme"
        >
          {#if theme.isDark}
            <Sun class="h-5 w-5" />
          {:else}
            <Moon class="h-5 w-5" />
          {/if}
        </button>

        <!-- Account -->
        <a
          href="/account"
          class="btn-press hidden h-10 w-10 items-center justify-center rounded-full text-gray-700 transition-colors hover:bg-burgundy-50 hover:text-burgundy-700 dark:text-gray-300 dark:hover:bg-burgundy-950 dark:hover:text-gold-400 sm:flex"
          aria-label="Account"
        >
          <User class="h-5 w-5" />
        </a>

        <!-- Cart Button -->
        <button
          onclick={() => cart.openCart()}
          class="btn-press relative flex h-10 w-10 items-center justify-center rounded-full text-gray-700 transition-colors hover:bg-burgundy-50 hover:text-burgundy-700 dark:text-gray-300 dark:hover:bg-burgundy-950 dark:hover:text-gold-400"
          aria-label="Shopping cart ({cart.itemCount} items)"
        >
          <ShoppingBag class="h-5 w-5" />
          {#if cart.itemCount > 0}
            <span
              class="absolute -right-0.5 -top-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-burgundy-700 text-[10px] font-bold text-white animate-scale-in"
            >
              {cart.itemCount > 99 ? '99+' : cart.itemCount}
            </span>
          {/if}
        </button>

        <!-- Mobile Menu Toggle -->
        <button
          onclick={toggleMobileMenu}
          class="btn-press flex h-10 w-10 items-center justify-center rounded-full text-gray-700 transition-colors hover:bg-burgundy-50 hover:text-burgundy-700 dark:text-gray-300 dark:hover:bg-burgundy-950 lg:hidden"
          aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={mobileMenuOpen}
        >
          {#if mobileMenuOpen}
            <X class="h-5 w-5" />
          {:else}
            <Menu class="h-5 w-5" />
          {/if}
        </button>
      </div>
    </div>

    <!-- Search Bar (expandable) -->
    {#if searchOpen}
      <div class="animate-slide-down border-t border-gray-100 pb-4 pt-2 dark:border-gray-800">
        <form action="/shop" method="get" class="relative">
          <Search class="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <input
            type="search"
            name="search"
            placeholder="Search luxury perfumes..."
            class="w-full rounded-full border border-gray-200 bg-white/80 py-3 pl-11 pr-4 text-sm backdrop-blur-sm transition-all focus:border-burgundy-400 focus:outline-none focus:ring-2 focus:ring-burgundy-200 dark:border-gray-700 dark:bg-gray-900/80 dark:text-white dark:focus:border-gold-500 dark:focus:ring-gold-500/20"
          />
        </form>
      </div>
    {/if}
  </nav>
</header>

<!-- Mobile Menu Overlay -->
{#if mobileMenuOpen}
  <div class="fixed inset-0 z-40 lg:hidden">
    <!-- Backdrop -->
    <button
      class="absolute inset-0 bg-black/50 backdrop-blur-sm animate-fade-in"
      onclick={closeMobileMenu}
      aria-label="Close menu"
      tabindex="-1"
    ></button>

    <!-- Menu Panel -->
    <div
      class="absolute right-0 top-0 h-full w-80 max-w-[85vw] bg-white shadow-2xl animate-slide-down dark:bg-gray-950"
    >
      <div class="flex h-16 items-center justify-between px-6">
        <span class="font-heading text-lg font-bold text-burgundy-800 dark:text-cream-200">Menu</span>
        <button
          onclick={closeMobileMenu}
          class="flex h-10 w-10 items-center justify-center rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"
          aria-label="Close menu"
        >
          <X class="h-5 w-5" />
        </button>
      </div>

      <nav class="flex flex-col px-6">
        {#each navLinks as link}
          <a
            href={link.href}
            onclick={closeMobileMenu}
            class="border-b border-gray-100 py-4 text-base font-medium transition-colors hover:text-burgundy-700 dark:border-gray-800 dark:hover:text-gold-400 {page
              .url.pathname === link.href
              ? 'text-burgundy-700 dark:text-gold-400'
              : 'text-gray-700 dark:text-gray-300'}"
          >
            {link.label}
          </a>
        {/each}

        <div class="mt-6 space-y-3">
          <a
            href="/account"
            onclick={closeMobileMenu}
            class="flex items-center gap-3 rounded-xl bg-gray-50 px-4 py-3 text-sm font-medium text-gray-700 transition-colors hover:bg-burgundy-50 hover:text-burgundy-700 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-burgundy-950"
          >
            <User class="h-5 w-5" />
            My Account
          </a>
          <a
            href="/auth/login"
            onclick={closeMobileMenu}
            class="flex items-center justify-center rounded-xl bg-burgundy-700 px-4 py-3 text-sm font-medium text-white transition-colors hover:bg-burgundy-800"
          >
            Sign In
          </a>
        </div>
      </nav>
    </div>
  </div>
{/if}
