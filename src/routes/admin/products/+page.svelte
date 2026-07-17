<script lang="ts">
  import { enhance } from '$app/forms';
  import { Plus, Edit3, Trash2, ShoppingBag, Star, Search } from '@lucide/svelte';
  import { formatPrice } from '$lib/utils';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { toast } from 'svelte-sonner';
  import type { PageData, ActionData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let products = $derived(data.products);
  let searchQuery = $state('');
  let loading = $state(false);

  const filteredProducts = $derived(
    products.filter((prod: any) => {
      const query = searchQuery.toLowerCase();
      return (
        prod.name.toLowerCase().includes(query) ||
        prod.brand.toLowerCase().includes(query) ||
        prod.status.toLowerCase().includes(query)
      );
    })
  );

  $effect(() => {
    if (form?.success) {
      toast.success('Product deleted successfully');
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<svelte:head>
  <title>Manage Products — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <div>
      <h1 class="font-heading text-2xl font-bold">Product Management</h1>
      <p class="text-xs text-[var(--text-muted)]">Configure perfume brands, stock counts, decant sizes, and images.</p>
    </div>

    <div class="flex items-center gap-3">
      <div class="relative w-full sm:w-64">
        <Input
          type="search"
          placeholder="Search name, brand..."
          bind:value={searchQuery}
          class="pl-10 pr-4"
        />
        <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
      </div>
      <a
        href="/admin/products/new"
        class="bg-burgundy-700 hover:bg-burgundy-800 text-white flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-semibold shrink-0"
      >
        <Plus class="h-4 w-4" />
        New Product
      </a>
    </div>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <div class="card-premium overflow-hidden">
    {#if filteredProducts.length === 0}
      <div class="flex min-h-[250px] flex-col items-center justify-center p-8 text-center">
        <ShoppingBag class="h-10 w-10 text-gray-400" />
        <h3 class="mt-4 text-base font-semibold">No Products Found</h3>
        <p class="text-xs text-[var(--text-muted)] mt-1">
          {searchQuery ? 'Adjust your search query.' : 'Click "New Product" to add a perfume decant.'}
        </p>
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100 dark:bg-gray-900 dark:border-gray-800 font-bold uppercase tracking-wider text-[var(--text-secondary)]">
              <th class="p-4">Image</th>
              <th class="p-4">Product Details</th>
              <th class="p-4">Brand</th>
              <th class="p-4 text-right">Base Price</th>
              <th class="p-4 text-center">Stock</th>
              <th class="p-4 text-center">Status</th>
              <th class="p-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            {#each filteredProducts as prod}
              {@const imgUrl = prod.product_images?.find((img: any) => img.is_primary)?.url 
                || prod.product_images?.[0]?.url 
                || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'}
              <tr class="hover:bg-gray-50/50 dark:hover:bg-gray-900/50 transition-colors">
                <td class="p-4">
                  <div class="h-12 w-12 overflow-hidden rounded-lg bg-gray-50 border dark:bg-gray-900 dark:border-gray-850">
                    <img src={imgUrl} alt="" class="h-full w-full object-cover" />
                  </div>
                </td>
                <td class="p-4">
                  <div class="font-bold text-gray-900 dark:text-white text-sm flex items-center gap-1.5">
                    {prod.name}
                    {#if prod.is_featured}
                      <span class="rounded-full bg-gold-100 text-gold-800 px-1.5 py-0.5 text-[9px] font-semibold dark:bg-gold-950 dark:text-gold-400">
                        Featured
                      </span>
                    {/if}
                  </div>
                  <div class="text-[10px] text-gray-500 capitalize">{prod.gender} • {prod.slug}</div>
                </td>
                <td class="p-4 uppercase font-semibold">{prod.brand}</td>
                <td class="p-4 text-right font-bold text-burgundy-700 dark:text-gold-400">
                  {#if prod.discount_price}
                    <span>{formatPrice(prod.discount_price)}</span>
                    <span class="text-[10px] text-gray-400 line-through block">{formatPrice(prod.price)}</span>
                  {:else}
                    <span>{formatPrice(prod.price)}</span>
                  {/if}
                </td>
                <td class="p-4 text-center">
                  <span class="font-bold {prod.stock_quantity <= 5 ? 'text-red-500' : 'text-gray-700 dark:text-gray-300'}">
                    {prod.stock_quantity}
                  </span>
                </td>
                <td class="p-4 text-center">
                  <span class="inline-flex rounded-full px-2 py-0.5 font-bold uppercase tracking-wider text-[10px] {prod.status === 'active' 
                    ? 'bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-400' 
                    : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-950 dark:text-yellow-400'}">
                    {prod.status}
                  </span>
                </td>
                <td class="p-4">
                  <div class="flex items-center justify-center gap-2">
                    <a
                      href="/admin/products/{prod.id}"
                      class="flex h-8 w-8 items-center justify-center rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800"
                      aria-label="Edit product"
                    >
                      <Edit3 class="h-4 w-4" />
                    </a>
                    <form
                      method="post"
                      action="?/deleteProduct"
                      use:enhance={() => {
                        loading = true;
                        return async ({ update }) => {
                          loading = false;
                          await update();
                        };
                      }}
                    >
                      <input type="hidden" name="id" value={prod.id} />
                      <button
                        type="submit"
                        disabled={loading}
                        class="flex h-8 w-8 items-center justify-center rounded-lg text-gray-400 hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-950/20"
                        aria-label="Delete product"
                      >
                        <Trash2 class="h-4 w-4" />
                      </button>
                    </form>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>
