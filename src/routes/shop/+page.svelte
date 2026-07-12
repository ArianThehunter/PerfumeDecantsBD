<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { Star, SlidersHorizontal, Search, X, ChevronDown, ChevronLeft, ChevronRight, ShoppingBag } from '@lucide/svelte';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { cart } from '$lib/stores/cart.svelte';
  import { formatPrice } from '$lib/utils/formatters';
  import { toast } from 'svelte-sonner';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  // Filter state (runes)
  let searchInput = $state('');
  let showMobileFilters = $state(false);

  $effect(() => {
    searchInput = data.filters.search;
  });

  // Computed values
  const products = $derived(data.products);
  const totalCount = $derived(data.totalCount);
  const categories = $derived(data.categories);
  const brands = $derived(data.brands);
  const filters = $derived(data.filters);
  
  const totalPages = $derived(Math.ceil(totalCount / filters.perPage));

  function updateFilters(newParams: Record<string, string | number | null>) {
    const url = new URL(page.url);
    
    // Always reset page when filters change, unless page is explicitly passed
    if (!('page' in newParams)) {
      url.searchParams.set('page', '1');
    }

    Object.entries(newParams).forEach(([key, val]) => {
      if (val === null || val === '') {
        url.searchParams.delete(key);
      } else {
        url.searchParams.set(key, String(val));
      }
    });

    goto(url.toString(), { keepFocus: true, noScroll: false });
  }

  function handleSearchSubmit(e: Event) {
    e.preventDefault();
    updateFilters({ search: searchInput });
  }

  function clearAllFilters() {
    searchInput = '';
    goto('/shop');
  }

  function handleAddToCart(e: MouseEvent, product: any) {
    e.preventDefault();
    e.stopPropagation();

    // Default to the first size or price if size array is present
    let sizeLabel = null;
    let sizePrice = product.price;

    if (product.sizes && Array.isArray(product.sizes) && product.sizes.length > 0) {
      const firstSize = product.sizes[0];
      sizeLabel = firstSize.label;
      sizePrice = firstSize.price;
    }

    const primaryImage = product.product_images?.find((img: any) => img.is_primary)?.url 
      || product.product_images?.[0]?.url 
      || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400';

    cart.addItem({
      product_id: product.id,
      product_name: product.name,
      product_image: primaryImage,
      product_slug: product.slug,
      brand: product.brand,
      size: sizeLabel,
      quantity: 1,
      unit_price: sizePrice,
      max_stock: product.stock_quantity
    });

    toast.success(`${product.name} added to cart`, {
      action: {
        label: 'View Cart',
        onClick: () => cart.openCart()
      }
    });
  }
  const shopSettings = $derived(page.data.settings?.shop_page || {});
  const shopTitle = $derived(shopSettings.title || 'All Fragrances');
  const shopSubtitle = $derived(shopSettings.subtitle || `Showing ${products.length} of ${totalCount} authentic luxury perfume decants`);
</script>

<svelte:head>
  <title>{shopTitle} — PerfumeDecantsBD</title>
</svelte:head>

<div class="bg-[var(--bg-primary)] py-8 lg:py-12">
  <div class="container-luxury">
    <!-- Breadcrumbs -->
    <nav class="mb-6 flex text-xs tracking-wider uppercase text-[var(--text-muted)]" aria-label="Breadcrumb">
      <a href="/" class="hover:text-burgundy-700">Home</a>
      <span class="mx-2">/</span>
      <span class="text-gray-900 dark:text-white font-medium">Shop</span>
    </nav>

    <!-- Page Title & Header -->
    <div class="flex flex-col gap-4 border-b border-gray-100 pb-8 dark:border-gray-800 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <h1 class="font-heading text-3xl font-bold lg:text-4xl">{shopTitle}</h1>
        <p class="mt-2 text-sm text-[var(--text-muted)]">{shopSubtitle}</p>
      </div>

      <!-- Quick Actions -->
      <div class="flex items-center gap-3">
        <!-- Mobile Filters Button -->
        <Button
          variant="outline"
          class="flex items-center gap-2 lg:hidden"
          onclick={() => (showMobileFilters = true)}
        >
          <SlidersHorizontal class="h-4 w-4" />
          Filters
        </Button>

        <!-- Search Bar -->
        <form onsubmit={handleSearchSubmit} class="relative flex-1 sm:w-80">
          <Input
            type="search"
            placeholder="Search brand or name..."
            bind:value={searchInput}
            class="pl-10 pr-4"
          />
          <button type="submit" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
            <Search class="h-4 w-4" />
          </button>
        </form>

        <!-- Sort selector -->
        <div class="relative">
          <select
            value={filters.sort}
            onchange={(e) => updateFilters({ sort: (e.target as HTMLSelectElement).value })}
            class="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            aria-label="Sort products"
          >
            <option value="popular">Sort: Popular</option>
            <option value="newest">Sort: Newest</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Active Filters Row -->
    {#if filters.category || filters.brand || filters.gender || filters.search}
      <div class="flex flex-wrap items-center gap-2 py-4">
        <span class="text-xs text-[var(--text-muted)] uppercase tracking-wider">Active Filters:</span>
        {#if filters.search}
          <span class="inline-flex items-center gap-1 rounded-full bg-burgundy-50 px-3 py-1 text-xs text-burgundy-800 dark:bg-burgundy-950 dark:text-gold-400">
            "{filters.search}"
            <button onclick={() => { searchInput = ''; updateFilters({ search: null }); }}><X class="h-3 w-3" /></button>
          </span>
        {/if}
        {#if filters.category}
          <span class="inline-flex items-center gap-1 rounded-full bg-burgundy-50 px-3 py-1 text-xs text-burgundy-800 dark:bg-burgundy-950 dark:text-gold-400">
            {categories.find(c => c.slug === filters.category)?.name || filters.category}
            <button onclick={() => updateFilters({ category: null })}><X class="h-3 w-3" /></button>
          </span>
        {/if}
        {#if filters.brand}
          <span class="inline-flex items-center gap-1 rounded-full bg-burgundy-50 px-3 py-1 text-xs text-burgundy-800 dark:bg-burgundy-950 dark:text-gold-400">
            {filters.brand}
            <button onclick={() => updateFilters({ brand: null })}><X class="h-3 w-3" /></button>
          </span>
        {/if}
        {#if filters.gender}
          <span class="inline-flex items-center gap-1 rounded-full bg-burgundy-50 px-3 py-1 text-xs text-burgundy-800 dark:bg-burgundy-950 dark:text-gold-400 capitalize">
            {filters.gender}
            <button onclick={() => updateFilters({ gender: null })}><X class="h-3 w-3" /></button>
          </span>
        {/if}
        <button
          onclick={clearAllFilters}
          class="text-xs font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline"
        >
          Clear All
        </button>
      </div>
    {/if}

    <div class="mt-8 grid gap-8 lg:grid-cols-[250px_1fr]">
      <!-- Desktop Filters Sidebar -->
      <aside class="hidden space-y-6 lg:block">
        <!-- Categories -->
        <div>
          <h3 class="font-heading text-base font-bold text-burgundy-850 dark:text-cream-200">Categories</h3>
          <div class="mt-3 space-y-2">
            <button
              onclick={() => updateFilters({ category: null })}
              class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {!filters.category ? 'font-bold text-burgundy-800 dark:text-gold-400' : 'text-gray-600 dark:text-gray-400'}"
            >
              All Categories
            </button>
            {#each categories as cat}
              <button
                onclick={() => updateFilters({ category: cat.slug })}
                class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {filters.category === cat.slug ? 'font-bold text-burgundy-800 dark:text-gold-400' : 'text-gray-600 dark:text-gray-400'}"
              >
                {cat.name}
              </button>
            {/each}
          </div>
        </div>

        <!-- Gender -->
        <div>
          <h3 class="font-heading text-base font-bold text-burgundy-850 dark:text-cream-200">Gender</h3>
          <div class="mt-3 space-y-2">
            {#each [
              { val: null, label: 'All Genders' },
              { val: 'men', label: 'For Men' },
              { val: 'women', label: 'For Women' },
              { val: 'unisex', label: 'Unisex' }
            ] as g}
              <button
                onclick={() => updateFilters({ gender: g.val })}
                class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {filters.gender === g.val ? 'font-bold text-burgundy-800 dark:text-gold-400' : 'text-gray-600 dark:text-gray-400'}"
              >
                {g.label}
              </button>
            {/each}
          </div>
        </div>

        <!-- Brands -->
        <div>
          <h3 class="font-heading text-base font-bold text-burgundy-850 dark:text-cream-200">Brands</h3>
          <div class="mt-3 space-y-2">
            <button
              onclick={() => updateFilters({ brand: null })}
              class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {!filters.brand ? 'font-bold text-burgundy-800 dark:text-gold-400' : 'text-gray-600 dark:text-gray-400'}"
            >
              All Brands
            </button>
            {#each brands as b}
              <button
                onclick={() => updateFilters({ brand: b })}
                class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {filters.brand === b ? 'font-bold text-burgundy-800 dark:text-gold-400' : 'text-gray-600 dark:text-gray-400'}"
              >
                {b}
              </button>
            {/each}
          </div>
        </div>

        <!-- Price Range -->
        <div>
          <h3 class="font-heading text-base font-bold text-burgundy-850 dark:text-cream-200">Price Range</h3>
          <div class="mt-4 space-y-4">
            <div class="flex gap-2">
              <div class="flex-1">
                <label for="min-price" class="text-xs text-[var(--text-muted)] uppercase">Min (৳)</label>
                <Input
                  id="min-price"
                  type="number"
                  value={filters.minPrice}
                  onchange={(e) => updateFilters({ min_price: (e.target as HTMLInputElement).value })}
                />
              </div>
              <div class="flex-1">
                <label for="max-price" class="text-xs text-[var(--text-muted)] uppercase">Max (৳)</label>
                <Input
                  id="max-price"
                  type="number"
                  value={filters.maxPrice}
                  onchange={(e) => updateFilters({ max_price: (e.target as HTMLInputElement).value })}
                />
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Product List & Grid -->
      <div>
        {#if products.length === 0}
          <div class="flex min-h-[400px] flex-col items-center justify-center text-center">
            <ShoppingBag class="h-16 w-16 text-gray-350" />
            <h3 class="mt-4 font-heading text-xl font-bold">No Products Found</h3>
            <p class="mt-1 text-sm text-[var(--text-muted)]">Try adjusting your filters or search term.</p>
            <Button class="mt-6" onclick={clearAllFilters}>Reset Filters</Button>
          </div>
        {:else}
          <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {#each products as product}
              {@const primaryImage = product.product_images?.find((img: any) => img.is_primary)?.url 
                || product.product_images?.[0]?.url 
                || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'}
              <a href="/product/{product.slug}" class="group card-premium flex flex-col justify-between overflow-hidden">
                <div>
                  <div class="relative aspect-[4/5] overflow-hidden bg-gray-50 dark:bg-gray-900">
                    <img
                      src={primaryImage}
                      alt={product.name}
                      class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
                      loading="lazy"
                    />
                    
                    <!-- Labels -->
                    <div class="absolute left-3 top-3 flex flex-col gap-1.5">
                      {#if product.is_bestseller}
                        <span class="rounded-full bg-gold-500 px-2.5 py-1 text-[9px] font-bold text-burgundy-950 uppercase tracking-wider">
                          Bestseller
                        </span>
                      {/if}
                      {#if product.is_new_arrival}
                        <span class="rounded-full bg-burgundy-800 px-2.5 py-1 text-[9px] font-bold text-white uppercase tracking-wider">
                          New
                        </span>
                      {/if}
                    </div>

                    <!-- Gender Label -->
                    <span class="absolute bottom-3 left-3 rounded-full bg-black/60 px-2 py-0.5 text-[10px] font-medium text-white backdrop-blur-sm capitalize">
                      {product.gender}
                    </span>

                    <!-- Quick Add Button Overlay -->
                    <button
                      onclick={(e) => handleAddToCart(e, product)}
                      class="absolute bottom-3 right-3 flex h-10 w-10 items-center justify-center rounded-full bg-white text-burgundy-950 shadow-md transition-all hover:scale-110 hover:bg-gold-500 hover:text-burgundy-950 dark:bg-gray-900 dark:text-white"
                      aria-label="Quick Add to Cart"
                    >
                      <ShoppingBag class="h-4.5 w-4.5" />
                    </button>
                  </div>

                  <div class="p-4">
                    <p class="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">{product.brand}</p>
                    <h3 class="mt-1 font-heading text-base font-bold group-hover:text-burgundy-700 dark:group-hover:text-gold-400 transition-colors">
                      {product.name}
                    </h3>
                    <div class="mt-1 flex items-center gap-1">
                      {#each Array(5) as _, i}
                        <Star class="h-3 w-3 {i < Math.floor(product.rating) ? 'fill-gold-400 text-gold-400' : 'text-gray-300'}" />
                      {/each}
                      <span class="ml-1 text-xs text-[var(--text-muted)]">({product.review_count})</span>
                    </div>
                  </div>
                </div>

                <div class="border-t border-gray-50 p-4 dark:border-gray-900">
                  <div class="flex items-center justify-between">
                    <div>
                      {#if product.discount_price}
                        <span class="font-heading text-lg font-bold text-burgundy-700 dark:text-gold-400">
                          {formatPrice(product.discount_price)}
                        </span>
                        <span class="ml-1.5 text-xs text-gray-400 line-through">
                          {formatPrice(product.price)}
                        </span>
                      {:else}
                        <span class="font-heading text-lg font-bold text-burgundy-700 dark:text-gold-400">
                          {formatPrice(product.price)}
                        </span>
                      {/if}
                      <span class="block text-[10px] text-gray-500">From decant size</span>
                    </div>

                    <span class="text-xs font-medium {product.stock_quantity > 0 ? 'text-green-600' : 'text-red-500'}">
                      {product.stock_quantity > 0 ? 'In Stock' : 'Out of Stock'}
                    </span>
                  </div>
                </div>
              </a>
            {/each}
          </div>

          <!-- Pagination -->
          {#if totalPages > 1}
            <nav class="mt-12 flex justify-center gap-1.5" aria-label="Pagination">
              <Button
                variant="outline"
                size="icon"
                disabled={filters.page <= 1}
                onclick={() => updateFilters({ page: filters.page - 1 })}
                aria-label="Previous page"
              >
                <ChevronLeft class="h-4 w-4" />
              </Button>

              {#each Array(totalPages) as _, i}
                {@const pNum = i + 1}
                <Button
                  variant={filters.page === pNum ? 'default' : 'outline'}
                  onclick={() => updateFilters({ page: pNum })}
                  class={filters.page === pNum ? 'bg-burgundy-700 hover:bg-burgundy-800' : ''}
                >
                  {pNum}
                </Button>
              {/each}

              <Button
                variant="outline"
                size="icon"
                disabled={filters.page >= totalPages}
                onclick={() => updateFilters({ page: filters.page + 1 })}
                aria-label="Next page"
              >
                <ChevronRight class="h-4 w-4" />
              </Button>
            </nav>
          {/if}
        {/if}
      </div>
    </div>
  </div>
</div>

<!-- Mobile Filters Drawer -->
{#if showMobileFilters}
  <div class="fixed inset-0 z-50 lg:hidden">
    <!-- Backdrop -->
    <button
      class="absolute inset-0 bg-black/60 backdrop-blur-xs"
      onclick={() => (showMobileFilters = false)}
      aria-label="Close filters"
      tabindex="-1"
    ></button>

    <!-- Content Panel -->
    <div class="absolute right-0 top-0 h-full w-80 max-w-[85vw] bg-white p-6 shadow-2xl dark:bg-gray-950 flex flex-col justify-between overflow-y-auto">
      <div class="space-y-6">
        <div class="flex items-center justify-between border-b pb-4">
          <h2 class="font-heading text-lg font-bold">Filters</h2>
          <button
            onclick={() => (showMobileFilters = false)}
            class="flex h-8 w-8 items-center justify-center rounded-full hover:bg-gray-100"
            aria-label="Close filters"
          >
            <X class="h-4 w-4" />
          </button>
        </div>

        <!-- Mobile Categories -->
        <div>
          <h3 class="font-heading text-sm font-bold text-burgundy-850 dark:text-cream-200">Categories</h3>
          <div class="mt-3 space-y-2">
            <button
              onclick={() => { updateFilters({ category: null }); showMobileFilters = false; }}
              class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {!filters.category ? 'font-bold text-burgundy-800' : 'text-gray-600'}"
            >
              All Categories
            </button>
            {#each categories as cat}
              <button
                onclick={() => { updateFilters({ category: cat.slug }); showMobileFilters = false; }}
                class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {filters.category === cat.slug ? 'font-bold text-burgundy-800' : 'text-gray-600'}"
              >
                {cat.name}
              </button>
            {/each}
          </div>
        </div>

        <!-- Mobile Gender -->
        <div>
          <h3 class="font-heading text-sm font-bold text-burgundy-850 dark:text-cream-200">Gender</h3>
          <div class="mt-3 space-y-2">
            {#each [
              { val: null, label: 'All Genders' },
              { val: 'men', label: 'For Men' },
              { val: 'women', label: 'For Women' },
              { val: 'unisex', label: 'Unisex' }
            ] as g}
              <button
                onclick={() => { updateFilters({ gender: g.val }); showMobileFilters = false; }}
                class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {filters.gender === g.val ? 'font-bold text-burgundy-800' : 'text-gray-600'}"
              >
                {g.label}
              </button>
            {/each}
          </div>
        </div>

        <!-- Mobile Brands -->
        <div>
          <h3 class="font-heading text-sm font-bold text-burgundy-850 dark:text-cream-200">Brands</h3>
          <div class="mt-3 space-y-2">
            <button
              onclick={() => { updateFilters({ brand: null }); showMobileFilters = false; }}
              class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {!filters.brand ? 'font-bold text-burgundy-800' : 'text-gray-600'}"
            >
              All Brands
            </button>
            {#each brands as b}
              <button
                onclick={() => { updateFilters({ brand: b }); showMobileFilters = false; }}
                class="block w-full text-left text-sm transition-colors hover:text-burgundy-700 {filters.brand === b ? 'font-bold text-burgundy-800' : 'text-gray-600'}"
              >
                {b}
              </button>
            {/each}
          </div>
        </div>
      </div>

      <div class="border-t pt-4 mt-6">
        <Button class="w-full bg-burgundy-700 hover:bg-burgundy-800" onclick={() => (showMobileFilters = false)}>
          Apply Filters
        </Button>
      </div>
    </div>
  </div>
{/if}
