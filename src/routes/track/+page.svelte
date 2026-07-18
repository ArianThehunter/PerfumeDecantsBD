<script lang="ts">
  import { ArrowLeft, MapPin, CreditCard, Clipboard, Calendar, Search, Printer, AlertTriangle } from '@lucide/svelte';
  import { formatPrice, formatDate, getStatusColor } from '$lib/utils';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  let order = $derived(data.order);
  let items = $derived(data.items);
  let error = $derived(data.error);
  let searched = $derived(data.searched);

  // Form bindings
  let orderIdInput = $state('');
  let phoneInput = $state('');

  function handlePrint() {
    if (typeof window !== 'undefined') {
      window.print();
    }
  }
</script>

<svelte:head>
  <title>Track Order</title>
</svelte:head>

<div class="bg-[var(--bg-primary)] py-10 lg:py-16 min-h-[80vh] print:bg-white print:py-0 print:min-h-0">
  <div class="container-luxury max-w-4xl print:px-0">
    <!-- Breadcrumb and title -->
    <div class="mb-8 flex items-center justify-between print:hidden">
      <div class="flex items-center gap-3">
        <a href="/" class="flex h-9 w-9 items-center justify-center rounded-full hover:bg-gray-150 dark:hover:bg-gray-800 transition-colors">
          <ArrowLeft class="h-5 w-5" />
        </a>
        <h1 class="font-heading text-3xl font-bold">Track Your Order</h1>
      </div>
      
      {#if order}
        <Button variant="outline" class="flex items-center gap-2 rounded-xl border-gray-300 dark:border-gray-800" onclick={handlePrint}>
          <Printer class="h-4 w-4" />
          Print / Download
        </Button>
      {/if}
    </div>

    <!-- Search Form (only visible if order is not loaded, or on screen print:hidden) -->
    <div class="print:hidden">
      {#if !order}
        <div class="card-premium p-6 md:p-8 max-w-xl mx-auto space-y-6">
          <div>
            <h2 class="font-heading text-xl font-bold">Find Guest or Account Orders</h2>
            <p class="text-xs text-[var(--text-muted)] mt-1">
              Enter your Order Number (e.g. PDBD-YYYYMMDD-XXXX or the UUID) and the 11-digit phone number associated with the shipping address.
            </p>
          </div>

          {#if error}
            <div class="flex items-start gap-3 rounded-xl bg-red-50 border border-red-200/50 p-4 dark:bg-red-950/15 dark:border-red-900/30 text-red-800 dark:text-red-300">
              <AlertTriangle class="h-5 w-5 shrink-0 text-red-600 dark:text-red-400" />
              <p class="text-xs font-semibold">{error}</p>
            </div>
          {/if}

          <form method="get" action="/track" class="space-y-4">
            <div class="space-y-1">
              <label for="orderId" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Order ID / Number</label>
              <Input
                id="orderId"
                name="orderId"
                type="text"
                placeholder="PDBD-20260718-0001"
                required
                bind:value={orderIdInput}
              />
            </div>

            <div class="space-y-1">
              <label for="phone" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Phone Number</label>
              <Input
                id="phone"
                name="phone"
                type="tel"
                placeholder="01XXXXXXXXX"
                required
                bind:value={phoneInput}
              />
            </div>

            <Button type="submit" class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-bold py-3 mt-4 flex items-center justify-center gap-2">
              <Search class="h-4 w-4" />
              Track Order
            </Button>
          </form>
        </div>
      {/if}
    </div>

    <!-- Order Display -->
    {#if order}
      <div class="space-y-8 mt-2 print:mt-0">
        <!-- Success Banner only shown if they literally just placed it and land here, but also normal header details -->
        <div class="card-premium p-6 space-y-6 bg-white dark:bg-gray-950">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-100 dark:border-gray-800 pb-4">
            <div>
              <span class="text-xs font-bold uppercase tracking-wider text-gold-500">Order Overview</span>
              <h2 class="font-heading text-2xl font-bold mt-1">Order details for {order.order_number}</h2>
              <p class="text-xs text-[var(--text-muted)] font-mono mt-0.5">Order UUID: {order.id}</p>
            </div>
            <div class="flex flex-col items-start md:items-end gap-1.5">
              <span class="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold capitalize {getStatusColor(order.status)}">
                {order.status}
              </span>
              <p class="text-xs text-[var(--text-muted)]">Placed: {formatDate(order.created_at)}</p>
            </div>
          </div>

          <!-- Summary Grid -->
          <div class="grid gap-6 md:grid-cols-3">
            <!-- Shipping Info -->
            <div class="flex gap-3 items-start">
              <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
                <MapPin class="h-4.5 w-4.5" />
              </div>
              <div class="text-xs leading-relaxed text-[var(--text-secondary)]">
                <h4 class="font-bold text-gray-950 dark:text-cream-200">Shipping Destination</h4>
                {#if order.shipping_address}
                  {@const addr = order.shipping_address}
                  <p class="font-semibold text-gray-900 dark:text-white mt-1">{addr.full_name}</p>
                  <p class="mt-0.5">
                    {addr.address_line_1}
                    {#if addr.address_line_2}
                      , {addr.address_line_2}
                    {/if}
                    <br />{addr.city} - {addr.postal_code || ''}
                    <br />Phone: {addr.phone}
                  </p>
                {/if}
              </div>
            </div>

            <!-- Payment Details -->
            <div class="flex gap-3 items-start">
              <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
                <CreditCard class="h-4.5 w-4.5" />
              </div>
              <div class="text-xs leading-relaxed text-[var(--text-secondary)]">
                <h4 class="font-bold text-gray-950 dark:text-cream-200">Payment Details</h4>
                <p class="font-semibold capitalize text-gray-900 dark:text-white mt-1">
                  {order.payment_method.replace('_', ' ')}
                </p>
                <p class="text-[10px] text-[var(--text-muted)] mt-1">Manual bank transfer or Cash on Delivery</p>
              </div>
            </div>

            <!-- Tracking Details / Support -->
            <div class="flex gap-3 items-start print:hidden">
              <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
                <Calendar class="h-4.5 w-4.5" />
              </div>
              <div class="text-xs leading-relaxed text-[var(--text-secondary)]">
                <h4 class="font-bold text-gray-950 dark:text-cream-200">Need Assistance?</h4>
                <p class="mt-1">If you have any questions regarding your delivery details, please contact us at <a href="mailto:readusshalehin22@gmail.com" class="text-burgundy-750 dark:text-gold-400 underline">readusshalehin22@gmail.com</a>.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Items table -->
        <div class="card-premium p-6 space-y-4 bg-white dark:bg-gray-950">
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
                      <div class="h-10 w-10 shrink-0 overflow-hidden rounded-lg bg-gray-150 dark:bg-gray-900">
                        <img src={item.product_image} alt="" class="h-full w-full object-cover" />
                      </div>
                      <span class="font-semibold text-gray-900 dark:text-white leading-tight">{item.product_name}</span>
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

          {#if order.notes}
            <div class="rounded-xl border border-gray-100 dark:border-gray-800 bg-gray-50/50 p-4 dark:bg-gray-900/40 text-xs text-[var(--text-secondary)] leading-relaxed space-y-1.5">
              <span class="font-bold flex items-center gap-1.5 uppercase text-[10px] tracking-wider text-gray-950 dark:text-cream-200">
                <Clipboard class="h-4 w-4" />
                Customer Notes
              </span>
              <p class="italic">"{order.notes}"</p>
            </div>
          {/if}

          <!-- Grand Total alignment -->
          <div class="flex justify-end pt-4">
            <div class="w-full max-w-xs space-y-2.5">
              <div class="flex justify-between text-xs">
                <span class="text-gray-500">Subtotal</span>
                <span class="font-semibold text-gray-900 dark:text-white">{formatPrice(order.subtotal)}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="text-gray-500">Shipping Cost</span>
                <span class="font-semibold text-gray-900 dark:text-white">{formatPrice(order.shipping_cost)}</span>
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

        <div class="text-center print:hidden">
          <a href="/track" class="text-sm font-semibold text-burgundy-750 hover:text-burgundy-850 dark:text-gold-400 underline">
            Track Another Order
          </a>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  @media print {
    :global(header), :global(footer), :global(.print\:hidden) {
      display: none !important;
    }
    :global(main) {
      padding-top: 0 !important;
    }
  }
</style>
