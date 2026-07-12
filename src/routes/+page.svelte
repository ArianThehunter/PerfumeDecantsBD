<script lang="ts">
  import { ArrowRight, Star, Shield, Truck, Award, Sparkles, Quote } from '@lucide/svelte';
  import { Button } from '$lib/components/ui/button';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  const featuredProducts = $derived(data.featuredProducts);
  const bestSellers = $derived(data.bestSellers);
  const categories = $derived(data.categories);

  const testimonials = [
    { name: 'Ariana K.', text: 'Absolutely authentic fragrances! The decants are perfect for trying luxury scents before committing to a full bottle.', rating: 5 },
    { name: 'Rafiq S.', text: 'Best perfume decant service in Bangladesh. Fast delivery and amazing packaging. Highly recommend!', rating: 5 },
    { name: 'Nusrat J.', text: 'I\'ve ordered multiple times and every experience has been flawless. The quality is unmatched.', rating: 5 }
  ];

  const features = [
    { icon: Shield, title: '100% Authentic', desc: 'Every fragrance is sourced directly from authorized distributors' },
    { icon: Truck, title: 'Fast Delivery', desc: 'Nationwide delivery within 2-3 business days' },
    { icon: Award, title: 'Premium Quality', desc: 'Carefully decanted and packaged with luxury in mind' },
    { icon: Sparkles, title: 'Try Before You Buy', desc: 'Experience luxury fragrances without the full bottle price' }
  ];

  function formatPrice(price: number) {
    return `৳${price.toLocaleString()}`;
  }
</script>

<svelte:head>
  <title>PerfumeDecantsBD — Premium Luxury Perfume Decants</title>
</svelte:head>

<!-- Hero Section -->
<section class="relative min-h-[90vh] overflow-hidden bg-burgundy-950 flex items-center">
  <!-- Background Pattern -->
  <div class="absolute inset-0 opacity-10">
    <div class="absolute inset-0" style="background-image: radial-gradient(circle at 25% 25%, rgba(212, 168, 85, 0.3) 0%, transparent 50%), radial-gradient(circle at 75% 75%, rgba(122, 27, 62, 0.3) 0%, transparent 50%)"></div>
  </div>

  <!-- Cover Image Overlay -->
  <div class="absolute inset-0">
    <img src="/cover.png" alt="" class="h-full w-full object-cover opacity-20" />
    <div class="absolute inset-0 bg-gradient-to-r from-burgundy-950 via-burgundy-950/90 to-burgundy-950/70"></div>
  </div>

  <div class="container-luxury relative z-10 py-20">
    <div class="mx-auto max-w-3xl text-center">
      <div class="animate-fade-in">
        <span class="inline-block rounded-full border border-gold-500/30 bg-gold-500/10 px-4 py-1.5 text-xs font-medium uppercase tracking-widest text-gold-400">
          Premium Fragrance Decants
        </span>
      </div>

      <h1 class="mt-6 font-heading text-4xl font-bold leading-tight text-white sm:text-5xl md:text-6xl lg:text-7xl animate-slide-up" style="animation-delay: 0.1s; opacity: 0;">
        Discover Your
        <span class="text-gradient bg-gradient-to-r from-gold-400 to-gold-600 bg-clip-text text-transparent">
          Signature Scent
        </span>
      </h1>

      <p class="mt-6 text-base leading-relaxed text-cream-300/70 sm:text-lg animate-slide-up" style="animation-delay: 0.2s; opacity: 0;">
        Experience the world's finest luxury perfumes without the full-bottle commitment.
        Authentic decants, expertly curated, delivered to your doorstep in Bangladesh.
      </p>

      <div class="mt-10 flex flex-col gap-4 sm:flex-row sm:justify-center animate-slide-up" style="animation-delay: 0.3s; opacity: 0;">
        <a
          href="/shop"
          class="btn-press inline-flex items-center justify-center gap-2 rounded-xl bg-gold-500 px-8 py-3.5 text-sm font-semibold text-burgundy-950 transition-all hover:bg-gold-400 hover:shadow-lg hover:shadow-gold-500/25"
        >
          Explore Collection
          <ArrowRight class="h-4 w-4" />
        </a>
        <a
          href="/about"
          class="btn-press inline-flex items-center justify-center gap-2 rounded-xl border border-cream-300/20 px-8 py-3.5 text-sm font-medium text-cream-200 transition-all hover:bg-white/5"
        >
          Our Story
        </a>
      </div>

      <!-- Stats -->
      <div class="mt-16 grid grid-cols-3 gap-8 border-t border-cream-300/10 pt-10 animate-slide-up" style="animation-delay: 0.4s; opacity: 0;">
        <div>
          <p class="font-heading text-2xl font-bold text-gold-400 sm:text-3xl">500+</p>
          <p class="mt-1 text-xs text-cream-300/50 sm:text-sm">Happy Customers</p>
        </div>
        <div>
          <p class="font-heading text-2xl font-bold text-gold-400 sm:text-3xl">50+</p>
          <p class="mt-1 text-xs text-cream-300/50 sm:text-sm">Premium Brands</p>
        </div>
        <div>
          <p class="font-heading text-2xl font-bold text-gold-400 sm:text-3xl">100%</p>
          <p class="mt-1 text-xs text-cream-300/50 sm:text-sm">Authentic</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Scroll Indicator -->
  <div class="absolute bottom-8 left-1/2 -translate-x-1/2 animate-float">
    <div class="h-10 w-6 rounded-full border-2 border-cream-300/30 p-1">
      <div class="h-2 w-full rounded-full bg-gold-400 animate-pulse-soft"></div>
    </div>
  </div>
</section>

<!-- Featured Products -->
<section class="section-padding bg-[var(--bg-primary)]">
  <div class="container-luxury">
    <div class="text-center">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">Curated Selection</span>
      <h2 class="mt-2 font-heading text-3xl font-bold sm:text-4xl">Featured Fragrances</h2>
      <p class="mx-auto mt-3 max-w-lg text-sm text-[var(--text-muted)]">
        Hand-picked luxury perfumes that define elegance and sophistication
      </p>
    </div>

    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {#each featuredProducts as product}
        {@const productImg = product.product_images?.[0]?.url || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'}
        <a href="/product/{product.slug}" class="group card-premium overflow-hidden">
          <div class="relative aspect-[4/5] overflow-hidden bg-gray-100 dark:bg-gray-900">
            <img
              src={productImg}
              alt={product.name}
              class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
              loading="lazy"
            />
            {#if product.discount_price}
              <span class="absolute left-3 top-3 rounded-full bg-burgundy-700 px-2.5 py-1 text-[10px] font-bold text-white">
                SALE
              </span>
            {/if}
          </div>
          <div class="p-4">
            <p class="text-xs font-medium uppercase tracking-wider text-[var(--text-muted)]">{product.brand}</p>
            <h3 class="mt-1 font-heading text-lg font-semibold group-hover:text-burgundy-700 dark:group-hover:text-gold-400 transition-colors">{product.name}</h3>
            <div class="mt-1 flex items-center gap-1">
              {#each Array(5) as _, i}
                <Star class="h-3 w-3 {i < Math.floor(product.rating) ? 'fill-gold-400 text-gold-400' : 'text-gray-300'}" />
              {/each}
              <span class="ml-1 text-xs text-[var(--text-muted)]">{product.rating}</span>
            </div>
            <div class="mt-2 flex items-center gap-2">
              {#if product.discount_price}
                <span class="font-heading text-lg font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(product.discount_price)}</span>
                <span class="text-sm text-gray-400 line-through">{formatPrice(product.price)}</span>
              {:else}
                <span class="font-heading text-lg font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(product.price)}</span>
              {/if}
            </div>
          </div>
        </a>
      {/each}
    </div>

    <div class="mt-10 text-center">
      <a
        href="/shop"
        class="btn-press inline-flex items-center gap-2 rounded-xl border-2 border-burgundy-700 px-8 py-3 text-sm font-semibold text-burgundy-700 transition-all hover:bg-burgundy-700 hover:text-white dark:border-gold-500 dark:text-gold-400 dark:hover:bg-gold-500 dark:hover:text-burgundy-950"
      >
        View All Products
        <ArrowRight class="h-4 w-4" />
      </a>
    </div>
  </div>
</section>

<!-- Categories -->
<section class="section-padding bg-[var(--bg-secondary)]">
  <div class="container-luxury">
    <div class="text-center">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">Browse By</span>
      <h2 class="mt-2 font-heading text-3xl font-bold sm:text-4xl">Shop Categories</h2>
    </div>

    <div class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
      {#each categories as cat}
        <a
          href="/shop?category={cat.slug}"
          class="group relative aspect-[3/4] overflow-hidden rounded-2xl"
        >
          <img
            src={cat.image_url}
            alt={cat.name}
            class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
            loading="lazy"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"></div>
          <div class="absolute bottom-0 left-0 right-0 p-4">
            <h3 class="font-heading text-lg font-bold text-white">{cat.name}</h3>
            <p class="text-xs text-cream-300/70">{cat.description || 'Explore collection'}</p>
          </div>
        </a>
      {/each}
    </div>
  </div>
</section>

<!-- Best Sellers -->
<section class="section-padding bg-[var(--bg-primary)]">
  <div class="container-luxury">
    <div class="text-center">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">Most Loved</span>
      <h2 class="mt-2 font-heading text-3xl font-bold sm:text-4xl">Best Sellers</h2>
      <p class="mx-auto mt-3 max-w-lg text-sm text-[var(--text-muted)]">
        Our customers' absolute favorites — tried, tested, and loved
      </p>
    </div>

    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {#each bestSellers as product}
        {@const productImg = product.product_images?.[0]?.url || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'}
        <a href="/product/{product.slug}" class="group card-premium overflow-hidden">
          <div class="relative aspect-[4/5] overflow-hidden bg-gray-100 dark:bg-gray-900">
            <img
              src={productImg}
              alt={product.name}
              class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
              loading="lazy"
            />
            <span class="absolute left-3 top-3 rounded-full bg-gold-500 px-2.5 py-1 text-[10px] font-bold text-burgundy-950">
              BESTSELLER
            </span>
          </div>
          <div class="p-4">
            <p class="text-xs font-medium uppercase tracking-wider text-[var(--text-muted)]">{product.brand}</p>
            <h3 class="mt-1 font-heading text-lg font-semibold group-hover:text-burgundy-700 dark:group-hover:text-gold-400 transition-colors">{product.name}</h3>
            <div class="mt-1 flex items-center gap-1">
              {#each Array(5) as _, i}
                <Star class="h-3 w-3 {i < Math.floor(product.rating) ? 'fill-gold-400 text-gold-400' : 'text-gray-300'}" />
              {/each}
              <span class="ml-1 text-xs text-[var(--text-muted)]">{product.rating}</span>
            </div>
            <p class="mt-2 font-heading text-lg font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(product.price)}</p>
          </div>
        </a>
      {/each}
    </div>
  </div>
</section>

<!-- Brand Story -->
<section class="relative overflow-hidden bg-burgundy-950 py-20">
  <div class="absolute inset-0 opacity-5">
    <img src="/cover.png" alt="" class="h-full w-full object-cover" />
  </div>
  <div class="container-luxury relative z-10">
    <div class="mx-auto max-w-3xl text-center">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-400">Our Story</span>
      <h2 class="mt-4 font-heading text-3xl font-bold text-white sm:text-4xl">
        Born from a Passion for Fine Fragrances
      </h2>
      <p class="mt-6 text-base leading-relaxed text-cream-300/70">
        PerfumeDecantsBD was founded with a simple mission: to make luxury fragrances accessible to everyone in Bangladesh.
        We believe everyone deserves to experience the artistry of world-class perfumery without the barrier of full-bottle prices.
        Each decant is carefully prepared with love and attention to detail, ensuring you receive the same premium experience
        as the original bottle.
      </p>
      <a
        href="/about"
        class="mt-8 btn-press inline-flex items-center gap-2 rounded-xl border border-gold-500/30 px-8 py-3 text-sm font-medium text-gold-400 transition-all hover:bg-gold-500/10"
      >
        Read More
        <ArrowRight class="h-4 w-4" />
      </a>
    </div>
  </div>
</section>

<!-- Why Choose Us -->
<section class="section-padding bg-[var(--bg-primary)]">
  <div class="container-luxury">
    <div class="text-center">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">Why Us</span>
      <h2 class="mt-2 font-heading text-3xl font-bold sm:text-4xl">Why Choose PerfumeDecantsBD</h2>
    </div>

    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {#each features as feature}
        <div class="card-premium p-6 text-center">
          <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
            <feature.icon class="h-7 w-7" />
          </div>
          <h3 class="mt-4 font-heading text-lg font-semibold">{feature.title}</h3>
          <p class="mt-2 text-sm text-[var(--text-muted)]">{feature.desc}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- Testimonials -->
<section class="section-padding bg-[var(--bg-secondary)]">
  <div class="container-luxury">
    <div class="text-center">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">Testimonials</span>
      <h2 class="mt-2 font-heading text-3xl font-bold sm:text-4xl">What Our Customers Say</h2>
    </div>

    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {#each testimonials as t}
        <div class="card-premium p-6">
          <Quote class="h-8 w-8 text-gold-400/30" />
          <p class="mt-3 text-sm leading-relaxed text-[var(--text-secondary)]">"{t.text}"</p>
          <div class="mt-4 flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-full bg-burgundy-100 font-heading font-bold text-burgundy-700 dark:bg-burgundy-900 dark:text-gold-400">
              {t.name[0]}
            </div>
            <div>
              <p class="text-sm font-semibold">{t.name}</p>
              <div class="flex gap-0.5">
                {#each Array(t.rating) as _}
                  <Star class="h-3 w-3 fill-gold-400 text-gold-400" />
                {/each}
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- CTA Banner -->
<section class="relative overflow-hidden bg-gradient-to-br from-burgundy-800 via-burgundy-900 to-burgundy-950 py-20">
  <div class="absolute inset-0 opacity-10" style="background-image: radial-gradient(circle at 30% 50%, rgba(212, 168, 85, 0.4) 0%, transparent 60%)"></div>
  <div class="container-luxury relative z-10 text-center">
    <h2 class="font-heading text-3xl font-bold text-white sm:text-4xl">
      Ready to Find Your Perfect Fragrance?
    </h2>
    <p class="mx-auto mt-4 max-w-lg text-base text-cream-300/70">
      Browse our curated collection of luxury perfume decants and start your fragrance journey today.
    </p>
    <a
      href="/shop"
      class="btn-press mt-8 inline-flex items-center gap-2 rounded-xl bg-gold-500 px-10 py-4 text-sm font-bold text-burgundy-950 transition-all hover:bg-gold-400 hover:shadow-lg hover:shadow-gold-500/25"
    >
      Shop Now
      <ArrowRight class="h-4 w-4" />
    </a>
  </div>
</section>
