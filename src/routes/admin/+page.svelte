<script lang="ts">
  import { ShoppingBag, TrendingUp, AlertTriangle, CheckCircle, Clock, FileSpreadsheet, ShieldAlert } from '@lucide/svelte';
  import { formatPrice, formatDate, getStatusColor } from '$lib/utils';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  let stats = $derived(data.stats);
  let recentOrders = $derived(data.recentOrders);
  let lowStockProducts = $derived(data.lowStockProducts);
  let cancelledOrders = $derived(data.cancelledOrders || []);
  let weeklySales = $derived(data.weeklySales || []);

  // Compute maximum amount to scale chart bar heights proportionally
  let maxAmount = $derived(
    Math.max(...weeklySales.map((w: any) => w.amount), 1000)
  );
</script>

<svelte:head>
  <title>Admin Dashboard — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-8">
  <div>
    <h1 class="font-heading text-3xl font-bold">Atelier Overview</h1>
    <p class="text-sm text-[var(--text-muted)]">Real-time status updates of your decant operations.</p>
  </div>

  <!-- Cancelled Orders Alerts -->
  {#if cancelledOrders.length > 0}
    <div class="space-y-2.5">
      {#each cancelledOrders as ord}
        <div class="flex items-center justify-between rounded-xl bg-red-50 border border-red-200/50 p-4 dark:bg-red-950/15 dark:border-red-900/30 text-red-800 dark:text-red-300 animate-scale-in">
          <div class="flex items-center gap-2.5 min-w-0">
            <ShieldAlert class="h-5 w-5 text-red-650 dark:text-red-400 shrink-0" />
            <span class="text-xs font-semibold truncate">
              Order <strong class="font-bold font-mono">{ord.order_number}</strong> was cancelled by customer on {ord.cancelled_at ? new Date(ord.cancelled_at).toLocaleString() : 'N/A'}
            </span>
          </div>
          <a
            href="/admin/orders/{ord.id}"
            class="text-xs font-bold underline hover:text-red-950 dark:hover:text-red-100 pl-3 shrink-0"
          >
            Manage Order
          </a>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Key Statistics Grid -->
  <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-5">
    <!-- Stat 1: Lifetime Revenue -->
    <div class="card-premium p-6 space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Lifetime Revenue</span>
        <TrendingUp class="h-4.5 w-4.5 text-green-500" />
      </div>
      <div>
        <h3 class="font-heading text-2xl font-bold text-gray-900 dark:text-white">{formatPrice(stats.revenue)}</h3>
        <p class="text-[10px] text-green-600 mt-1 font-semibold">Completed orders only</p>
      </div>
    </div>

    <!-- Stat 2: Monthly Revenue -->
    <div class="card-premium p-6 space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Monthly Revenue</span>
        <TrendingUp class="h-4.5 w-4.5 text-green-500" />
      </div>
      <div>
        <h3 class="font-heading text-2xl font-bold text-gray-900 dark:text-white">{formatPrice(stats.monthlyRevenue)}</h3>
        <p class="text-[10px] text-green-600 mt-1 font-semibold">This month (completed)</p>
      </div>
    </div>

    <!-- Stat 3: Daily Revenue -->
    <div class="card-premium p-6 space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Daily Revenue</span>
        <TrendingUp class="h-4.5 w-4.5 text-green-500" />
      </div>
      <div>
        <h3 class="font-heading text-2xl font-bold text-gray-900 dark:text-white">{formatPrice(stats.dailyRevenue)}</h3>
        <p class="text-[10px] text-green-600 mt-1 font-semibold">Today (completed)</p>
      </div>
    </div>

    <!-- Stat 2: Total Orders -->
    <div class="card-premium p-6 space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Total Orders</span>
        <FileSpreadsheet class="h-4.5 w-4.5 text-burgundy-600 dark:text-gold-400" />
      </div>
      <div>
        <h3 class="font-heading text-2xl font-bold text-gray-900 dark:text-white">{stats.totalOrders}</h3>
        <p class="text-[10px] text-[var(--text-muted)] mt-1">Lifetime total orders</p>
      </div>
    </div>

    <!-- Stat 4: Completed Orders -->
    <div class="card-premium p-6 space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Completed</span>
        <CheckCircle class="h-4.5 w-4.5 text-green-500" />
      </div>
      <div>
        <h3 class="font-heading text-2xl font-bold text-gray-900 dark:text-white">{stats.completedOrders}</h3>
        <p class="text-[10px] text-[var(--text-muted)] mt-1">Flipped orders delivered</p>
      </div>
    </div>

    <!-- Stat 5: Pending Orders -->
    <div class="card-premium p-6 space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Pending</span>
        <Clock class="h-4.5 w-4.5 text-yellow-500" />
      </div>
      <div>
        <h3 class="font-heading text-2xl font-bold text-gray-900 dark:text-white">{stats.pendingOrders}</h3>
        <p class="text-[10px] text-[var(--text-muted)] mt-1">Waiting for fulfillment</p>
      </div>
    </div>

    <!-- Stat 5: Total Products -->
    <div class="card-premium p-6 space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Products</span>
        <ShoppingBag class="h-4.5 w-4.5 text-purple-500" />
      </div>
      <div>
        <h3 class="font-heading text-2xl font-bold text-gray-900 dark:text-white">{stats.totalProducts}</h3>
        <p class="text-[10px] text-[var(--text-muted)] mt-1">Available active or drafts</p>
      </div>
    </div>
  </div>

  <div class="grid gap-8 lg:grid-cols-3">
    <!-- Chart Column (Real Completed Sales Last 30 Days) -->
    <div class="lg:col-span-2 space-y-4">
      <h3 class="font-heading text-xl font-bold">Sales Chart (Last 30 Days)</h3>
      <div class="card-premium p-6 flex flex-col justify-between min-h-[300px]">
        <div class="flex-1 flex items-end gap-6 pt-8">
          {#each weeklySales as sale}
            <div class="flex-1 flex flex-col items-center gap-2">
              <span class="text-xs font-semibold text-burgundy-700 dark:text-gold-450">{formatPrice(sale.amount)}</span>
              <div
                class="w-full bg-gradient-to-t from-burgundy-900 to-gold-500 rounded-t-lg transition-all duration-500 hover:opacity-90"
                style="height: {Math.max(10, (sale.amount / maxAmount) * 150)}px"
              ></div>
              <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">{sale.day}</span>
            </div>
          {/each}
        </div>
        <p class="text-center text-xs text-[var(--text-muted)] pt-6 font-semibold">Real weekly sales performance (completed orders only)</p>
      </div>
    </div>

    <!-- Alerts Column (Low Stock Products) -->
    <div class="space-y-4">
      <h3 class="font-heading text-xl font-bold text-red-650 dark:text-red-400 flex items-center gap-2">
        <AlertTriangle class="h-5 w-5 shrink-0" />
        Low Stock Alerts
      </h3>
      <div class="card-premium p-6 space-y-4">
        {#if lowStockProducts.length === 0}
          <p class="text-xs text-[var(--text-muted)] text-center py-8">All items have sufficient stock quantities.</p>
        {:else}
          <div class="space-y-3">
            {#each lowStockProducts as prod}
              <div class="flex justify-between items-center text-xs bg-red-50/40 p-2.5 rounded-lg border border-red-100 dark:bg-red-950/15 dark:border-red-900/30">
                <div class="min-w-0 pr-2">
                  <h4 class="font-bold truncate text-gray-900 dark:text-white">{prod.name}</h4>
                  <span class="text-[10px] text-gray-500 uppercase">{prod.brand}</span>
                </div>
                <span class="rounded-full bg-red-600 px-2 py-0.5 font-bold text-white text-[10px] shrink-0">
                  {prod.stock_quantity} left
                </span>
              </div>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  </div>

  <!-- Recent Orders Table -->
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="font-heading text-xl font-bold">Recent Orders</h3>
      <a href="/admin/orders" class="text-xs font-bold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline">
        View All Orders
      </a>
    </div>

    <div class="card-premium overflow-hidden">
      {#if recentOrders.length === 0}
        <p class="text-xs text-[var(--text-muted)] text-center py-10">No orders placed recently.</p>
      {:else}
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-100 dark:bg-gray-900 dark:border-gray-800 font-bold uppercase tracking-wider text-[var(--text-secondary)]">
                <th class="p-4">Order Code</th>
                <th class="p-4">Date</th>
                <th class="p-4">Payment</th>
                <th class="p-4">Status</th>
                <th class="p-4 text-right">Grand Total</th>
                <th class="p-4 text-center">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
              {#each recentOrders as order}
                <tr class="hover:bg-gray-50/50 dark:hover:bg-gray-900/50 transition-colors">
                  <td class="p-4 font-mono font-bold text-gray-900 dark:text-white">{order.order_number}</td>
                  <td class="p-4">{formatDate(order.created_at)}</td>
                  <td class="p-4 capitalize">{order.payment_method.replace('_', ' ')}</td>
                  <td class="p-4">
                    <span class="inline-flex items-center rounded-full px-2 py-0.5 font-medium capitalize {getStatusColor(order.status)}">
                      {order.status}
                    </span>
                  </td>
                  <td class="p-4 text-right font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(order.total)}</td>
                  <td class="p-4 text-center">
                    <a
                      href="/admin/orders/{order.id}"
                      class="font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline"
                    >
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
  </div>
</div>
