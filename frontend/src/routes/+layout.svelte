<!--
  PerfumeDecantBD — Root Layout
  Global layout with Navbar and Footer wrapping all pages.
-->
<script lang="ts">
  import '../app.css';
  import Navbar from '$lib/components/layout/Navbar.svelte';
  import Footer from '$lib/components/layout/Footer.svelte';

  let { children } = $props();
</script>

<svelte:head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="PerfumeDecantBD — Discover luxury fragrances from world-renowned perfume houses. Premium decants, authentic bottles, and curated collections." />
  <title>PerfumeDecantBD — Luxury Perfume E-commerce</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
</svelte:head>

<div class="min-h-screen flex flex-col">
  <Navbar />
  <main class="flex-1">
    {@render children()}
  </main>
  <Footer />
</div>
