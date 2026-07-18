<script lang="ts">
  import { FileSpreadsheet, Eye, Search } from '@lucide/svelte';
  import { formatPrice, formatDate, getStatusColor } from '$lib/utils';
  import { Input } from '$lib/components/ui/input';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  let orders = $derived(data.orders);
  let searchQuery = $state('');

  // Filter orders by search query (order number, name, phone, email, status)
  const filteredOrders = $derived(
    orders.filter((order: any) => {
      const query = searchQuery.toLowerCase();
      if (!query) return true;
      const orderNum = order.order_number.toLowerCase();
      const customerName = (order.profiles?.full_name || '').toLowerCase();
      const profilePhone = (order.profiles?.phone || '').toLowerCase();
      const status = order.status.toLowerCase();
      const addr = order.shipping_address as any;
      const addrName = (addr?.full_name || '').toLowerCase();
      const addrPhone = (addr?.phone || '').toLowerCase();
      const addrEmail = (addr?.email || '').toLowerCase();

      return (
        orderNum.includes(query) ||
        customerName.includes(query) ||
        profilePhone.includes(query) ||
        status.includes(query) ||
        addrName.includes(query) ||
        addrPhone.includes(query) ||
        addrEmail.includes(query)
      );
    })
  );
</script>

<svelte:head>
  <title>Manage Orders</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <div>
      <h1 class="font-heading text-2xl font-bold">Order Management</h1>
      <p class="text-xs text-[var(--text-muted)]">Track customer orders, confirm payments, and update shipping logs.</p>
    </div>
    
    <div class="relative w-full sm:w-80">
      <Input
        type="search"
        placeholder="Search order, name, phone, email..."
        bind:value={searchQuery}
        class="pl-10 pr-4"
      />
      <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
    </div>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <div class="card-premium overflow-hidden">
    {#if filteredOrders.length === 0}
      <div class="flex min-h-[250px] flex-col items-center justify-center p-8 text-center">
        <FileSpreadsheet class="h-10 w-10 text-gray-400" />
        <h3 class="mt-4 text-base font-semibold">No Orders Found</h3>
        <p class="text-xs text-[var(--text-muted)] mt-1">
          {searchQuery ? 'Adjust your search query.' : 'Customer orders will show up here.'}
        </p>
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100 dark:bg-gray-900 dark:border-gray-800 font-bold uppercase tracking-wider text-[var(--text-secondary)]">
              <th class="p-4">Order Code</th>
              <th class="p-4">Customer Details</th>
              <th class="p-4">Date</th>
              <th class="p-4">Payment</th>
              <th class="p-4">Status</th>
              <th class="p-4 text-right">Total Price</th>
              <th class="p-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            {#each filteredOrders as order}
              {@const addr = order.shipping_address as any}
              <tr class="hover:bg-gray-50/50 dark:hover:bg-gray-900/50 transition-colors">
                <td class="p-4 font-mono font-bold text-gray-900 dark:text-white text-sm">{order.order_number}</td>
                <td class="p-4">
                  <div class="font-bold text-gray-800 dark:text-gray-200">
                    {addr?.full_name || order.profiles?.full_name || 'Guest'}
                  </div>
                  <div class="text-[10px] text-gray-500">{addr?.phone || order.profiles?.phone || ''}</div>
                </td>
                <td class="p-4">{formatDate(order.created_at)}</td>
                <td class="p-4 capitalize">{order.payment_method.replace('_', ' ')}</td>
                <td class="p-4">
                  <span class="inline-flex items-center rounded-full px-2.5 py-0.5 font-medium capitalize {getStatusColor(order.status)}">
                    {order.status}
                  </span>
                </td>
                <td class="p-4 text-right font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(order.total)}</td>
                <td class="p-4 text-center">
                  <a
                    href="/admin/orders/{order.id}"
                    class="inline-flex items-center gap-1 font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline"
                  >
                    <Eye class="h-3.5 w-3.5" />
                    Fulfill
                  </a>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>
