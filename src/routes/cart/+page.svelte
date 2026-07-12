<script lang="ts">
  import { cart } from '$lib/stores/cart.svelte';
  import { formatPrice } from '$lib/utils/formatters';
  import { Trash2, Minus, Plus, ShoppingBag, ArrowRight, ArrowLeft } from '@lucide/svelte';
  import { Button } from '$lib/components/ui/button';
  import { Separator } from '$lib/components/ui/separator';
</script>

<svelte:head>
  <title>Shopping Cart — PerfumeDecantsBD</title>
</svelte:head>

<div class="bg-[var(--bg-secondary)] py-10 lg:py-16 min-h-[80vh]">
  <div class="container-luxury">
    <h1 class="font-heading text-3xl font-bold mb-8">Shopping Cart</h1>

    {#if cart.items.length === 0}
      <div class="card-premium p-12 text-center flex flex-col items-center justify-center min-h-[400px]">
        <div class="flex h-20 w-20 items-center justify-center rounded-full bg-burgundy-50 dark:bg-burgundy-950">
          <ShoppingBag class="h-10 w-10 text-burgundy-300 dark:text-burgundy-700" />
        </div>
        <h2 class="mt-6 font-heading text-2xl font-bold">Your cart is currently empty</h2>
        <p class="mt-2 text-sm text-[var(--text-muted)] max-w-md mx-auto">
          Before you proceed to checkout, you must add some luxury perfumes to your shopping cart.
        </p>
        <a
          href="/shop"
          class="mt-8 inline-flex items-center gap-2 rounded-xl bg-burgundy-700 px-8 py-3 text-sm font-semibold text-white transition-colors hover:bg-burgundy-800"
        >
          <ArrowLeft class="h-4 w-4" />
          Continue Shopping
        </a>
      </div>
    {:else}
      <div class="grid gap-8 lg:grid-cols-[1fr_360px]">
        <!-- Cart Items List -->
        <div class="space-y-4">
          <div class="card-premium divide-y divide-gray-100 dark:divide-gray-800 overflow-hidden">
            {#each cart.items as item}
              <div class="p-6 flex flex-col sm:flex-row gap-6 items-start sm:items-center">
                <!-- Image -->
                <div class="h-24 w-24 shrink-0 overflow-hidden rounded-xl bg-gray-50 border border-gray-100 dark:bg-gray-900 dark:border-gray-800">
                  <img src={item.product_image} alt={item.product_name} class="h-full w-full object-cover" />
                </div>

                <!-- Info -->
                <div class="flex-1 space-y-1">
                  <p class="text-xs font-semibold uppercase tracking-wider text-gold-600">{item.brand}</p>
                  <a
                    href="/product/{item.product_slug}"
                    class="font-heading text-lg font-bold hover:text-burgundy-700 dark:hover:text-gold-400 block transition-colors"
                  >
                    {item.product_name}
                  </a>
                  {#if item.size}
                    <span class="inline-flex items-center rounded-md bg-gray-100 px-2.5 py-0.5 text-xs font-semibold text-gray-800 dark:bg-gray-800 dark:text-gray-200 uppercase tracking-wider">
                      Size: {item.size}
                    </span>
                  {/if}
                </div>

                <!-- Price and quantity controls -->
                <div class="flex items-center justify-between sm:justify-end gap-6 w-full sm:w-auto">
                  <!-- Quantity controls -->
                  <div class="flex h-9 items-center rounded-lg border border-gray-200 dark:border-gray-800">
                    <button
                      onclick={() => cart.updateQuantity(item.product_id, item.size, item.quantity - 1)}
                      class="flex h-full w-9 items-center justify-center transition-colors hover:bg-gray-100 dark:hover:bg-gray-900"
                      aria-label="Decrease quantity"
                    >
                      <Minus class="h-3.5 w-3.5" />
                    </button>
                    <span class="w-10 text-center text-sm font-semibold">{item.quantity}</span>
                    <button
                      onclick={() => cart.updateQuantity(item.product_id, item.size, item.quantity + 1)}
                      disabled={item.quantity >= item.max_stock}
                      class="flex h-full w-9 items-center justify-center transition-colors hover:bg-gray-100 disabled:opacity-40 dark:hover:bg-gray-900"
                      aria-label="Increase quantity"
                    >
                      <Plus class="h-3.5 w-3.5" />
                    </button>
                  </div>

                  <!-- Unit Price / Total -->
                  <div class="text-right">
                    <span class="block font-heading font-bold text-lg text-burgundy-700 dark:text-gold-400">
                      {formatPrice(item.unit_price * item.quantity)}
                    </span>
                    <span class="text-[10px] text-[var(--text-muted)]">
                      {formatPrice(item.unit_price)} each
                    </span>
                  </div>

                  <!-- Delete -->
                  <button
                    onclick={() => cart.removeItem(item.product_id, item.size)}
                    class="flex h-10 w-10 items-center justify-center rounded-xl text-gray-400 hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-950/20 transition-all"
                    aria-label="Delete item"
                  >
                    <Trash2 class="h-5 w-5" />
                  </button>
                </div>
              </div>
            {/each}
          </div>

          <!-- Actions -->
          <div class="flex justify-between items-center">
            <a
              href="/shop"
              class="inline-flex items-center gap-2 text-sm font-bold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 hover:underline"
            >
              <ArrowLeft class="h-4 w-4" />
              Continue Shopping
            </a>

            <button
              onclick={() => cart.clearCart()}
              class="text-sm font-semibold text-red-650 hover:text-red-750 underline"
            >
              Clear Shopping Cart
            </button>
          </div>
        </div>

        <!-- Order Summary Sidebar -->
        <div class="space-y-6">
          <div class="card-premium p-6 space-y-4">
            <h3 class="font-heading text-xl font-bold">Order Summary</h3>
            <hr class="border-gray-100 dark:border-gray-800" />

            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Subtotal</span>
                <span class="font-semibold">{formatPrice(cart.subtotal)}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Shipping</span>
                <span class="font-semibold">
                  {#if cart.shippingCost === 0}
                    <span class="text-green-600">Free</span>
                  {:else}
                    {formatPrice(cart.shippingCost)}
                  {/if}
                </span>
              </div>
            </div>

            <Separator />

            <div class="flex justify-between">
              <span class="font-heading font-bold text-base">Grand Total</span>
              <span class="font-heading font-bold text-lg text-burgundy-700 dark:text-gold-400">
                {formatPrice(cart.total)}
              </span>
            </div>

            {#if cart.shippingCost > 0}
              <p class="text-[11px] text-[var(--text-muted)] text-center leading-relaxed">
                Add {formatPrice(5000 - cart.subtotal)} more to qualify for FREE Shipping.
              </p>
            {/if}

            <a
              href="/checkout"
              class="btn-press w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3.5 rounded-xl flex items-center justify-center gap-2 mt-4"
            >
              Proceed to Checkout
              <ArrowRight class="h-4 w-4" />
            </a>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
