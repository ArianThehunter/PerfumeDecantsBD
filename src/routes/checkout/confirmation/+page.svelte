<script lang="ts">
  import { CheckCircle, Calendar, CreditCard, ShoppingBag, ArrowRight } from '@lucide/svelte';
  import { formatPrice } from '$lib/utils/formatters';
  import { cart } from '$lib/stores/cart.svelte';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  let order = $derived(data.order);

  $effect(() => {
    cart.clearCart();
  });
</script>

<svelte:head>
  <title>Order Confirmed</title>
</svelte:head>

<div class="flex min-h-[80vh] items-center justify-center bg-[var(--bg-secondary)] px-4 py-12">
  <div class="w-full max-w-lg space-y-8 rounded-2xl bg-white p-8 shadow-xl dark:bg-gray-950 border border-gray-100 dark:border-gray-900 text-center">
    <div class="space-y-4">
      <CheckCircle class="mx-auto h-16 w-16 text-green-500 animate-scale-in" />
      <h1 class="font-heading text-3xl font-bold tracking-tight text-burgundy-950 dark:text-cream-200">
        Thank you for your order!
      </h1>
      <p class="text-sm text-[var(--text-secondary)] leading-relaxed max-w-md mx-auto">
        Your order has been placed successfully. A confirmation email/message will be sent shortly containing packaging details.
      </p>
    </div>

    <!-- Order summary details card -->
    <div class="card-premium p-6 text-left space-y-3 bg-gray-50/50 dark:bg-gray-900/50">
      <div class="flex justify-between items-center text-sm border-b pb-3 border-gray-200 dark:border-gray-800">
        <span class="text-gray-500 font-semibold uppercase tracking-wider text-xs">Order Number</span>
        <span class="font-mono font-bold text-gray-900 dark:text-white">{order.order_number}</span>
      </div>

      <div class="flex justify-between items-center text-sm pt-1">
        <span class="text-gray-500 flex items-center gap-1.5">
          <Calendar class="h-4 w-4" />
          Order Date
        </span>
        <span class="font-medium">{new Date(order.created_at).toLocaleDateString()}</span>
      </div>

      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-500 flex items-center gap-1.5">
          <CreditCard class="h-4 w-4" />
          Payment Method
        </span>
        <span class="font-medium capitalize">{order.payment_method.replace('_', ' ')}</span>
      </div>

      <div class="flex justify-between items-center text-sm border-t pt-3 border-gray-200 dark:border-gray-800">
        <span class="font-heading font-bold text-base">Grand Total</span>
        <span class="font-heading font-bold text-lg text-burgundy-700 dark:text-gold-400">{formatPrice(order.total)}</span>
      </div>
    </div>

    {#if !data.isAuthenticated}
      <!-- Account creation encouragement -->
      <div class="mt-6 rounded-xl border border-dashed border-gray-250 bg-gray-50/50 p-5 dark:border-gray-800 dark:bg-gray-900/30 text-xs text-[var(--text-secondary)] space-y-2 max-w-md mx-auto">
        <p class="font-bold text-gray-900 dark:text-cream-200">Create an account to track future orders, save your addresses, and enjoy a faster checkout experience.</p>
        <p class="text-[10px] text-[var(--text-muted)]">It's completely optional and takes less than a minute.</p>
        <a href="/auth/register" class="inline-block text-xs font-bold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 hover:underline mt-1">
          Register Account Now &rarr;
        </a>
      </div>
    {/if}

    <div class="flex flex-col sm:flex-row gap-3 justify-center pt-6">
      {#if data.isAuthenticated}
        <a
          href="/account/orders/{order.id}"
          class="btn-press flex items-center justify-center gap-2 rounded-xl border border-gray-200 px-6 py-3 text-sm font-semibold transition-colors hover:bg-gray-50 dark:border-gray-800 dark:hover:bg-gray-900"
        >
          <ShoppingBag class="h-4 w-4" />
          Track Order
        </a>
      {:else}
        {@const shippingAddress = order.shipping_address as any}
        <a
          href="/track?orderId={order.order_number}&phone={shippingAddress?.phone || ''}"
          class="btn-press flex items-center justify-center gap-2 rounded-xl border border-gray-200 px-6 py-3 text-sm font-semibold transition-colors hover:bg-gray-50 dark:border-gray-800 dark:hover:bg-gray-900"
        >
          <ShoppingBag class="h-4 w-4" />
          View Order Details
        </a>
      {/if}
      <a
        href="/shop"
        class="btn-press flex items-center justify-center gap-2 rounded-xl bg-burgundy-700 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-burgundy-800"
      >
        Continue Shopping
        <ArrowRight class="h-4 w-4" />
      </a>
    </div>
  </div>
</div>
