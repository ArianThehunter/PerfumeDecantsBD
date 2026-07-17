<script lang="ts">
  import { cart } from '$lib/stores/cart.svelte';
  import { formatPrice } from '$lib/utils/formatters';
  import { X, Minus, Plus, ShoppingBag, Trash2, ArrowRight } from '@lucide/svelte';
  import * as Sheet from '$lib/components/ui/sheet';
  import { Button } from '$lib/components/ui/button';
  import { Separator } from '$lib/components/ui/separator';
</script>

<Sheet.Root open={cart.isOpen} onOpenChange={(open) => { if (!open) cart.closeCart(); }}>
  <Sheet.Content side="right" class="w-full max-w-md p-0 sm:max-w-lg [&>button]:hidden bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 border-l border-gray-200 dark:border-gray-800">
    <div class="flex h-full flex-col">
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-gray-100 dark:border-gray-800 px-6 py-4">
        <div class="flex items-center gap-2">
          <ShoppingBag class="h-5 w-5 text-burgundy-700 dark:text-gold-400" />
          <Sheet.Title class="font-heading text-lg font-bold">
            Shopping Cart ({cart.itemCount})
          </Sheet.Title>
        </div>
        <button
          onclick={() => cart.closeCart()}
          class="flex h-8 w-8 items-center justify-center rounded-full transition-colors hover:bg-gray-100 dark:hover:bg-gray-800"
          aria-label="Close cart"
        >
          <X class="h-4 w-4" />
        </button>
      </div>

      <!-- Cart Items -->
      {#if cart.items.length === 0}
        <div class="flex flex-1 flex-col items-center justify-center px-6 text-center">
          <div class="flex h-20 w-20 items-center justify-center rounded-full bg-burgundy-50 dark:bg-burgundy-950">
            <ShoppingBag class="h-10 w-10 text-burgundy-300 dark:text-burgundy-700" />
          </div>
          <h3 class="mt-4 font-heading text-lg font-semibold">Your cart is empty</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Discover our collection of luxury fragrances
          </p>
          <a
            href="/shop"
            onclick={() => cart.closeCart()}
            class="mt-6 inline-flex items-center gap-2 rounded-lg bg-burgundy-700 px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-burgundy-800"
          >
            Browse Shop
            <ArrowRight class="h-4 w-4" />
          </a>
        </div>
      {:else}
        <div class="flex-1 overflow-y-auto px-6 py-4">
          <div class="space-y-4">
            {#each cart.items as item}
              <div class="flex gap-4 rounded-xl bg-gray-50 p-3 dark:bg-gray-900">
                <!-- Image -->
                <div class="h-20 w-20 shrink-0 overflow-hidden rounded-lg bg-gray-200 dark:bg-gray-800">
                  <img
                    src={item.product_image}
                    alt={item.product_name}
                    class="h-full w-full object-cover"
                    loading="lazy"
                  />
                </div>

                <!-- Details -->
                <div class="flex flex-1 flex-col justify-between">
                  <div>
                    <a
                      href="/product/{item.product_slug}"
                      onclick={() => cart.closeCart()}
                      class="text-sm font-semibold leading-tight hover:text-burgundy-700 dark:hover:text-gold-400"
                    >
                      {item.product_name}
                    </a>
                    <p class="mt-0.5 text-xs text-gray-500">{item.brand}{item.size ? ` • ${item.size}` : ''}</p>
                  </div>

                  <div class="flex items-center justify-between">
                    <!-- Quantity Controls -->
                    <div class="flex items-center gap-1">
                      <button
                        onclick={() => cart.updateQuantity(item.product_id, item.size, item.quantity - 1)}
                        class="flex h-7 w-7 items-center justify-center rounded-md border transition-colors hover:bg-gray-200 dark:border-gray-700 dark:hover:bg-gray-800"
                        aria-label="Decrease quantity"
                      >
                        <Minus class="h-3 w-3" />
                      </button>
                      <span class="w-8 text-center text-sm font-medium">{item.quantity}</span>
                      <button
                        onclick={() => cart.updateQuantity(item.product_id, item.size, item.quantity + 1)}
                        disabled={item.quantity >= item.max_stock}
                        class="flex h-7 w-7 items-center justify-center rounded-md border transition-colors hover:bg-gray-200 disabled:opacity-40 dark:border-gray-700 dark:hover:bg-gray-800"
                        aria-label="Increase quantity"
                      >
                        <Plus class="h-3 w-3" />
                      </button>
                    </div>

                    <div class="flex items-center gap-2">
                      <span class="text-sm font-bold text-burgundy-700 dark:text-gold-400">
                        {formatPrice(item.unit_price * item.quantity)}
                      </span>
                      <button
                        onclick={() => cart.removeItem(item.product_id, item.size)}
                        class="flex h-7 w-7 items-center justify-center rounded-md text-gray-400 transition-colors hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-950"
                        aria-label="Remove item"
                      >
                        <Trash2 class="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>

        <!-- Footer / Summary -->
        <div class="border-t border-gray-100 dark:border-gray-800 px-6 py-4">
          <div class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Subtotal</span>
              <span class="font-medium">{formatPrice(cart.subtotal)}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Shipping</span>
              <span class="font-medium">
                {#if cart.shippingCost === 0}
                  <span class="text-green-600">Free</span>
                {:else}
                  {formatPrice(cart.shippingCost)}
                {/if}
              </span>
            </div>
            <Separator />
            <div class="flex justify-between">
              <span class="font-heading text-base font-bold">Total</span>
              <span class="font-heading text-lg font-bold text-burgundy-700 dark:text-gold-400">
                {formatPrice(cart.total)}
              </span>
            </div>
          </div>

          {#if cart.subtotal > 0 && cart.subtotal < 5000}
            <p class="mt-2 text-center text-xs text-gray-500">
              Add {formatPrice(5000 - cart.subtotal)} more for free shipping!
            </p>
          {/if}

          <div class="mt-4 grid gap-2">
            <a
              href="/checkout"
              onclick={() => cart.closeCart()}
              class="btn-press flex items-center justify-center gap-2 rounded-xl bg-burgundy-700 py-3 text-sm font-semibold text-white transition-colors hover:bg-burgundy-800"
            >
              Checkout
              <ArrowRight class="h-4 w-4" />
            </a>
            <a
              href="/cart"
              onclick={() => cart.closeCart()}
              class="flex items-center justify-center rounded-xl border border-gray-200 py-2.5 text-sm font-medium transition-colors hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-900"
            >
              View Full Cart
            </a>
          </div>
        </div>
      {/if}
    </div>
  </Sheet.Content>
</Sheet.Root>
