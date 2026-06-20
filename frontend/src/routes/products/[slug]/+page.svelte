<!--
  PerfumeDecantBD — Product Detail Page
  Gallery, fragrance pyramid, variant selector, reviews, related products.
-->
<script lang="ts">
  import { page } from '$app/stores';

  let selectedSize = $state('100ml');
  let quantity = $state(1);
  let activeTab = $state('description');
  let selectedImage = $state(0);
  let wishlistAdded = $state(false);

  const product = {
    id: 1,
    name: 'Bleu de Chanel',
    brand: 'Chanel',
    slug: 'bleu-de-chanel',
    description: 'An aromatic-woody fragrance that embodies freedom. Bleu de Chanel is a timeless and powerfully fresh composition. Cedar and sandalwood bring depth, while grapefruit and mint create an invigorating opening. This is a fragrance for the man who refuses to be defined.',
    shortDescription: 'A woody aromatic fragrance that embodies freedom and determination.',
    concentration: 'Eau de Parfum',
    gender: 'Men',
    perfumer: 'Jacques Polge',
    releaseYear: 2014,
    rating: 4.8,
    reviews: 124,
    totalSold: 523,
    longevity: 8.5,
    projection: 7.2,
    value: 8.0,
    images: [
      'https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=800&h=1000&fit=crop',
      'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800&h=1000&fit=crop',
      'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=800&h=1000&fit=crop',
      'https://images.unsplash.com/photo-1595425964272-fc617fa19dfa?w=800&h=1000&fit=crop',
    ],
    variants: [
      { size: '50ml', price: 3200, originalPrice: 3800, inStock: true, sku: 'BDC-50' },
      { size: '100ml', price: 4500, originalPrice: 5200, inStock: true, sku: 'BDC-100' },
      { size: '150ml', price: 5800, originalPrice: null, inStock: false, sku: 'BDC-150' },
    ],
    notes: {
      top: [
        { name: 'Grapefruit', icon: '🍊' },
        { name: 'Lemon', icon: '🍋' },
        { name: 'Mint', icon: '🌿' },
        { name: 'Pink Pepper', icon: '🌶️' },
      ],
      middle: [
        { name: 'Ginger', icon: '🫚' },
        { name: 'Jasmine', icon: '🌸' },
        { name: 'Nutmeg', icon: '🥜' },
        { name: 'Iso E Super', icon: '🧪' },
      ],
      base: [
        { name: 'Cedar', icon: '🪵' },
        { name: 'Sandalwood', icon: '🪵' },
        { name: 'Vetiver', icon: '🌿' },
        { name: 'Incense', icon: '🕯️' },
      ],
    },
    usage: { occasion: 'Day & Night, Office, Date Night', season: 'Fall, Winter, Spring' },
  };

  const selectedVariant = $derived(product.variants.find(v => v.size === selectedSize) || product.variants[0]);
  const formatPrice = (price: number) => `৳${price.toLocaleString()}`;

  const relatedProducts = [
    { id: 2, name: 'Sauvage', brand: 'Dior', price: 4200, image: 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=500&fit=crop', rating: 4.7 },
    { id: 3, name: 'Oud Wood', brand: 'Tom Ford', price: 8500, image: 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=400&h=500&fit=crop', rating: 4.9 },
    { id: 4, name: 'Aventus', brand: 'Creed', price: 12000, image: 'https://images.unsplash.com/photo-1595425964272-fc617fa19dfa?w=400&h=500&fit=crop', rating: 4.9 },
    { id: 5, name: "Terre d'Hermès", brand: 'Hermès', price: 6500, image: 'https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=400&h=500&fit=crop', rating: 4.7 },
  ];

  const reviewsList = [
    { name: 'Ahmed R.', rating: 5, date: '2 weeks ago', title: 'Absolutely stunning fragrance', content: 'This has become my signature scent. The longevity is incredible — I get compliments even after 10+ hours. The dry down is particularly impressive.', verified: true },
    { name: 'Fatima S.', rating: 4, date: '1 month ago', title: 'Great but pricey', content: 'Beautiful fragrance that performs well. A bit expensive for Bangladesh market but you get what you pay for. Authentic product.', verified: true },
    { name: 'Karim H.', rating: 5, date: '2 months ago', title: 'Best office fragrance', content: 'Perfect for professional settings. Not too loud, very sophisticated. My colleagues always ask what I am wearing.', verified: false },
  ];

  const tabs = [
    { id: 'description', label: 'Description' },
    { id: 'notes', label: 'Fragrance Notes' },
    { id: 'reviews', label: `Reviews (${product.reviews})` },
  ];
</script>

<svelte:head>
  <title>{product.name} by {product.brand} — PerfumeDecantBD</title>
  <meta name="description" content="{product.shortDescription} Shop authentic {product.name} at the best price in Bangladesh." />
</svelte:head>

<div class="pt-28 pb-16">
  <div class="container-luxury">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm text-warm-400 mb-8">
      <a href="/" class="hover:text-primary-600 transition-colors">Home</a>
      <span>/</span>
      <a href="/products" class="hover:text-primary-600 transition-colors">Shop</a>
      <span>/</span>
      <a href="/products?brand={product.brand}" class="hover:text-primary-600 transition-colors">{product.brand}</a>
      <span>/</span>
      <span class="text-warm-700">{product.name}</span>
    </nav>

    <!-- Product Main -->
    <div class="grid lg:grid-cols-2 gap-12 lg:gap-16">
      <!-- Gallery -->
      <div class="space-y-4">
        <!-- Main Image -->
        <div class="aspect-[4/5] overflow-hidden bg-warm-100 relative group">
          <img
            src={product.images[selectedImage]}
            alt="{product.name} - Image {selectedImage + 1}"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110 cursor-zoom-in"
          />
          {#if selectedVariant.originalPrice}
            <span class="absolute top-4 left-4 badge badge-danger">
              -{Math.round((1 - selectedVariant.price / selectedVariant.originalPrice) * 100)}% OFF
            </span>
          {/if}
        </div>
        <!-- Thumbnails -->
        <div class="grid grid-cols-4 gap-3">
          {#each product.images as img, i}
            <button
              onclick={() => selectedImage = i}
              class="aspect-square overflow-hidden border-2 transition-all duration-300
                {selectedImage === i ? 'border-primary-500 opacity-100' : 'border-transparent opacity-60 hover:opacity-100'}"
            >
              <img src={img} alt="Thumbnail {i + 1}" class="w-full h-full object-cover" />
            </button>
          {/each}
        </div>
      </div>

      <!-- Product Info -->
      <div class="lg:sticky lg:top-32 lg:self-start">
        <p class="text-primary-500 text-sm tracking-[0.2em] uppercase mb-2">{product.brand}</p>
        <h1 class="text-3xl md:text-4xl font-bold font-[var(--font-heading)] text-warm-950 mb-3">
          {product.name}
        </h1>
        <p class="text-warm-500 mb-4">{product.concentration} · {product.gender}</p>

        <!-- Rating -->
        <div class="flex items-center gap-3 mb-6">
          <div class="flex items-center gap-1">
            {#each Array(5) as _, j}
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 {j < Math.floor(product.rating) ? 'text-primary-500' : 'text-warm-300'}" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            {/each}
          </div>
          <span class="text-warm-600 text-sm">{product.rating}</span>
          <span class="text-warm-400">·</span>
          <a href="#reviews" class="text-primary-600 text-sm hover:underline">{product.reviews} reviews</a>
          <span class="text-warm-400">·</span>
          <span class="text-warm-500 text-sm">{product.totalSold} sold</span>
        </div>

        <!-- Performance Ratings -->
        <div class="flex items-center gap-6 mb-8 p-4 bg-warm-50 border border-warm-200">
          {#each [{ label: 'Longevity', value: product.longevity }, { label: 'Projection', value: product.projection }, { label: 'Value', value: product.value }] as perf}
            <div class="text-center flex-1">
              <p class="text-xs text-warm-500 uppercase tracking-wider mb-1">{perf.label}</p>
              <p class="text-lg font-semibold text-warm-900">{perf.value}<span class="text-warm-400 text-sm">/10</span></p>
            </div>
          {/each}
        </div>

        <!-- Price -->
        <div class="flex items-end gap-3 mb-6">
          <span class="text-3xl font-bold text-warm-950">{formatPrice(selectedVariant.price)}</span>
          {#if selectedVariant.originalPrice}
            <span class="text-xl text-warm-400 line-through">{formatPrice(selectedVariant.originalPrice)}</span>
            <span class="badge badge-danger text-xs">
              Save {formatPrice(selectedVariant.originalPrice - selectedVariant.price)}
            </span>
          {/if}
        </div>

        <!-- Size Selector -->
        <div class="mb-6">
          <p class="text-sm font-semibold uppercase tracking-wider text-warm-900 mb-3">Size</p>
          <div class="flex gap-3">
            {#each product.variants as variant}
              <button
                onclick={() => selectedSize = variant.size}
                disabled={!variant.inStock}
                class="px-6 py-3 border text-sm transition-all duration-300
                  {selectedSize === variant.size
                    ? 'border-primary-500 bg-primary-50 text-primary-700 font-medium'
                    : variant.inStock
                      ? 'border-warm-300 text-warm-600 hover:border-warm-400'
                      : 'border-warm-200 text-warm-300 line-through cursor-not-allowed'
                  }"
              >
                {variant.size}
                {#if !variant.inStock}
                  <span class="text-xs block text-warm-400">Sold out</span>
                {/if}
              </button>
            {/each}
          </div>
        </div>

        <!-- Quantity & Add to Cart -->
        <div class="flex items-center gap-4 mb-6">
          <div class="flex items-center border border-warm-300">
            <button onclick={() => quantity = Math.max(1, quantity - 1)} class="w-10 h-12 flex items-center justify-center text-warm-600 hover:bg-warm-50 transition-colors">−</button>
            <span class="w-12 h-12 flex items-center justify-center text-sm font-medium border-x border-warm-300">{quantity}</span>
            <button onclick={() => quantity = Math.min(10, quantity + 1)} class="w-10 h-12 flex items-center justify-center text-warm-600 hover:bg-warm-50 transition-colors">+</button>
          </div>
          <button class="btn-primary flex-1 py-4" disabled={!selectedVariant.inStock}>
            {selectedVariant.inStock ? 'Add to Cart' : 'Out of Stock'}
          </button>
          <button
            onclick={() => wishlistAdded = !wishlistAdded}
            class="w-12 h-12 border border-warm-300 flex items-center justify-center hover:border-primary-500 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 {wishlistAdded ? 'text-red-500 fill-red-500' : 'text-warm-500'}" fill="{wishlistAdded ? 'currentColor' : 'none'}" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
            </svg>
          </button>
        </div>

        <!-- Stock Status -->
        {#if selectedVariant.inStock}
          <p class="flex items-center gap-2 text-sm text-green-600 mb-6">
            <span class="w-2 h-2 rounded-full bg-green-500"></span>
            In Stock — Usually ships within 1-2 business days
          </p>
        {:else}
          <p class="flex items-center gap-2 text-sm text-red-500 mb-6">
            <span class="w-2 h-2 rounded-full bg-red-500"></span>
            Currently Out of Stock
          </p>
        {/if}

        <!-- Usage Info -->
        <div class="border-t border-warm-200 pt-6 space-y-3">
          <p class="text-sm"><span class="text-warm-500">Best for:</span> <span class="text-warm-800">{product.usage.occasion}</span></p>
          <p class="text-sm"><span class="text-warm-500">Season:</span> <span class="text-warm-800">{product.usage.season}</span></p>
          <p class="text-sm"><span class="text-warm-500">Perfumer:</span> <span class="text-warm-800">{product.perfumer}</span></p>
          <p class="text-sm"><span class="text-warm-500">Year:</span> <span class="text-warm-800">{product.releaseYear}</span></p>
        </div>
      </div>
    </div>

    <!-- Tabs Section -->
    <div class="mt-20">
      <!-- Tab Navigation -->
      <div class="flex border-b border-warm-200">
        {#each tabs as tab}
          <button
            onclick={() => activeTab = tab.id}
            class="px-6 py-4 text-sm font-medium tracking-wider uppercase transition-all relative
              {activeTab === tab.id ? 'text-primary-600' : 'text-warm-500 hover:text-warm-700'}"
          >
            {tab.label}
            {#if activeTab === tab.id}
              <span class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-500"></span>
            {/if}
          </button>
        {/each}
      </div>

      <!-- Tab Content -->
      <div class="py-10">
        {#if activeTab === 'description'}
          <div class="max-w-3xl">
            <p class="text-warm-700 leading-relaxed text-lg font-[var(--font-accent)] mb-6">
              {product.description}
            </p>
          </div>

        {:else if activeTab === 'notes'}
          <!-- Fragrance Pyramid -->
          <div class="max-w-3xl mx-auto">
            <h3 class="text-2xl font-semibold font-[var(--font-heading)] text-center mb-10">Fragrance Pyramid</h3>
            <div class="space-y-8">
              {#each [{ label: 'Top Notes', sublabel: 'First impression (0-30 min)', notes: product.notes.top, color: 'primary' }, { label: 'Heart Notes', sublabel: 'Character (30 min - 4h)', notes: product.notes.middle, color: 'secondary' }, { label: 'Base Notes', sublabel: 'Foundation (4h+)', notes: product.notes.base, color: 'accent' }] as layer}
                <div class="p-6 bg-warm-50 border border-warm-200">
                  <div class="flex items-center gap-3 mb-4">
                    <div class="w-3 h-3 rounded-full bg-{layer.color}-500"></div>
                    <div>
                      <h4 class="font-semibold text-warm-900">{layer.label}</h4>
                      <p class="text-xs text-warm-400">{layer.sublabel}</p>
                    </div>
                  </div>
                  <div class="flex flex-wrap gap-3">
                    {#each layer.notes as note}
                      <span class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-warm-200 text-sm text-warm-700 hover:border-primary-300 transition-colors">
                        <span>{note.icon}</span>
                        {note.name}
                      </span>
                    {/each}
                  </div>
                </div>
              {/each}
            </div>
          </div>

        {:else if activeTab === 'reviews'}
          <div id="reviews" class="max-w-3xl">
            <!-- Review Summary -->
            <div class="flex items-center gap-8 mb-10 p-6 bg-warm-50 border border-warm-200">
              <div class="text-center">
                <p class="text-5xl font-bold text-primary-600 font-[var(--font-heading)]">{product.rating}</p>
                <div class="flex items-center gap-1 mt-2 justify-center">
                  {#each Array(5) as _, j}
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 {j < Math.floor(product.rating) ? 'text-primary-500' : 'text-warm-300'}" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  {/each}
                </div>
                <p class="text-warm-500 text-sm mt-1">{product.reviews} reviews</p>
              </div>
              <div class="flex-1 space-y-2">
                {#each [5, 4, 3, 2, 1] as star}
                  <div class="flex items-center gap-3">
                    <span class="text-xs text-warm-500 w-6">{star}★</span>
                    <div class="flex-1 h-2 bg-warm-200 rounded-full overflow-hidden">
                      <div class="h-full bg-primary-500 rounded-full" style="width: {star === 5 ? 70 : star === 4 ? 20 : star === 3 ? 7 : 3}%"></div>
                    </div>
                  </div>
                {/each}
              </div>
            </div>

            <!-- Individual Reviews -->
            <div class="space-y-8">
              {#each reviewsList as review}
                <div class="border-b border-warm-100 pb-8">
                  <div class="flex items-center gap-3 mb-3">
                    <div class="flex items-center gap-1">
                      {#each Array(5) as _, j}
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5 {j < review.rating ? 'text-primary-500' : 'text-warm-300'}" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      {/each}
                    </div>
                    <span class="font-medium text-sm text-warm-900">{review.name}</span>
                    {#if review.verified}
                      <span class="badge badge-success text-[10px]">Verified Purchase</span>
                    {/if}
                    <span class="text-warm-400 text-xs ml-auto">{review.date}</span>
                  </div>
                  <h4 class="font-medium text-warm-900 mb-2">{review.title}</h4>
                  <p class="text-warm-600 text-sm leading-relaxed">{review.content}</p>
                </div>
              {/each}
            </div>
          </div>
        {/if}
      </div>
    </div>

    <!-- Related Products -->
    <div class="mt-16 border-t border-warm-200 pt-16">
      <h2 class="section-heading mb-10">You May Also Like</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        {#each relatedProducts as related}
          <a href="/products/{related.name.toLowerCase().replace(/\s+/g, '-')}" class="group">
            <div class="luxury-card overflow-hidden">
              <div class="aspect-[4/5] overflow-hidden bg-warm-100">
                <img src={related.image} alt={related.name} class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy" />
              </div>
              <div class="p-4">
                <p class="text-warm-400 text-xs tracking-[0.15em] uppercase mb-1">{related.brand}</p>
                <h3 class="text-warm-900 font-medium text-sm font-[var(--font-heading)] group-hover:text-primary-600 transition-colors">{related.name}</h3>
                <p class="text-warm-900 font-semibold mt-2">{formatPrice(related.price)}</p>
              </div>
            </div>
          </a>
        {/each}
      </div>
    </div>
  </div>
</div>
