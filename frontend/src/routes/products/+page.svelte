<!--
  PerfumeDecantBD — Product Catalog
  Advanced filtering, search, sort, grid/list toggle, pagination.
-->
<script lang="ts">
  let viewMode = $state<'grid' | 'list'>('grid');
  let filtersOpen = $state(true);
  let mobileFiltersOpen = $state(false);
  let sortBy = $state('newest');
  let searchQuery = $state('');

  // Filter state
  let selectedBrands = $state<string[]>([]);
  let selectedGender = $state('');
  let selectedConcentration = $state('');
  let priceRange = $state({ min: 0, max: 50000 });
  let selectedRating = $state(0);

  const brands = ['Chanel', 'Dior', 'Tom Ford', 'Creed', 'Guerlain', 'Hermès', 'YSL', 'Versace', 'Lancôme', 'D&G'];
  const genders = ['Men', 'Women', 'Unisex'];
  const concentrations = ['Eau de Parfum', 'Eau de Toilette', 'Parfum', 'Eau de Cologne'];
  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'price_asc', label: 'Price: Low to High' },
    { value: 'price_desc', label: 'Price: High to Low' },
    { value: 'rating', label: 'Highest Rated' },
    { value: 'popular', label: 'Most Popular' },
  ];

  // Mock products
  const products = [
    { id: 1, name: 'Bleu de Chanel', brand: 'Chanel', price: 4500, originalPrice: 5200, rating: 4.8, reviews: 124, image: 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=400&h=500&fit=crop', concentration: 'Eau de Parfum', gender: 'Men', inStock: true, badge: 'Best Seller' },
    { id: 2, name: 'Sauvage', brand: 'Dior', price: 4200, originalPrice: null, rating: 4.7, reviews: 98, image: 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=500&fit=crop', concentration: 'Eau de Parfum', gender: 'Men', inStock: true, badge: null },
    { id: 3, name: 'Oud Wood', brand: 'Tom Ford', price: 8500, originalPrice: 9800, rating: 4.9, reviews: 67, image: 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=400&h=500&fit=crop', concentration: 'Eau de Parfum', gender: 'Unisex', inStock: true, badge: 'Premium' },
    { id: 4, name: 'Aventus', brand: 'Creed', price: 12000, originalPrice: null, rating: 4.9, reviews: 203, image: 'https://images.unsplash.com/photo-1595425964272-fc617fa19dfa?w=400&h=500&fit=crop', concentration: 'Parfum', gender: 'Men', inStock: true, badge: 'Iconic' },
    { id: 5, name: "La Vie Est Belle", brand: 'Lancôme', price: 3800, originalPrice: 4500, rating: 4.6, reviews: 156, image: 'https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?w=400&h=500&fit=crop', concentration: 'Eau de Parfum', gender: 'Women', inStock: true, badge: null },
    { id: 6, name: 'Black Orchid', brand: 'Tom Ford', price: 7200, originalPrice: null, rating: 4.7, reviews: 89, image: 'https://images.unsplash.com/photo-1594035910387-fea081d63b64?w=400&h=500&fit=crop', concentration: 'Eau de Parfum', gender: 'Unisex', inStock: false, badge: null },
    { id: 7, name: 'N°5', brand: 'Chanel', price: 5500, originalPrice: null, rating: 4.8, reviews: 312, image: 'https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=400&h=500&fit=crop', concentration: 'Parfum', gender: 'Women', inStock: true, badge: 'Legendary' },
    { id: 8, name: 'Light Blue', brand: 'D&G', price: 2800, originalPrice: 3200, rating: 4.5, reviews: 178, image: 'https://images.unsplash.com/photo-1592914610354-fd354ea45e48?w=400&h=500&fit=crop', concentration: 'Eau de Toilette', gender: 'Women', inStock: true, badge: null },
    { id: 9, name: 'Terre d\'Hermès', brand: 'Hermès', price: 6500, originalPrice: null, rating: 4.7, reviews: 95, image: 'https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=400&h=500&fit=crop', concentration: 'Eau de Parfum', gender: 'Men', inStock: true, badge: null },
    { id: 10, name: 'Shalimar', brand: 'Guerlain', price: 5800, originalPrice: 6500, rating: 4.6, reviews: 142, image: 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=400&h=500&fit=crop', concentration: 'Eau de Parfum', gender: 'Women', inStock: true, badge: 'Classic' },
    { id: 11, name: 'Y Eau de Parfum', brand: 'YSL', price: 3900, originalPrice: null, rating: 4.5, reviews: 87, image: 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=500&fit=crop', concentration: 'Eau de Parfum', gender: 'Men', inStock: true, badge: null },
    { id: 12, name: 'Eros', brand: 'Versace', price: 3200, originalPrice: 3800, rating: 4.4, reviews: 210, image: 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=400&h=500&fit=crop', concentration: 'Eau de Toilette', gender: 'Men', inStock: true, badge: null },
  ];

  const formatPrice = (price: number) => `৳${price.toLocaleString()}`;

  function toggleBrand(brand: string) {
    if (selectedBrands.includes(brand)) {
      selectedBrands = selectedBrands.filter(b => b !== brand);
    } else {
      selectedBrands = [...selectedBrands, brand];
    }
  }
</script>

<svelte:head>
  <title>Shop Luxury Perfumes — PerfumeDecantBD</title>
  <meta name="description" content="Browse our collection of authentic luxury perfumes. Filter by brand, gender, concentration, price and more." />
</svelte:head>

<!-- Page Header -->
<div class="bg-gradient-hero pt-32 pb-16">
  <div class="container-luxury text-center">
    <h1 class="text-3xl md:text-5xl font-bold text-white mb-4 font-[var(--font-heading)]">
      Our Collection
    </h1>
    <p class="text-warm-400 font-light text-lg font-[var(--font-accent)]">
      Discover your signature scent from over 500 luxury fragrances
    </p>
  </div>
</div>

<!-- Toolbar -->
<div class="sticky top-[88px] z-30 bg-white border-b border-warm-200 shadow-sm">
  <div class="container-luxury py-4 flex items-center justify-between gap-4">
    <!-- Left: Results count & filter toggle -->
    <div class="flex items-center gap-4">
      <button
        onclick={() => mobileFiltersOpen = !mobileFiltersOpen}
        class="lg:hidden btn-ghost text-xs"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
        </svg>
        Filters
      </button>
      <span class="text-warm-500 text-sm hidden md:block">{products.length} fragrances</span>
    </div>

    <!-- Center: Search -->
    <div class="flex-1 max-w-md">
      <div class="relative">
        <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-warm-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>
        <input
          bind:value={searchQuery}
          type="text"
          placeholder="Search fragrances..."
          class="luxury-input pl-10 py-2.5 text-sm"
        />
      </div>
    </div>

    <!-- Right: Sort & View -->
    <div class="flex items-center gap-3">
      <select
        bind:value={sortBy}
        class="luxury-input py-2 text-sm w-auto pr-8 hidden sm:block"
      >
        {#each sortOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>

      <div class="hidden md:flex items-center border border-warm-200">
        <button
          onclick={() => viewMode = 'grid'}
          class="p-2 transition-colors {viewMode === 'grid' ? 'bg-primary-50 text-primary-600' : 'text-warm-400 hover:text-warm-600'}"
          aria-label="Grid view"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25a2.25 2.25 0 0 1-2.25-2.25v-2.25Z" />
          </svg>
        </button>
        <button
          onclick={() => viewMode = 'list'}
          class="p-2 transition-colors {viewMode === 'list' ? 'bg-primary-50 text-primary-600' : 'text-warm-400 hover:text-warm-600'}"
          aria-label="List view"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</div>

<!-- Main Content -->
<div class="container-luxury py-8">
  <div class="flex gap-8">
    <!-- Sidebar Filters (Desktop) -->
    <aside class="hidden lg:block w-64 flex-shrink-0">
      <div class="sticky top-[160px] space-y-8">
        <!-- Brands -->
        <div>
          <h3 class="text-sm font-semibold uppercase tracking-wider text-warm-900 mb-4">Brand</h3>
          <div class="space-y-2 max-h-60 overflow-y-auto">
            {#each brands as brand}
              <label class="flex items-center gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={selectedBrands.includes(brand)}
                  onchange={() => toggleBrand(brand)}
                  class="w-4 h-4 rounded-none border-warm-300 text-primary-500 focus:ring-primary-500"
                />
                <span class="text-sm text-warm-600 group-hover:text-warm-900 transition-colors">{brand}</span>
              </label>
            {/each}
          </div>
        </div>

        <!-- Gender -->
        <div>
          <h3 class="text-sm font-semibold uppercase tracking-wider text-warm-900 mb-4">Gender</h3>
          <div class="flex flex-wrap gap-2">
            {#each genders as gender}
              <button
                onclick={() => selectedGender = selectedGender === gender ? '' : gender}
                class="px-4 py-2 text-xs tracking-wider uppercase border transition-all duration-300
                  {selectedGender === gender ? 'border-primary-500 bg-primary-50 text-primary-700' : 'border-warm-300 text-warm-600 hover:border-warm-400'}"
              >
                {gender}
              </button>
            {/each}
          </div>
        </div>

        <!-- Concentration -->
        <div>
          <h3 class="text-sm font-semibold uppercase tracking-wider text-warm-900 mb-4">Concentration</h3>
          <div class="space-y-2">
            {#each concentrations as conc}
              <label class="flex items-center gap-3 cursor-pointer group">
                <input
                  type="radio"
                  name="concentration"
                  checked={selectedConcentration === conc}
                  onchange={() => selectedConcentration = selectedConcentration === conc ? '' : conc}
                  class="w-4 h-4 border-warm-300 text-primary-500 focus:ring-primary-500"
                />
                <span class="text-sm text-warm-600 group-hover:text-warm-900 transition-colors">{conc}</span>
              </label>
            {/each}
          </div>
        </div>

        <!-- Price Range -->
        <div>
          <h3 class="text-sm font-semibold uppercase tracking-wider text-warm-900 mb-4">Price Range</h3>
          <div class="flex items-center gap-3">
            <input
              type="number"
              bind:value={priceRange.min}
              placeholder="Min"
              class="luxury-input py-2 text-sm w-full"
            />
            <span class="text-warm-400">—</span>
            <input
              type="number"
              bind:value={priceRange.max}
              placeholder="Max"
              class="luxury-input py-2 text-sm w-full"
            />
          </div>
        </div>

        <!-- Rating -->
        <div>
          <h3 class="text-sm font-semibold uppercase tracking-wider text-warm-900 mb-4">Minimum Rating</h3>
          <div class="flex items-center gap-2">
            {#each [4, 3, 2, 1] as rating}
              <button
                onclick={() => selectedRating = selectedRating === rating ? 0 : rating}
                class="flex items-center gap-1 px-3 py-1.5 border text-xs transition-all
                  {selectedRating === rating ? 'border-primary-500 bg-primary-50' : 'border-warm-300 hover:border-warm-400'}"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                {rating}+
              </button>
            {/each}
          </div>
        </div>

        <!-- Clear Filters -->
        <button
          onclick={() => { selectedBrands = []; selectedGender = ''; selectedConcentration = ''; priceRange = { min: 0, max: 50000 }; selectedRating = 0; }}
          class="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          Clear All Filters
        </button>
      </div>
    </aside>

    <!-- Product Grid -->
    <div class="flex-1">
      <div
        class="{viewMode === 'grid'
          ? 'grid grid-cols-2 md:grid-cols-3 gap-6'
          : 'space-y-4'}"
      >
        {#each products as product, i (product.id)}
          {#if viewMode === 'grid'}
            <!-- Grid Card -->
            <a href="/products/{product.name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}" class="group animate-fade-in" style="animation-delay: {i * 50}ms">
              <div class="luxury-card overflow-hidden">
                <div class="relative aspect-[4/5] overflow-hidden bg-warm-100">
                  <img
                    src={product.image}
                    alt={product.name}
                    class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                    loading="lazy"
                  />
                  {#if product.badge}
                    <span class="absolute top-3 left-3 badge badge-gold text-[10px]">{product.badge}</span>
                  {/if}
                  {#if product.originalPrice}
                    <span class="absolute top-3 right-3 badge badge-danger text-[10px]">
                      -{Math.round((1 - product.price / product.originalPrice) * 100)}%
                    </span>
                  {/if}
                  {#if !product.inStock}
                    <div class="absolute inset-0 bg-warm-900/50 flex items-center justify-center">
                      <span class="text-white text-sm font-medium tracking-wider uppercase">Out of Stock</span>
                    </div>
                  {/if}
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
                <div class="p-4">
                  <p class="text-warm-400 text-xs tracking-[0.15em] uppercase mb-1">{product.brand}</p>
                  <h3 class="text-warm-900 font-medium text-sm mb-1 font-[var(--font-heading)] group-hover:text-primary-600 transition-colors line-clamp-1">{product.name}</h3>
                  <p class="text-warm-400 text-xs mb-2">{product.concentration}</p>
                  <div class="flex items-center gap-1 mb-2">
                    {#each Array(5) as _, j}
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 {j < Math.floor(product.rating) ? 'text-primary-500' : 'text-warm-300'}" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    {/each}
                    <span class="text-warm-400 text-xs ml-1">({product.reviews})</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-warm-900 font-semibold">{formatPrice(product.price)}</span>
                    {#if product.originalPrice}
                      <span class="text-warm-400 text-xs line-through">{formatPrice(product.originalPrice)}</span>
                    {/if}
                  </div>
                </div>
              </div>
            </a>
          {:else}
            <!-- List Card -->
            <a href="/products/{product.name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}" class="group">
              <div class="luxury-card flex overflow-hidden">
                <div class="w-40 h-48 flex-shrink-0 overflow-hidden bg-warm-100">
                  <img src={product.image} alt={product.name} class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy" />
                </div>
                <div class="flex-1 p-5 flex flex-col justify-between">
                  <div>
                    <div class="flex items-start justify-between">
                      <div>
                        <p class="text-warm-400 text-xs tracking-[0.15em] uppercase mb-1">{product.brand}</p>
                        <h3 class="text-warm-900 font-medium text-lg font-[var(--font-heading)] group-hover:text-primary-600 transition-colors">{product.name}</h3>
                      </div>
                      {#if product.badge}
                        <span class="badge badge-gold text-[10px]">{product.badge}</span>
                      {/if}
                    </div>
                    <p class="text-warm-500 text-sm mt-2">{product.concentration} · {product.gender}</p>
                    <div class="flex items-center gap-1 mt-2">
                      {#each Array(5) as _, j}
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5 {j < Math.floor(product.rating) ? 'text-primary-500' : 'text-warm-300'}" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      {/each}
                      <span class="text-warm-400 text-sm ml-1">{product.rating} ({product.reviews} reviews)</span>
                    </div>
                  </div>
                  <div class="flex items-center justify-between mt-4">
                    <div class="flex items-center gap-3">
                      <span class="text-warm-900 font-semibold text-lg">{formatPrice(product.price)}</span>
                      {#if product.originalPrice}
                        <span class="text-warm-400 text-sm line-through">{formatPrice(product.originalPrice)}</span>
                      {/if}
                    </div>
                    <button class="btn-primary text-xs py-2.5 px-6">Add to Cart</button>
                  </div>
                </div>
              </div>
            </a>
          {/if}
        {/each}
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-center gap-2 mt-12">
        <button class="px-4 py-2 border border-warm-300 text-warm-500 text-sm hover:border-primary-500 hover:text-primary-600 transition-colors">
          ← Previous
        </button>
        {#each [1, 2, 3, 4, 5] as page}
          <button
            class="w-10 h-10 text-sm font-medium transition-colors
              {page === 1 ? 'bg-primary-500 text-white' : 'border border-warm-300 text-warm-600 hover:border-primary-500 hover:text-primary-600'}"
          >
            {page}
          </button>
        {/each}
        <button class="px-4 py-2 border border-warm-300 text-warm-500 text-sm hover:border-primary-500 hover:text-primary-600 transition-colors">
          Next →
        </button>
      </div>
    </div>
  </div>
</div>
