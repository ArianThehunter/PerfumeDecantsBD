<script lang="ts">
  import { enhance } from '$app/forms';
  import { ArrowLeft, User, Phone, Mail, MapPin, CreditCard, Clipboard, Calendar } from '@lucide/svelte';
  import { formatPrice, formatDate, getStatusColor } from '$lib/utils';
  import { Button } from '$lib/components/ui/button';
  import { toast } from 'svelte-sonner';
  import type { PageData, ActionData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let order = $derived(data.order);
  let items = $derived(data.items);
  let addr = $derived(order.shipping_address as any);
  
  let loading = $state(false);

  $effect(() => {
    if (form?.success) {
      toast.success('Order status updated successfully');
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<svelte:head>
  <title>Fulfill Order {order.order_number} — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex items-center gap-3">
    <a
      href="/admin/orders"
      class="flex h-8 w-8 items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
      aria-label="Back to order history"
    >
      <ArrowLeft class="h-4 w-4" />
    </a>
    <div>
      <h1 class="font-heading text-2xl font-bold">Fulfill Order</h1>
      <p class="text-xs text-[var(--text-muted)] font-mono">Code: {order.order_number}</p>
    </div>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <!-- Split Info: Status Modifier & Summary Details -->
  <div class="grid gap-6 md:grid-cols-3">
    <!-- Status Control -->
    <div class="card-premium p-6 space-y-4">
      <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">
        <Calendar class="h-4 w-4 text-gold-500" />
        Order Fulfill status
      </div>

      <form
        method="post"
        action="?/updateStatus"
        use:enhance={() => {
          loading = true;
          return async ({ update }) => {
            loading = false;
            await update();
          };
        }}
        class="space-y-3"
      >
        <select
          name="status"
          value={order.status}
          class="flex h-10 w-full items-center justify-between rounded-md border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3 py-2 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-burgundy-500/20 dark:focus:ring-gold-500/20"
        >
          <option value="pending">Pending</option>
          <option value="confirmed">Confirmed</option>
          <option value="processing">Processing</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>

        <Button
          type="submit"
          disabled={loading}
          class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold rounded-xl text-xs py-2"
        >
          {loading ? 'Updating...' : 'Update Status'}
        </Button>
      </form>

      {#if order.status === 'cancelled'}
        <div class="mt-3 text-xs font-semibold text-red-650 dark:text-red-400 bg-red-50/50 dark:bg-red-950/10 border border-red-200/50 dark:border-red-900/30 rounded-lg p-2.5 text-center">
          Cancelled: {order.cancelled_at ? new Date(order.cancelled_at).toLocaleString() : 'Time not recorded'}
        </div>
      {/if}
    </div>

    <!-- Customer -->
    <div class="card-premium p-6 space-y-3">
      <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">
        <User class="h-4 w-4 text-gold-500" />
        Customer Contact
      </div>
      <div class="space-y-1.5 text-xs">
        <p class="font-bold text-gray-900 dark:text-white">{addr?.full_name || 'Guest'}</p>
        <p class="flex items-center gap-1.5 text-[var(--text-secondary)]">
          <Mail class="h-3.5 w-3.5 text-gray-400" />
          {addr?.email || 'N/A'}
        </p>
        <p class="flex items-center gap-1.5 text-[var(--text-secondary)]">
          <Phone class="h-3.5 w-3.5 text-gray-400" />
          {addr?.phone || 'N/A'}
        </p>
      </div>
    </div>

    <!-- Shipping Destination -->
    <div class="card-premium p-6 space-y-3">
      <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">
        <MapPin class="h-4 w-4 text-gold-500" />
        Shipping Destination
      </div>
      <p class="text-xs text-[var(--text-secondary)] leading-relaxed">
        {addr?.address_line_1}
        {#if addr?.address_line_2}
          , {addr.address_line_2}
        {/if}
        <br />{addr?.city} - {addr?.postal_code}
      </p>
    </div>
  </div>

  <!-- Ordered Items -->
  <div class="space-y-4">
    <h3 class="font-heading text-lg font-bold">Items to Pack</h3>
    <div class="overflow-hidden rounded-xl border border-gray-100 dark:border-gray-800">
      <table class="w-full text-left border-collapse text-sm">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100 dark:bg-gray-900 dark:border-gray-800 text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">
            <th class="p-4">Item Details</th>
            <th class="p-4">Size</th>
            <th class="p-4 text-center">Fulfill Qty</th>
            <th class="p-4 text-right">Unit Price</th>
            <th class="p-4 text-right">Total Price</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          {#each items as item}
            <tr>
              <td class="p-4 flex items-center gap-3">
                <div class="h-12 w-12 shrink-0 overflow-hidden rounded-lg bg-gray-55 border border-gray-100 dark:bg-gray-900 dark:border-gray-850">
                  <img src={item.product_image} alt="" class="h-full w-full object-cover" />
                </div>
                <h4 class="font-semibold text-gray-900 dark:text-white leading-tight">{item.product_name}</h4>
              </td>
              <td class="p-4 text-xs font-bold uppercase tracking-wider">{item.size || 'Default'}</td>
              <td class="p-4 text-center font-bold text-base text-burgundy-900 dark:text-gold-450">{item.quantity}</td>
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

  <!-- Pricing Details alignment -->
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
