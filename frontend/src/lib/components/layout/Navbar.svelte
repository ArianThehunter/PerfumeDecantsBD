<!--
  PerfumeDecantBD — Navigation Bar
  Luxury navigation with transparent-to-solid scroll effect.
-->
<script lang="ts">
  import { onMount } from 'svelte';

  let scrolled = $state(false);
  let mobileMenuOpen = $state(false);
  let searchOpen = $state(false);

  onMount(() => {
    const handleScroll = () => {
      scrolled = window.scrollY > 50;
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  });

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/products', label: 'Shop' },
    { href: '/products?collection=new-arrivals', label: 'New Arrivals' },
    { href: '/products?collection=best-sellers', label: 'Best Sellers' },
    { href: '/products?is_featured=true', label: 'Collections' },
  ];
</script>

<header
  class="fixed top-0 left-0 right-0 z-50 transition-all duration-500"
  class:bg-white={scrolled}
  class:shadow-md={scrolled}
  class:bg-transparent={!scrolled}
>
  <!-- Top Bar -->
  <div class="bg-gradient-luxury text-white text-center text-xs tracking-[0.2em] uppercase py-2 px-4 font-light">
    ✦ Free Shipping on Orders Over ৳5,000 ✦ Authentic Luxury Fragrances ✦
  </div>

  <!-- Main Nav -->
  <nav class="container-luxury flex items-center justify-between py-4">
    <!-- Logo -->
    <a href="/" class="flex items-center gap-3 group">
      <div class="w-10 h-10 rounded-full bg-gradient-gold flex items-center justify-center text-white font-bold text-lg font-[var(--font-heading)]">
        P
      </div>
      <div>
        <span
          class="text-xl font-bold tracking-wider font-[var(--font-heading)] transition-colors duration-300"
          class:text-white={!scrolled}
          class:text-warm-950={scrolled}
        >
          PerfumeDecant
        </span>
        <span class="text-gradient-gold text-xl font-bold font-[var(--font-heading)]">BD</span>
      </div>
    </a>

    <!-- Desktop Nav Links -->
    <div class="hidden lg:flex items-center gap-8">
      {#each navLinks as link}
        <a
          href={link.href}
          class="text-sm font-medium tracking-wider uppercase transition-all duration-300 hover:text-primary-500 relative group {scrolled ? 'text-warm-700' : 'text-white/90'}"
        >
          {link.label}
          <span class="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-gold transition-all duration-300 group-hover:w-full"></span>
        </a>
      {/each}
    </div>

    <!-- Right Actions -->
    <div class="flex items-center gap-4">
      <!-- Search -->
      <button
        onclick={() => searchOpen = !searchOpen}
        class="p-2 transition-colors duration-300 hover:text-primary-500"
        class:text-white={!scrolled}
        class:text-warm-700={scrolled}
        aria-label="Search"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>
      </button>

      <!-- Wishlist -->
      <a
        href="/account/wishlist"
        class="p-2 transition-colors duration-300 hover:text-primary-500 hidden sm:block"
        class:text-white={!scrolled}
        class:text-warm-700={scrolled}
        aria-label="Wishlist"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
        </svg>
      </a>

      <!-- User -->
      <a
        href="/auth/login"
        class="p-2 transition-colors duration-300 hover:text-primary-500 hidden sm:block"
        class:text-white={!scrolled}
        class:text-warm-700={scrolled}
        aria-label="Account"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
        </svg>
      </a>

      <!-- Cart -->
      <a
        href="/cart"
        class="relative p-2 transition-colors duration-300 hover:text-primary-500"
        class:text-white={!scrolled}
        class:text-warm-700={scrolled}
        aria-label="Cart"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
        </svg>
        <span class="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-gradient-gold text-[10px] font-bold text-white flex items-center justify-center">
          0
        </span>
      </a>

      <!-- Mobile Menu Toggle -->
      <button
        onclick={() => mobileMenuOpen = !mobileMenuOpen}
        class="lg:hidden p-2 transition-colors duration-300"
        class:text-white={!scrolled}
        class:text-warm-700={scrolled}
        aria-label="Menu"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          {#if mobileMenuOpen}
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          {:else}
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9h16.5m-16.5 6.75h16.5" />
          {/if}
        </svg>
      </button>
    </div>
  </nav>

  <!-- Search Bar Overlay -->
  {#if searchOpen}
    <div class="absolute top-full left-0 right-0 bg-white shadow-xl p-6 animate-fade-in">
      <div class="container-luxury flex items-center gap-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-warm-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>
        <input
          type="text"
          placeholder="Search fragrances, brands, notes..."
          class="flex-1 text-lg border-none outline-none bg-transparent font-[var(--font-body)] text-warm-800 placeholder:text-warm-400"
          autofocus
        />
        <button onclick={() => searchOpen = false} class="text-warm-500 hover:text-warm-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  {/if}

  <!-- Mobile Menu -->
  {#if mobileMenuOpen}
    <div class="lg:hidden bg-white shadow-xl border-t border-warm-100 animate-fade-in">
      <div class="container-luxury py-6 space-y-4">
        {#each navLinks as link}
          <a
            href={link.href}
            class="block text-sm font-medium tracking-wider uppercase text-warm-700 hover:text-primary-600 py-2 transition-colors"
            onclick={() => mobileMenuOpen = false}
          >
            {link.label}
          </a>
        {/each}
        <div class="luxury-divider my-4"></div>
        <a href="/auth/login" class="block text-sm font-medium tracking-wider uppercase text-warm-700 py-2">Account</a>
        <a href="/account/wishlist" class="block text-sm font-medium tracking-wider uppercase text-warm-700 py-2">Wishlist</a>
      </div>
    </div>
  {/if}
</header>
