<script lang="ts">
  import { Star, ShieldCheck, Truck, RefreshCw, ShoppingBag, Heart, Minus, Plus, ChevronRight } from '@lucide/svelte';
  import { cart } from '$lib/stores/cart.svelte';
  import { formatPrice } from '$lib/utils/formatters';
  import { Button } from '$lib/components/ui/button';
  import { toast } from 'svelte-sonner';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  // Computed values
  const product = $derived(data.product);
  const relatedProducts = $derived(data.relatedProducts);

  // Parse sizes options
  const sizes = $derived((product.sizes && Array.isArray(product.sizes)) ? product.sizes : []);

  // UI state
  let selectedSizeIndex = $state(0);
  let quantity = $state(1);
  let activeTab = $state<'desc' | 'notes' | 'shipping'>('desc');
  
  // Gallery state
  const images = $derived(product.product_images || []);
  let activeImageIndex = $state(0);
  const activeImageUrl = $derived(images[activeImageIndex]?.url || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=600');

  // Selected size properties
  const currentSize = $derived(sizes[selectedSizeIndex] || null);
  const currentPrice = $derived(currentSize ? currentSize.price : product.price);

  function adjustQuantity(delta: number) {
    quantity = Math.max(1, Math.min(quantity + delta, product.stock_quantity));
  }

  function handleAddToCart() {
    const sizeLabel = currentSize ? currentSize.label : null;
    
    cart.addItem({
      product_id: product.id,
      product_name: product.name,
      product_image: activeImageUrl,
      product_slug: product.slug,
      brand: product.brand,
      size: sizeLabel,
      quantity: quantity,
      unit_price: currentPrice,
      max_stock: product.stock_quantity
    });

    toast.success(`Added ${quantity}x ${product.name} (${sizeLabel || 'Default'}) to cart`, {
      action: {
        label: 'View Cart',
        onClick: () => cart.openCart()
      }
    });
  }
</script>

<svelte:head>
  <title>{product.name} — {product.brand}</title>
  <meta name="description" content={product.short_description || `Buy authentic ${product.name} perfume decant by ${product.brand} in Bangladesh. High quality atomizers, fast delivery.`} />
  <meta property="og:title" content="{product.name} — {product.brand}" />
  <meta property="og:description" content={product.short_description || `Buy authentic ${product.name} perfume decant by ${product.brand} in Bangladesh.`} />
  <meta property="og:type" content="product" />
  <meta property="og:image" content={activeImageUrl} />
</svelte:head>

<div class="bg-[var(--bg-primary)] py-8 lg:py-16">
  <div class="container-luxury">
    <!-- Breadcrumbs -->
    <nav class="mb-8 flex text-xs tracking-wider uppercase text-[var(--text-muted)]" aria-label="Breadcrumb">
      <a href="/" class="hover:text-burgundy-700">Home</a>
      <span class="mx-2">/</span>
      <a href="/shop" class="hover:text-burgundy-700">Shop</a>
      <span class="mx-2">/</span>
      <span class="text-gray-900 dark:text-white font-medium">{product.name}</span>
    </nav>

    <!-- Main Product Layout -->
    <div class="grid gap-12 lg:grid-cols-2">
      <!-- Left: Image Gallery -->
      <div class="space-y-4">
        <!-- Main Image -->
        <div class="relative aspect-square overflow-hidden rounded-2xl bg-gray-50 border border-gray-100 dark:bg-gray-900 dark:border-gray-800">
          <img
            src={activeImageUrl}
            alt={product.name}
            class="h-full w-full object-cover transition-all duration-300"
          />
          {#if product.is_bestseller}
            <span class="absolute left-4 top-4 rounded-full bg-gold-500 px-3 py-1.5 text-xs font-bold text-burgundy-950 uppercase tracking-wider">
              Bestseller
            </span>
          {/if}
        </div>

        <!-- Thumbnails -->
        {#if images.length > 1}
          <div class="flex gap-3 overflow-x-auto pb-2">
            {#each images as img, idx}
              <button
                onclick={() => (activeImageIndex = idx)}
                class="relative aspect-square w-20 shrink-0 overflow-hidden rounded-xl border-2 transition-all {activeImageIndex === idx ? 'border-burgundy-700 dark:border-gold-500' : 'border-transparent bg-gray-50 dark:bg-gray-900'}"
              >
                <img src={img.url} alt="" class="h-full w-full object-cover" />
              </button>
            {/each}
          </div>
        {/if}
      </div>

      <!-- Right: Product Information -->
      <div class="flex flex-col justify-between">
        <div class="space-y-6">
          <div>
            <p class="text-sm font-semibold uppercase tracking-wider text-gold-600">{product.brand}</p>
            <h1 class="font-heading mt-2 text-3xl font-bold lg:text-4xl">{product.name}</h1>
          </div>

          <!-- Price Display -->
          <div class="flex items-baseline gap-3">
            {#if product.discount_price && !currentSize}
              <span class="font-heading text-3xl font-bold text-burgundy-700 dark:text-gold-400">
                {formatPrice(product.discount_price)}
              </span>
              <span class="text-base text-gray-400 line-through">
                {formatPrice(product.price)}
              </span>
            {:else}
              <span class="font-heading text-3xl font-bold text-burgundy-700 dark:text-gold-400">
                {formatPrice(currentPrice)}
              </span>
            {/if}
            {#if currentSize}
              <span class="text-sm text-[var(--text-muted)]">For {currentSize.label} size</span>
            {/if}
          </div>

          <!-- Short Description -->
          <p class="text-sm leading-relaxed text-[var(--text-secondary)]">
            {product.short_description || 'Experience the olfactory elegance of this masterfully crafted fragrance, hand-decanted with precision.'}
          </p>

          <!-- Size Selector -->
          {#if sizes.length > 0}
            <div class="space-y-2">
              <label class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]" for="size-selector">Select Decant Size</label>
              <div id="size-selector" class="flex flex-wrap gap-3">
                {#each sizes as size, idx}
                  <button
                    onclick={() => (selectedSizeIndex = idx)}
                    class="btn-press rounded-xl border-2 px-5 py-3 text-sm font-semibold transition-all {selectedSizeIndex === idx 
                      ? 'border-burgundy-700 bg-burgundy-50/55 text-burgundy-900 dark:border-gold-500 dark:bg-gold-950/20 dark:text-gold-400' 
                      : 'border-gray-200 hover:border-gray-400 dark:border-gray-800'}"
                  >
                    <span class="block text-xs uppercase tracking-wider">{size.label}</span>
                    <span class="mt-0.5 block text-base font-bold">{formatPrice(size.price)}</span>
                  </button>
                {/each}
              </div>
            </div>
          {/if}

          <!-- Quantity and Add to Cart -->
          <div class="space-y-4 pt-4">
            <div class="flex items-center gap-4">
              <!-- Quantity Selector -->
              <div class="flex h-12 items-center rounded-xl border border-gray-200 dark:border-gray-800">
                <button
                  onclick={() => adjustQuantity(-1)}
                  class="flex h-full w-12 items-center justify-center transition-colors hover:bg-gray-100 dark:hover:bg-gray-900"
                  aria-label="Decrease quantity"
                >
                  <Minus class="h-4 w-4" />
                </button>
                <span class="w-12 text-center text-sm font-semibold">{quantity}</span>
                <button
                  onclick={() => adjustQuantity(1)}
                  class="flex h-full w-12 items-center justify-center transition-colors hover:bg-gray-100 dark:hover:bg-gray-900"
                  aria-label="Increase quantity"
                >
                  <Plus class="h-4 w-4" />
                </button>
              </div>

              <!-- Add to Cart Button -->
              <Button
                size="lg"
                class="h-12 flex-1 bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold rounded-xl flex items-center justify-center gap-2"
                onclick={handleAddToCart}
                disabled={product.stock_quantity <= 0}
              >
                <ShoppingBag class="h-4.5 w-4.5" />
                {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
              </Button>

              <!-- Wishlist Placeholder -->
              <button
                class="flex h-12 w-12 items-center justify-center rounded-xl border border-gray-200 hover:bg-gray-50 dark:border-gray-800 dark:hover:bg-gray-900 transition-colors"
                aria-label="Add to wishlist"
                onclick={() => toast.info('Wishlist feature is a UI placeholder')}
              >
                <Heart class="h-5 w-5 text-gray-500" />
              </button>
            </div>

            <!-- Stock status -->
            <p class="text-xs text-[var(--text-muted)]">
              {#if product.stock_quantity > 0}
                Availability: <span class="font-bold text-green-600">In Stock ({product.stock_quantity} left)</span>
              {:else}
                Availability: <span class="font-bold text-red-500">Temporarily Out of Stock</span>
              {/if}
            </p>
          </div>
        </div>

        <!-- Trust Badges -->
        <div class="mt-8 grid grid-cols-3 gap-4 border-t border-gray-100 pt-6 dark:border-gray-800">
          <div class="flex flex-col items-center text-center">
            <ShieldCheck class="h-6 w-6 text-gold-500" />
            <span class="mt-2 text-xs font-semibold">100% Authentic</span>
          </div>
          <div class="flex flex-col items-center text-center">
            <Truck class="h-6 w-6 text-gold-500" />
            <span class="mt-2 text-xs font-semibold">Fast Delivery</span>
          </div>
          <div class="flex flex-col items-center text-center">
            <RefreshCw class="h-6 w-6 text-gold-500" />
            <span class="mt-2 text-xs font-semibold">Secure Payout</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Description & Fragrance Notes Tabs -->
    <div class="mt-16 border-t border-gray-100 pt-10 dark:border-gray-800">
      <div class="flex border-b border-gray-100 dark:border-gray-800">
        {#each [
          { key: 'desc', label: 'Product Details' },
          { key: 'notes', label: 'Fragrance Notes' },
          { key: 'shipping', label: 'Shipping & Delivery' }
        ] as tab}
          <button
            onclick={() => (activeTab = tab.key as any)}
            class="border-b-2 px-6 py-3.5 text-sm font-semibold uppercase tracking-wider transition-all {activeTab === tab.key 
              ? 'border-burgundy-700 text-burgundy-800 dark:border-gold-500 dark:text-gold-400' 
              : 'border-transparent text-gray-500 hover:text-burgundy-700'}"
          >
            {tab.label}
          </button>
        {/each}
      </div>

      <div class="py-8">
        {#if activeTab === 'desc'}
          <div class="prose dark:prose-invert max-w-none text-sm leading-relaxed text-[var(--text-secondary)]">
            <p>{product.description || 'No detailed description available.'}</p>
          </div>
        {:else if activeTab === 'notes'}
          <!-- Visual Fragrance Notes -->
          <div class="grid gap-8 md:grid-cols-3">
            <!-- Top Notes -->
            <div class="card-premium p-6 text-center">
              <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">Initial Impression</span>
              <h3 class="font-heading mt-2 text-lg font-bold">Top Notes</h3>
              <div class="mt-4 flex flex-wrap justify-center gap-1.5">
                {#each product.top_notes || ['None'] as note}
                  <span class="rounded-full border border-gray-200 px-3.5 py-1 text-xs dark:border-gray-800">{note}</span>
                {/each}
              </div>
            </div>
            <!-- Middle Notes -->
            <div class="card-premium p-6 text-center">
              <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">Heart of Fragrance</span>
              <h3 class="font-heading mt-2 text-lg font-bold">Middle / Heart Notes</h3>
              <div class="mt-4 flex flex-wrap justify-center gap-1.5">
                {#each product.middle_notes || ['None'] as note}
                  <span class="rounded-full border border-gray-200 px-3.5 py-1 text-xs dark:border-gray-800">{note}</span>
                {/each}
              </div>
            </div>
            <!-- Base Notes -->
            <div class="card-premium p-6 text-center">
              <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">Lingering Trace</span>
              <h3 class="font-heading mt-2 text-lg font-bold">Base Notes</h3>
              <div class="mt-4 flex flex-wrap justify-center gap-1.5">
                {#each product.base_notes || ['None'] as note}
                  <span class="rounded-full border border-gray-200 px-3.5 py-1 text-xs dark:border-gray-800">{note}</span>
                {/each}
              </div>
            </div>
          </div>
        {:else if activeTab === 'shipping'}
          <div class="space-y-4 text-sm text-[var(--text-secondary)] leading-relaxed">
            <h3 class="font-heading text-lg font-bold">Delivery inside Bangladesh</h3>
            <p>We deliver nationwide inside Bangladesh. Orders inside Dhaka are delivered in 1-2 days, outside Dhaka in 2-3 business days.</p>
            <p><strong>Shipping Rates:</strong> Inside Dhaka ৳80 and outside Dhaka ৳140. Free shipping for orders above ৳5,000.</p>
          </div>
        {/if}
      </div>
    </div>

    <!-- Related Products -->
    {#if relatedProducts.length > 0}
      <div class="mt-16 border-t border-gray-100 pt-10 dark:border-gray-800">
        <h2 class="font-heading text-2xl font-bold">You May Also Like</h2>
        <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {#each relatedProducts as rel}
            {@const relImage = rel.product_images?.[0]?.url || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'}
            <a href="/product/{rel.slug}" class="group card-premium overflow-hidden">
              <div class="relative aspect-[4/5] overflow-hidden bg-gray-50 dark:bg-gray-900">
                <img
                  src={relImage}
                  alt={rel.name}
                  class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
                  loading="lazy"
                />
              </div>
              <div class="p-4">
                <p class="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">{rel.brand}</p>
                <h3 class="mt-1 font-heading text-base font-bold group-hover:text-burgundy-700 dark:group-hover:text-gold-400 transition-colors">
                  {rel.name}
                </h3>
                <p class="mt-2 font-heading font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(rel.price)}</p>
              </div>
            </a>
          {/each}
        </div>
      </div>
    {/if}
  </div>
</div>
