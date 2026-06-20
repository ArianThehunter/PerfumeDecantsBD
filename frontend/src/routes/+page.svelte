<!--
  PerfumeDecantBD — Landing Page
  ═══════════════════════════════════════════════════════════════════════════
  Luxury landing page with:
  - Cinematic hero banner
  - Featured collections
  - Best sellers grid
  - Brand story
  - Featured ingredients
  - Testimonials
  - Newsletter
  - Instagram gallery
-->
<script lang="ts">
  import { onMount } from 'svelte';

  let visible = $state(false);

  onMount(() => {
    visible = true;
  });

  // Mock data for frontend-only display
  const featuredCollections = [
    { id: 1, name: 'For Him', slug: 'for-him', image: 'https://images.unsplash.com/photo-1594035910387-fea081d63b64?w=600&h=800&fit=crop', count: 45 },
    { id: 2, name: 'For Her', slug: 'for-her', image: 'https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?w=600&h=800&fit=crop', count: 52 },
    { id: 3, name: 'Niche & Exclusive', slug: 'niche', image: 'https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=600&h=800&fit=crop', count: 28 },
    { id: 4, name: 'Gift Sets', slug: 'gifts', image: 'https://images.unsplash.com/photo-1592914610354-fd354ea45e48?w=600&h=800&fit=crop', count: 18 },
  ];

  const bestSellers = [
    { id: 1, name: 'Bleu de Chanel', brand: 'Chanel', price: 4500, originalPrice: 5200, rating: 4.8, reviews: 124, image: 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=400&h=500&fit=crop', badge: 'Best Seller' },
    { id: 2, name: 'Sauvage Eau de Parfum', brand: 'Dior', price: 4200, originalPrice: null, rating: 4.7, reviews: 98, image: 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=500&fit=crop', badge: null },
    { id: 3, name: 'Oud Wood', brand: 'Tom Ford', price: 8500, originalPrice: 9800, rating: 4.9, reviews: 67, image: 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=400&h=500&fit=crop', badge: 'Premium' },
    { id: 4, name: 'Aventus', brand: 'Creed', price: 12000, originalPrice: null, rating: 4.9, reviews: 203, image: 'https://images.unsplash.com/photo-1595425964272-fc617fa19dfa?w=400&h=500&fit=crop', badge: 'Iconic' },
    { id: 5, name: "La Vie Est Belle", brand: 'Lancôme', price: 3800, originalPrice: 4500, rating: 4.6, reviews: 156, image: 'https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?w=400&h=500&fit=crop', badge: 'Popular' },
    { id: 6, name: 'Black Orchid', brand: 'Tom Ford', price: 7200, originalPrice: null, rating: 4.7, reviews: 89, image: 'https://images.unsplash.com/photo-1594035910387-fea081d63b64?w=400&h=500&fit=crop', badge: null },
    { id: 7, name: 'N°5', brand: 'Chanel', price: 5500, originalPrice: null, rating: 4.8, reviews: 312, image: 'https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=400&h=500&fit=crop', badge: 'Legendary' },
    { id: 8, name: 'Light Blue', brand: 'Dolce & Gabbana', price: 2800, originalPrice: 3200, rating: 4.5, reviews: 178, image: 'https://images.unsplash.com/photo-1592914610354-fd354ea45e48?w=400&h=500&fit=crop', badge: null },
  ];

  const ingredients = [
    { name: 'Oud', icon: '🪵', description: 'The liquid gold of perfumery, prized for its deep, complex, woody aroma.' },
    { name: 'Rose de Mai', icon: '🌹', description: 'Hand-picked at dawn in Grasse, the heart of countless iconic fragrances.' },
    { name: 'Bergamot', icon: '🍊', description: 'Bright Italian citrus that opens fragrances with sparkling freshness.' },
    { name: 'Vanilla', icon: '🌿', description: 'Rich Madagascar bourbon vanilla, the most sensual of base notes.' },
    { name: 'Jasmine', icon: '🌸', description: 'Night-blooming jasmine from India, intoxicating and deeply floral.' },
    { name: 'Sandalwood', icon: '🪵', description: 'Mysore sandalwood, creamy, warm, and timelessly elegant.' },
  ];

  const testimonials = [
    { name: 'Sarah K.', location: 'Dhaka', text: 'Absolutely authentic fragrances. The packaging was luxurious and the decant quality is exceptional. My go-to perfume store in BD!', rating: 5, avatar: '👩' },
    { name: 'Rahim M.', location: 'Chittagong', text: 'Finally a reliable source for niche fragrances in Bangladesh. Creed Aventus was 100% genuine. Will order again.', rating: 5, avatar: '👨' },
    { name: 'Nadia A.', location: 'Sylhet', text: 'The curation is incredible — every fragrance I have ordered has been a masterpiece. The 3-day delivery was a pleasant surprise!', rating: 5, avatar: '👩' },
  ];

  const formatPrice = (price: number) => `৳${price.toLocaleString()}`;
</script>

<svelte:head>
  <title>PerfumeDecantBD — Luxury Fragrances | Authentic Perfumes in Bangladesh</title>
  <meta name="description" content="Discover authentic luxury perfumes from Chanel, Dior, Tom Ford, Creed & more. Premium decants and full bottles delivered across Bangladesh." />
</svelte:head>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- HERO SECTION                                                          -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="relative min-h-screen flex items-center bg-gradient-hero overflow-hidden">
  <!-- Animated Background Elements -->
  <div class="absolute inset-0 overflow-hidden">
    <div class="absolute top-20 left-10 w-96 h-96 rounded-full bg-primary-500/5 blur-3xl animate-float"></div>
    <div class="absolute bottom-20 right-10 w-80 h-80 rounded-full bg-secondary-500/5 blur-3xl animate-float delay-300"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-primary-500/3 blur-3xl"></div>
    <!-- Decorative golden particles -->
    <div class="absolute top-32 right-1/4 w-2 h-2 rounded-full bg-primary-400/40 animate-float delay-200"></div>
    <div class="absolute top-48 left-1/3 w-1.5 h-1.5 rounded-full bg-primary-400/30 animate-float delay-500"></div>
    <div class="absolute bottom-32 left-1/4 w-2.5 h-2.5 rounded-full bg-primary-400/20 animate-float delay-700"></div>
  </div>

  <div class="container-luxury relative z-10 py-40 lg:py-0">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
      <!-- Hero Text -->
      <div class="text-center lg:text-left" class:animate-fade-in-up={visible}>
        <div class="inline-flex items-center gap-2 px-4 py-2 bg-white/5 backdrop-blur-sm border border-white/10 text-primary-400 text-xs tracking-[0.3em] uppercase mb-8">
          <span class="w-1.5 h-1.5 rounded-full bg-primary-400 animate-pulse"></span>
          Curated Luxury Fragrances
        </div>

        <h1 class="text-4xl md:text-5xl lg:text-7xl font-bold text-white mb-6 leading-[1.1]">
          The Art of
          <span class="block animate-shimmer-gold">
            Fine Perfumery
          </span>
        </h1>

        <p class="text-warm-400 text-lg md:text-xl max-w-xl mx-auto lg:mx-0 mb-10 font-light leading-relaxed font-[var(--font-accent)]">
          Discover authentic luxury fragrances from the world's most prestigious perfume houses.
          Every bottle tells a story of craftsmanship and elegance.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
          <a href="/products" class="btn-primary">
            Explore Collection
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
            </svg>
          </a>
          <a href="/products?collection=best-sellers" class="btn-secondary border-white/30 text-white hover:bg-white/10 hover:border-white/50">
            Best Sellers
          </a>
        </div>

        <!-- Trust Badges -->
        <div class="flex items-center gap-8 mt-12 justify-center lg:justify-start text-warm-500 text-xs tracking-wider uppercase">
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
            </svg>
            100% Authentic
          </div>
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 0 1-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 0 0-3.213-9.193 2.056 2.056 0 0 0-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 0 0-10.026 0 1.106 1.106 0 0 0-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
            </svg>
            Fast Delivery
          </div>
          <div class="flex items-center gap-2 hidden sm:flex">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 11.25v8.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1 0 9.375 7.5H12m0-2.625V7.5m0-2.625A2.625 2.625 0 1 1 14.625 7.5H12m0 0V21m-8.625-9.75h18c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125h-18c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
            </svg>
            Premium Packaging
          </div>
        </div>
      </div>

      <!-- Hero Visual -->
      <div class="hidden lg:flex justify-center items-center relative">
        <div class="relative w-[400px] h-[500px]">
          <!-- Glowing circle behind bottle -->
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-80 h-80 rounded-full bg-primary-500/10 animate-pulse-glow"></div>
          </div>
          <!-- Perfume bottle placeholder with elegant styling -->
          <div class="absolute inset-0 flex items-center justify-center" class:animate-fade-in={visible}>
            <div class="relative">
              <div class="w-48 h-72 bg-gradient-to-b from-primary-300/20 to-primary-600/20 backdrop-blur-sm border border-primary-400/30 rounded-t-[30%] flex items-center justify-center">
                <span class="text-7xl opacity-60">🧴</span>
              </div>
              <div class="w-20 h-8 mx-auto -mt-1 bg-gradient-gold rounded-t-lg"></div>
            </div>
          </div>
          <!-- Floating note badges -->
          <div class="absolute top-12 -left-4 glass-card px-4 py-2 text-xs text-white/80 animate-float delay-200 bg-white/5">
            🌹 Rose de Mai
          </div>
          <div class="absolute bottom-24 -right-4 glass-card px-4 py-2 text-xs text-white/80 animate-float delay-500 bg-white/5">
            🪵 Oud Wood
          </div>
          <div class="absolute top-36 -right-8 glass-card px-4 py-2 text-xs text-white/80 animate-float delay-700 bg-white/5">
            🍊 Bergamot
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Scroll indicator -->
  <div class="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
    <div class="w-6 h-10 rounded-full border-2 border-white/30 flex items-start justify-center pt-2">
      <div class="w-1.5 h-3 rounded-full bg-primary-400 animate-pulse"></div>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- FEATURED COLLECTIONS                                                  -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="py-24 bg-surface-light">
  <div class="container-luxury">
    <div class="text-center mb-16">
      <h2 class="section-heading section-heading-center">Curated Collections</h2>
      <p class="text-warm-500 mt-6 max-w-2xl mx-auto font-light text-lg font-[var(--font-accent)]">
        Explore our carefully curated fragrance collections, each designed to match your mood, occasion, and personality.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {#each featuredCollections as collection, i}
        <a
          href="/products?collection={collection.slug}"
          class="group relative overflow-hidden aspect-[3/4] block"
          style="animation-delay: {i * 150}ms"
        >
          <img
            src={collection.image}
            alt={collection.name}
            class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            loading="lazy"
          />
          <div class="absolute inset-0 overlay-gradient"></div>
          <div class="absolute inset-0 bg-primary-500/0 group-hover:bg-primary-500/10 transition-colors duration-500"></div>
          <div class="absolute bottom-0 left-0 right-0 p-6">
            <h3 class="text-white text-xl font-semibold font-[var(--font-heading)] mb-1">{collection.name}</h3>
            <p class="text-white/60 text-sm">{collection.count} fragrances</p>
            <div class="mt-3 flex items-center gap-2 text-primary-300 text-xs tracking-[0.15em] uppercase opacity-0 group-hover:opacity-100 transition-opacity duration-500 translate-y-2 group-hover:translate-y-0">
              Shop Collection
              <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
              </svg>
            </div>
          </div>
        </a>
      {/each}
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- BEST SELLERS                                                          -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="py-24 bg-white">
  <div class="container-luxury">
    <div class="flex items-end justify-between mb-16">
      <div>
        <h2 class="section-heading">Best Sellers</h2>
        <p class="text-warm-500 mt-6 font-light text-lg font-[var(--font-accent)]">
          Our most loved fragrances, chosen by thousands of perfume enthusiasts.
        </p>
      </div>
      <a href="/products?collection=best-sellers" class="btn-secondary hidden md:inline-flex">
        View All
      </a>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {#each bestSellers as product, i}
        <a href="/products/{product.name.toLowerCase().replace(/\s+/g, '-')}" class="group">
          <div class="luxury-card overflow-hidden">
            <!-- Image -->
            <div class="relative aspect-[4/5] overflow-hidden bg-warm-100">
              <img
                src={product.image}
                alt={product.name}
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                loading="lazy"
              />
              {#if product.badge}
                <span class="absolute top-3 left-3 badge badge-gold text-[10px]">
                  {product.badge}
                </span>
              {/if}
              {#if product.originalPrice}
                <span class="absolute top-3 right-3 badge badge-danger text-[10px]">
                  -{Math.round((1 - product.price / product.originalPrice) * 100)}%
                </span>
              {/if}
              <!-- Quick actions on hover -->
              <div class="absolute bottom-0 left-0 right-0 p-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-4 group-hover:translate-y-0">
                <button class="flex-1 bg-white/90 backdrop-blur-sm text-warm-900 text-xs font-medium py-2.5 hover:bg-primary-500 hover:text-white transition-colors tracking-wider uppercase">
                  Add to Cart
                </button>
                <button class="w-10 h-10 bg-white/90 backdrop-blur-sm flex items-center justify-center hover:bg-primary-500 hover:text-white transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Info -->
            <div class="p-4">
              <p class="text-warm-400 text-xs tracking-[0.15em] uppercase mb-1">{product.brand}</p>
              <h3 class="text-warm-900 font-medium text-sm mb-2 font-[var(--font-heading)] group-hover:text-primary-600 transition-colors">
                {product.name}
              </h3>
              <!-- Rating -->
              <div class="flex items-center gap-1 mb-2">
                {#each Array(5) as _, j}
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 {j < Math.floor(product.rating) ? 'text-primary-500' : 'text-warm-300'}" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                {/each}
                <span class="text-warm-400 text-xs ml-1">({product.reviews})</span>
              </div>
              <!-- Price -->
              <div class="flex items-center gap-2">
                <span class="text-warm-900 font-semibold">{formatPrice(product.price)}</span>
                {#if product.originalPrice}
                  <span class="text-warm-400 text-sm line-through">{formatPrice(product.originalPrice)}</span>
                {/if}
              </div>
            </div>
          </div>
        </a>
      {/each}
    </div>

    <div class="text-center mt-12 md:hidden">
      <a href="/products?collection=best-sellers" class="btn-secondary">View All Best Sellers</a>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- SEASONAL PROMOTION BANNER                                             -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="relative py-32 bg-gradient-hero overflow-hidden">
  <div class="absolute inset-0">
    <div class="absolute top-10 right-10 w-64 h-64 rounded-full bg-primary-500/5 blur-3xl animate-float"></div>
    <div class="absolute bottom-10 left-10 w-48 h-48 rounded-full bg-secondary-500/5 blur-3xl animate-float delay-300"></div>
  </div>
  <div class="container-luxury relative z-10 text-center">
    <p class="text-primary-400 text-sm tracking-[0.3em] uppercase mb-4">Limited Time Offer</p>
    <h2 class="text-4xl md:text-6xl font-bold text-white mb-6 font-[var(--font-heading)]">
      Summer Collection
      <span class="text-gradient-gold">2026</span>
    </h2>
    <p class="text-warm-400 text-lg max-w-2xl mx-auto mb-10 font-light font-[var(--font-accent)]">
      Fresh aquatic and citrus fragrances perfect for the warm season.
      Up to 25% off on selected summer fragrances.
    </p>
    <a href="/products?collection=summer-2026" class="btn-primary">
      Shop Summer Collection
    </a>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- BRAND STORY                                                           -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="py-24 bg-white">
  <div class="container-luxury">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
      <div>
        <p class="text-primary-500 text-sm tracking-[0.3em] uppercase mb-4">Our Story</p>
        <h2 class="section-heading mb-8">
          Crafting Moments Through Scent
        </h2>
        <div class="space-y-6 text-warm-600 font-light leading-relaxed">
          <p class="text-lg font-[var(--font-accent)]">
            Born from a passion for fine perfumery, PerfumeDecantBD brings the world's most
            prestigious fragrance houses to Bangladesh. We believe that luxury should be accessible
            without compromising authenticity.
          </p>
          <p>
            Every fragrance in our collection is sourced directly from authorized distributors,
            ensuring 100% authenticity. From iconic designer perfumes to rare niche creations,
            we curate only the finest — because your scent is your signature.
          </p>
          <p>
            Our decant service allows you to experience luxury fragrances in premium travel-sized
            portions, making world-class perfumery accessible to everyone.
          </p>
        </div>
        <a href="/about" class="btn-secondary mt-8 inline-flex">
          Read Our Story
        </a>
      </div>
      <div class="relative">
        <div class="aspect-[4/5] overflow-hidden">
          <img
            src="https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=800&h=1000&fit=crop"
            alt="Perfume artisan crafting fragrances"
            class="w-full h-full object-cover"
            loading="lazy"
          />
        </div>
        <!-- Floating stat card -->
        <div class="absolute -bottom-6 -left-6 glass-card p-6 bg-white/90">
          <p class="text-3xl font-bold text-primary-600 font-[var(--font-heading)]">500+</p>
          <p class="text-warm-600 text-sm mt-1">Premium Fragrances</p>
        </div>
        <div class="absolute -top-6 -right-6 glass-card p-6 bg-white/90">
          <p class="text-3xl font-bold text-primary-600 font-[var(--font-heading)]">5000+</p>
          <p class="text-warm-600 text-sm mt-1">Happy Customers</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- FEATURED INGREDIENTS                                                  -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="py-24 bg-surface-light">
  <div class="container-luxury">
    <div class="text-center mb-16">
      <h2 class="section-heading section-heading-center">The Finest Ingredients</h2>
      <p class="text-warm-500 mt-6 max-w-2xl mx-auto font-light text-lg font-[var(--font-accent)]">
        The world's most precious raw materials, transformed into olfactory masterpieces.
      </p>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
      {#each ingredients as ingredient, i}
        <div
          class="luxury-card p-6 text-center group cursor-default"
          style="animation-delay: {i * 100}ms"
        >
          <div class="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">
            {ingredient.icon}
          </div>
          <h3 class="text-warm-900 font-semibold font-[var(--font-heading)] mb-2">{ingredient.name}</h3>
          <p class="text-warm-500 text-xs leading-relaxed font-light">{ingredient.description}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- TESTIMONIALS                                                          -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="py-24 bg-white">
  <div class="container-luxury">
    <div class="text-center mb-16">
      <h2 class="section-heading section-heading-center">What Our Customers Say</h2>
      <p class="text-warm-500 mt-6 max-w-2xl mx-auto font-light text-lg font-[var(--font-accent)]">
        Join thousands of fragrance lovers who trust PerfumeDecantBD.
      </p>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      {#each testimonials as testimonial, i}
        <div class="luxury-card p-8" style="animation-delay: {i * 150}ms">
          <!-- Stars -->
          <div class="flex items-center gap-1 mb-6">
            {#each Array(testimonial.rating) as _}
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            {/each}
          </div>
          <!-- Quote -->
          <p class="text-warm-700 leading-relaxed mb-6 italic font-[var(--font-accent)] text-lg">
            "{testimonial.text}"
          </p>
          <!-- Author -->
          <div class="flex items-center gap-3">
            <span class="text-2xl">{testimonial.avatar}</span>
            <div>
              <p class="text-warm-900 font-medium text-sm">{testimonial.name}</p>
              <p class="text-warm-400 text-xs">{testimonial.location}</p>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- NEWSLETTER CTA                                                        -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="py-24 bg-gradient-hero relative overflow-hidden">
  <div class="absolute inset-0">
    <div class="absolute top-0 right-0 w-96 h-96 bg-primary-500/5 rounded-full blur-3xl"></div>
    <div class="absolute bottom-0 left-0 w-64 h-64 bg-secondary-500/5 rounded-full blur-3xl"></div>
  </div>
  <div class="container-luxury relative z-10 text-center">
    <h2 class="text-3xl md:text-5xl font-bold text-white mb-6 font-[var(--font-heading)]">
      Stay in the World of
      <span class="text-gradient-gold">Luxury</span>
    </h2>
    <p class="text-warm-400 text-lg max-w-xl mx-auto mb-10 font-light font-[var(--font-accent)]">
      Be the first to discover new arrivals, exclusive offers, and curated fragrance guides.
    </p>
    <form class="max-w-md mx-auto flex gap-3" onsubmit={(e) => e.preventDefault()}>
      <input
        type="email"
        placeholder="your@email.com"
        class="flex-1 bg-white/10 border border-white/20 px-6 py-4 text-white placeholder:text-warm-500 focus:border-primary-400 focus:outline-none backdrop-blur-sm transition-colors"
      />
      <button type="submit" class="btn-primary px-8">
        Subscribe
      </button>
    </form>
    <p class="text-warm-600 text-xs mt-4">No spam. Unsubscribe anytime.</p>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- TRENDING BRANDS BAR                                                   -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<section class="py-16 bg-warm-50 border-y border-warm-200">
  <div class="container-luxury">
    <p class="text-center text-warm-400 text-xs tracking-[0.3em] uppercase mb-10">Featuring World-Renowned Houses</p>
    <div class="flex flex-wrap items-center justify-center gap-12 md:gap-16 text-warm-400">
      {#each ['Chanel', 'Dior', 'Tom Ford', 'Creed', 'Guerlain', 'Hermès', 'YSL', 'Versace'] as brand}
        <span class="text-lg md:text-xl font-[var(--font-heading)] font-semibold tracking-wider hover:text-primary-600 transition-colors cursor-default">
          {brand}
        </span>
      {/each}
    </div>
  </div>
</section>
