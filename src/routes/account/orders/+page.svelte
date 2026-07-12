<script lang="ts">
  import { ShoppingBag, ChevronRight, Eye } from '@lucide/svelte';
  import { formatPrice, formatDate, getStatusColor } from '$lib/utils';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  let orders = $derived(data.orders);
</script>

<div class="space-y-6">
  <div>
    <h2 class="font-heading text-2xl font-bold">Order History</h2>
    <p class="text-sm text-[var(--text-muted)]">Track and manage your current and past decant orders.</p>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  {#if orders.length === 0}
    <div class="flex min-h-[300px] flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-200 p-8 text-center dark:border-gray-800">
      <ShoppingBag class="h-10 w-10 text-gray-400" />
      <h3 class="mt-4 text-base font-semibold">No orders yet</h3>
      <p class="mt-1 text-xs text-[var(--text-muted)]">When you buy luxury perfumes, they will show up here.</p>
      <a
        href="/shop"
        class="mt-6 inline-flex items-center gap-2 rounded-xl bg-burgundy-700 px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-burgundy-800"
      >
        Start Shopping
        <ChevronRight class="h-4 w-4" />
      </a>
    </div>
  {:else}
    <div class="overflow-x-auto rounded-xl border border-gray-100 dark:border-gray-850">
      <table class="w-full text-left border-collapse text-sm">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100 dark:bg-gray-900 dark:border-gray-800 text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">
            <th class="p-4">Order Number</th>
            <th class="p-4">Date Purchased</th>
            <th class="p-4">Payment Method</th>
            <th class="p-4">Status</th>
            <th class="p-4 text-right">Total Price</th>
            <th class="p-4 text-center">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          {#each orders as order}
            <tr class="hover:bg-gray-50/50 dark:hover:bg-gray-900/50 transition-colors">
              <td class="p-4 font-mono font-bold text-gray-900 dark:text-white">{order.order_number}</td>
              <td class="p-4 text-xs">{formatDate(order.created_at)}</td>
              <td class="p-4 text-xs capitalize">{order.payment_method.replace('_', ' ')}</td>
              <td class="p-4">
                <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize {getStatusColor(order.status)}">
                  {order.status}
                </span>
              </td>
              <td class="p-4 text-right font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(order.total)}</td>
              <td class="p-4 text-center">
                <a
                  href="/account/orders/{order.id}"
                  class="inline-flex items-center gap-1 text-xs font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 hover:underline"
                >
                  <Eye class="h-3.5 w-3.5" />
                  Details
                </a>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>
