<!--
  PerfumeDecantBD — Shopping Cart
-->
<script lang="ts">
  let couponCode = $state('');
  let couponApplied = $state(false);

  let cartItems = $state([
    { id: 1, name: 'Bleu de Chanel', brand: 'Chanel', variant: '100ml EDP', price: 4500, originalPrice: 5200, quantity: 1, image: 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=200&h=250&fit=crop', inStock: true },
    { id: 2, name: 'Sauvage', brand: 'Dior', variant: '100ml EDP', price: 4200, originalPrice: null, quantity: 2, image: 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=200&h=250&fit=crop', inStock: true },
    { id: 3, name: 'Oud Wood', brand: 'Tom Ford', variant: '50ml EDP', price: 8500, originalPrice: 9800, quantity: 1, image: 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=200&h=250&fit=crop', inStock: true },
  ]);

  const subtotal = $derived(cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0));
  const savings = $derived(cartItems.reduce((sum, item) => sum + ((item.originalPrice || item.price) - item.price) * item.quantity, 0));
  const shipping = $derived(subtotal > 5000 ? 0 : 150);
  const tax = $derived(Math.round(subtotal * 0.05));
  const discount = $derived(couponApplied ? Math.round(subtotal * 0.1) : 0);
  const total = $derived(subtotal + shipping + tax - discount);

  const formatPrice = (price: number) => `৳${price.toLocaleString()}`;

  function updateQuantity(id: number, delta: number) {
    cartItems = cartItems.map(item => {
      if (item.id === id) {
        const newQty = Math.max(0, Math.min(10, item.quantity + delta));
        return { ...item, quantity: newQty };
      }
      return item;
    }).filter(item => item.quantity > 0);
  }

  function removeItem(id: number) {
    cartItems = cartItems.filter(item => item.id !== id);
  }
</script>

<svelte:head>
  <title>Shopping Cart — PerfumeDecantBD</title>
</svelte:head>

<div class="pt-32 pb-16">
  <div class="container-luxury">
    <h1 class="text-3xl font-bold font-[var(--font-heading)] text-warm-950 mb-2">Shopping Cart</h1>
    <p class="text-warm-500 mb-10">{cartItems.length} items in your cart</p>

    {#if cartItems.length === 0}
      <div class="text-center py-20">
        <div class="text-6xl mb-6">🛍️</div>
        <h2 class="text-2xl font-semibold font-[var(--font-heading)] text-warm-900 mb-4">Your cart is empty</h2>
        <p class="text-warm-500 mb-8">Looks like you haven't added any fragrances yet.</p>
        <a href="/products" class="btn-primary">Continue Shopping</a>
      </div>
    {:else}
      <div class="grid lg:grid-cols-3 gap-10">
        <!-- Cart Items -->
        <div class="lg:col-span-2 space-y-4">
          {#each cartItems as item (item.id)}
            <div class="luxury-card p-4 md:p-6 flex gap-4 md:gap-6 animate-fade-in">
              <!-- Image -->
              <a href="/products/{item.name.toLowerCase().replace(/\s+/g, '-')}" class="w-24 h-28 md:w-28 md:h-36 flex-shrink-0 overflow-hidden bg-warm-100">
                <img src={item.image} alt={item.name} class="w-full h-full object-cover" />
              </a>

              <!-- Info -->
              <div class="flex-1 flex flex-col justify-between min-w-0">
                <div>
                  <div class="flex items-start justify-between gap-2">
                    <div>
                      <p class="text-warm-400 text-xs tracking-[0.15em] uppercase">{item.brand}</p>
                      <h3 class="text-warm-900 font-medium font-[var(--font-heading)] text-sm md:text-base">{item.name}</h3>
                      <p class="text-warm-500 text-xs mt-0.5">{item.variant}</p>
                    </div>
                    <button onclick={() => removeItem(item.id)} class="text-warm-400 hover:text-red-500 transition-colors p-1" aria-label="Remove item">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>

                <div class="flex items-center justify-between mt-4">
                  <!-- Quantity -->
                  <div class="flex items-center border border-warm-300">
                    <button onclick={() => updateQuantity(item.id, -1)} class="w-8 h-8 flex items-center justify-center text-warm-600 hover:bg-warm-50 text-sm">−</button>
                    <span class="w-10 h-8 flex items-center justify-center text-sm font-medium border-x border-warm-300">{item.quantity}</span>
                    <button onclick={() => updateQuantity(item.id, 1)} class="w-8 h-8 flex items-center justify-center text-warm-600 hover:bg-warm-50 text-sm">+</button>
                  </div>
                  <!-- Price -->
                  <div class="text-right">
                    <p class="text-warm-900 font-semibold">{formatPrice(item.price * item.quantity)}</p>
                    {#if item.originalPrice}
                      <p class="text-warm-400 text-xs line-through">{formatPrice(item.originalPrice * item.quantity)}</p>
                    {/if}
                  </div>
                </div>
              </div>
            </div>
          {/each}

          <a href="/products" class="inline-flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 font-medium mt-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
            </svg>
            Continue Shopping
          </a>
        </div>

        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <div class="luxury-card p-6 sticky top-32">
            <h2 class="text-lg font-semibold font-[var(--font-heading)] text-warm-950 mb-6">Order Summary</h2>

            <!-- Coupon -->
            <div class="mb-6">
              <div class="flex gap-2">
                <input
                  bind:value={couponCode}
                  type="text"
                  placeholder="Coupon code"
                  class="luxury-input py-2.5 text-sm flex-1"
                />
                <button
                  onclick={() => { if (couponCode) couponApplied = true; }}
                  class="btn-secondary py-2.5 px-4 text-xs"
                >
                  Apply
                </button>
              </div>
              {#if couponApplied}
                <p class="text-green-600 text-xs mt-2 flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" /></svg>
                  Coupon applied! 10% discount
                </p>
              {/if}
            </div>

            <div class="space-y-3 text-sm">
              <div class="flex justify-between text-warm-600">
                <span>Subtotal</span>
                <span>{formatPrice(subtotal)}</span>
              </div>
              {#if savings > 0}
                <div class="flex justify-between text-green-600">
                  <span>You save</span>
                  <span>-{formatPrice(savings)}</span>
                </div>
              {/if}
              {#if discount > 0}
                <div class="flex justify-between text-green-600">
                  <span>Coupon discount</span>
                  <span>-{formatPrice(discount)}</span>
                </div>
              {/if}
              <div class="flex justify-between text-warm-600">
                <span>Shipping</span>
                <span>{shipping === 0 ? 'Free' : formatPrice(shipping)}</span>
              </div>
              <div class="flex justify-between text-warm-600">
                <span>Tax (5%)</span>
                <span>{formatPrice(tax)}</span>
              </div>
              <div class="luxury-divider my-2"></div>
              <div class="flex justify-between text-warm-950 font-semibold text-base">
                <span>Total</span>
                <span>{formatPrice(total)}</span>
              </div>
            </div>

            {#if subtotal < 5000}
              <p class="text-xs text-primary-600 mt-4 p-3 bg-primary-50 border border-primary-200">
                Add {formatPrice(5000 - subtotal)} more for <strong>free shipping</strong>
              </p>
            {/if}

            <a href="/checkout" class="btn-primary w-full mt-6 py-4 text-center block">
              Proceed to Checkout
            </a>

            <!-- Trust badges -->
            <div class="flex items-center justify-center gap-4 mt-6 text-warm-400 text-xs">
              <span>🔒 Secure</span>
              <span>✓ Authentic</span>
              <span>📦 Tracked</span>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
