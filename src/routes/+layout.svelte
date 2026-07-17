<script lang="ts">
  import '../app.css';
  import Navbar from '$lib/components/layout/Navbar.svelte';
  import Footer from '$lib/components/layout/Footer.svelte';
  import CartDrawer from '$lib/components/layout/CartDrawer.svelte';
  import ScrollToTop from '$lib/components/layout/ScrollToTop.svelte';
  import { Toaster } from '$lib/components/ui/sonner';
  import { page } from '$app/state';
  import { cart } from '$lib/stores/cart.svelte';

  let { children } = $props();

  // Determine if we're on an admin page (different layout)
  const isAdmin = $derived(page.url.pathname.startsWith('/admin'));

  // Sync user-specific cart key reactively on authentication updates
  $effect(() => {
    cart.initForUser(page.data.user?.id || null);
  });
</script>

<svelte:head>
  <meta name="description" content="PerfumeDecantsBD — Premium luxury perfume decants delivered to your door. Authentic fragrances, expertly curated." />
</svelte:head>

{#if !isAdmin}
  <Navbar />
{/if}

<main class={isAdmin ? '' : 'min-h-screen pt-16 lg:pt-20'}>
  {@render children()}
</main>

{#if !isAdmin}
  <Footer />
  <CartDrawer />
  <ScrollToTop />
{/if}

<Toaster richColors position="top-right" duration={2000} />
