<script lang="ts">
  import { ArrowLeft, MapPin, CreditCard, Clipboard, Calendar } from '@lucide/svelte';
  import { formatPrice, formatDate, getStatusColor } from '$lib/utils';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  let order = $derived(data.order);
  let items = $derived(data.items);
  
  // Parse address snapshot
  const addr = $derived(order.shipping_address as any);
</script>

<svelte:head>
  <title>Order Detail {order.order_number} — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex items-center gap-3">
    <a
      href="/account/orders"
      class="flex h-8 w-8 items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
      aria-label="Back to order history"
    >
      <ArrowLeft class="h-4 w-4" />
    </a>
    <div>
      <h2 class="font-heading text-2xl font-bold">Order Details</h2>
      <p class="text-xs text-[var(--text-muted)] font-mono">ID: {order.order_number}</p>
    </div>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <!-- Summary Info Cards -->
  <div class="grid gap-6 md:grid-cols-3">
    <!-- Status -->
    <div class="card-premium p-4 flex gap-3 items-start">
      <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
        <Calendar class="h-5 w-5" />
      </div>
      <div>
        <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Order Status</h4>
        <span class="inline-flex mt-1 items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize {getStatusColor(order.status)}">
          {order.status}
        </span>
        <p class="text-[10px] text-[var(--text-muted)] mt-1">Placed: {formatDate(order.created_at)}</p>
      </div>
    </div>

    <!-- Address -->
    <div class="card-premium p-4 flex gap-3 items-start">
      <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
        <MapPin class="h-5 w-5" />
      </div>
      <div>
        <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Shipping Address</h4>
        <p class="text-xs font-bold text-gray-900 dark:text-white mt-1">{addr?.full_name}</p>
        <p class="text-[11px] text-[var(--text-secondary)] leading-tight mt-0.5">
          {addr?.address_line_1}
          {#if addr?.address_line_2}
            , {addr.address_line_2}
          {/if}
          <br />{addr?.city} - {addr?.postal_code}
          <br />Phone: {addr?.phone}
        </p>
      </div>
    </div>

    <!-- Payment -->
    <div class="card-premium p-4 flex gap-3 items-start">
      <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
        <CreditCard class="h-5 w-5" />
      </div>
      <div>
        <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Payment Details</h4>
        <p class="text-xs font-bold capitalize mt-1">
          {order.payment_method.replace('_', ' ')}
        </p>
        <p class="text-[10px] text-[var(--text-muted)] mt-1">Manual bank transfer or Cash on Delivery</p>
      </div>
    </div>
  </div>

  <!-- Ordered Items Table -->
  <div class="space-y-4">
    <h3 class="font-heading text-lg font-bold">Items Purchased</h3>
    <div class="overflow-hidden rounded-xl border border-gray-100 dark:border-gray-800">
      <table class="w-full text-left border-collapse text-sm">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100 dark:bg-gray-900 dark:border-gray-800 text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">
            <th class="p-4">Perfume Details</th>
            <th class="p-4">Size</th>
            <th class="p-4 text-center">Qty</th>
            <th class="p-4 text-right">Price</th>
            <th class="p-4 text-right">Total</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          {#each items as item}
            <tr>
              <td class="p-4 flex items-center gap-3">
                <div class="h-12 w-12 shrink-0 overflow-hidden rounded-lg bg-gray-100 dark:bg-gray-900">
                  <img src={item.product_image} alt="" class="h-full w-full object-cover" />
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900 dark:text-white leading-tight">{item.product_name}</h4>
                </div>
              </td>
              <td class="p-4 text-xs font-semibold">{item.size || 'Default'}</td>
              <td class="p-4 text-center">{item.quantity}</td>
              <td class="p-4 text-right font-medium">{formatPrice(item.unit_price)}</td>
              <td class="p-4 text-right font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(item.total_price)}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Order Notes -->
  {#if order.notes}
    <div class="card-premium p-4 space-y-2">
      <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">
        <Clipboard class="h-4 w-4 text-gold-500" />
        Customer Notes
      </div>
      <p class="text-xs text-[var(--text-secondary)] leading-relaxed italic">"{order.notes}"</p>
    </div>
  {/if}

  <!-- Pricing summary alignment -->
  <div class="flex justify-end pt-4">
    <div class="w-full max-w-xs space-y-2.5">
      <div class="flex justify-between text-sm">
        <span class="text-gray-500">Subtotal</span>
        <span class="font-semibold">{formatPrice(order.subtotal)}</span>
      </div>
      <div class="flex justify-between text-sm">
        <span class="text-gray-500">Shipping Cost</span>
        <span class="font-semibold">{formatPrice(order.shipping_cost)}</span>
      </div>
      <hr class="border-gray-200 dark:border-gray-850" />
      <div class="flex justify-between">
        <span class="font-heading font-bold text-base">Grand Total</span>
        <span class="font-heading font-bold text-lg text-burgundy-700 dark:text-gold-400">
          {formatPrice(order.total)}
        </span>
      </div>
    </div>
  </div>
</div>
