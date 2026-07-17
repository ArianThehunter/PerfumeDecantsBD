<script lang="ts">
  import { enhance } from '$app/forms';
  import { ArrowLeft, Save, Plus } from '@lucide/svelte';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { Textarea } from '$lib/components/ui/textarea';
  import { formatPrice } from '$lib/utils';
  import { toast } from 'svelte-sonner';
  import type { PageData, ActionData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let product = $derived(data.product);
  let categories = $derived(data.categories);
  let loading = $state(false);

  // Helper size states
  let sizeLabel = $state('');
  let sizePrice = $state(0);
  let sizesList = $state<{ label: string; price: number; ml: number }[]>([]);

  // Init size options list from loaded product
  $effect(() => {
    if (product.sizes && Array.isArray(product.sizes)) {
      sizesList = product.sizes as any[];
    }
  });

  const sizesJson = $derived(sizesList.length > 0 ? JSON.stringify(sizesList) : '');
  const primaryImageUrl = $derived(product.product_images?.find((img: any) => img.is_primary)?.url || '');

  function addSizeOption() {
    if (!sizeLabel || sizePrice <= 0) return;
    const mlMatch = sizeLabel.match(/\d+/);
    const mlVal = mlMatch ? Number(mlMatch[0]) : 0;

    sizesList = [...sizesList, { label: sizeLabel, price: sizePrice, ml: mlVal }];
    sizeLabel = '';
    sizePrice = 0;
  }

  function removeSizeOption(idx: number) {
    sizesList = sizesList.filter((_, i) => i !== idx);
  }

  $effect(() => {
    if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<svelte:head>
  <title>Edit Product — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex items-center gap-3">
    <a href="/admin/products" class="flex h-8 w-8 items-center justify-center rounded-full hover:bg-gray-100 transition-colors">
      <ArrowLeft class="h-4 w-4" />
    </a>
    <div>
      <h1 class="font-heading text-2xl font-bold">Edit Product</h1>
      <p class="text-xs text-[var(--text-muted)] font-mono">ID: {product.id}</p>
    </div>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <form
    method="post"
    action="?/updateProduct"
    enctype="multipart/form-data"
    use:enhance={() => {
      loading = true;
      return async ({ update }) => {
        loading = false;
        await update();
      };
    }}
    class="grid gap-8 lg:grid-cols-3"
  >
    <input type="hidden" name="sizesJson" value={sizesJson} />

    <!-- Left column: general details -->
    <div class="lg:col-span-2 space-y-6">
      <!-- General info -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">1. General Information</h3>
        
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-1">
            <label for="name" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Name</label>
            <Input id="name" name="name" type="text" value={product.name} required />
          </div>
          <div class="space-y-1">
            <label for="brand" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Brand</label>
            <Input id="brand" name="brand" type="text" value={product.brand} required />
          </div>
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-1">
            <label for="slug" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Slug</label>
            <Input id="slug" name="slug" type="text" value={product.slug} required />
          </div>
          <div class="space-y-1">
            <label for="categoryId" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Category</label>
            <select
              id="categoryId"
              name="categoryId"
              value={product.category_id || ''}
              class="flex h-10 w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3.5 py-2 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 transition-all"
            >
              <option value="">Select Category</option>
              {#each categories as cat}
                <option value={cat.id}>{cat.name}</option>
              {/each}
            </select>
          </div>
        </div>

        <div class="space-y-1">
          <label for="shortDesc" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Short Description</label>
          <Input id="shortDesc" name="shortDesc" type="text" value={product.short_description || ''} />
        </div>

        <div class="space-y-1">
          <label for="description" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Long Description</label>
          <Textarea id="description" name="description" value={product.description || ''} rows={5} />
        </div>
      </div>

      <!-- Notes -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">2. Fragrance Notes (Comma Separated)</h3>
        
        <div class="space-y-3">
          <div class="space-y-1">
            <label for="topNotes" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Top Notes</label>
            <Input id="topNotes" name="topNotes" type="text" value={product.top_notes?.join(', ') || ''} />
          </div>
          <div class="space-y-1">
            <label for="middleNotes" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Middle Notes</label>
            <Input id="middleNotes" name="middleNotes" type="text" value={product.middle_notes?.join(', ') || ''} />
          </div>
          <div class="space-y-1">
            <label for="baseNotes" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Base Notes</label>
            <Input id="baseNotes" name="baseNotes" type="text" value={product.base_notes?.join(', ') || ''} />
          </div>
        </div>
      </div>

      <!-- Sizes -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">3. Size Pricing Options (Decants)</h3>
        
        <div class="grid grid-cols-3 gap-3 items-end bg-gray-50/50 p-4 rounded-xl dark:bg-gray-900/50">
          <div>
            <label for="sizeLabel" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Size (e.g. 5ml)</label>
            <Input id="sizeLabel" type="text" bind:value={sizeLabel} placeholder="5ml" />
          </div>
          <div>
            <label for="sizePrice" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Price (৳)</label>
            <Input id="sizePrice" type="number" bind:value={sizePrice} placeholder="500" />
          </div>
          <Button type="button" variant="outline" onclick={addSizeOption} class="flex items-center gap-1.5 rounded-lg">
            <Plus class="h-4 w-4" />
            Add option
          </Button>
        </div>

        {#if sizesList.length > 0}
          <div class="space-y-2 mt-4">
            <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Added Sizes list:</h4>
            <div class="grid gap-2">
              {#each sizesList as sz, idx}
                <div class="flex items-center justify-between text-xs border border-gray-150 p-2.5 rounded-lg dark:border-gray-800 bg-white dark:bg-gray-950">
                  <span class="font-bold">{sz.label} ({sz.ml} ml)</span>
                  <span class="font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(sz.price)}</span>
                  <button type="button" onclick={() => removeSizeOption(idx)} class="text-red-500 font-semibold underline">Remove</button>
                </div>
              {/each}
            </div>
          </div>
        {/if}
      </div>
    </div>

    <!-- Right column: configs & visibility -->
    <div class="space-y-6">
      <!-- Media Settings -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">4. Product Media</h3>
        <div class="space-y-3">
          {#if primaryImageUrl}
            <div class="relative aspect-video w-full overflow-hidden rounded-lg bg-gray-100 dark:bg-gray-900 border">
              <img src={primaryImageUrl} alt="Current product" class="h-full w-full object-cover" />
            </div>
          {/if}
          
          <div class="space-y-1">
            <label for="imageFile" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Upload New Image</label>
            <Input id="imageFile" name="imageFile" type="file" accept="image/*" />
          </div>

          <div class="relative flex py-1.5 items-center">
            <div class="flex-grow border-t border-gray-200 dark:border-gray-800"></div>
            <span class="flex-shrink mx-3 text-[10px] text-[var(--text-muted)] font-bold uppercase tracking-widest">or</span>
            <div class="flex-grow border-t border-gray-200 dark:border-gray-800"></div>
          </div>

          <div class="space-y-1">
            <label for="imageUrl" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Or Main Image URL</label>
            <Input id="imageUrl" name="imageUrl" type="url" value={primaryImageUrl} />
          </div>
        </div>
      </div>

      <!-- Pricing / Stock -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">5. Pricing & Stock</h3>
        
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-1">
            <label for="price" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Base Price (৳)</label>
            <Input id="price" name="price" type="number" value={product.price} required />
          </div>
          <div class="space-y-1">
            <label for="discountPrice" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Discount Price (৳)</label>
            <Input id="discountPrice" name="discountPrice" type="number" value={product.discount_price || ''} />
          </div>
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-1">
            <label for="stockQuantity" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Stock count</label>
            <Input id="stockQuantity" name="stockQuantity" type="number" value={product.stock_quantity} required />
          </div>
          <div class="space-y-1">
            <label for="gender" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Gender</label>
            <select
              id="gender"
              name="gender"
              value={product.gender}
              class="flex h-10 w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3.5 py-2 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 transition-all"
            >
              <option value="unisex">Unisex</option>
              <option value="men">Men</option>
              <option value="women">Women</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Settings & Visibility -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">6. Settings & Visibility</h3>
        
        <div class="space-y-1">
          <label for="status" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Status</label>
          <select
            id="status"
            name="status"
            value={product.status}
            class="flex h-10 w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3.5 py-2 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 transition-all"
          >
            <option value="active">Active</option>
            <option value="draft">Draft</option>
          </select>
        </div>

        <div class="space-y-3 pt-2">
          <!-- Featured -->
          <div class="flex items-center gap-2">
            <input type="checkbox" id="isFeatured" name="isFeatured" checked={product.is_featured} class="h-4 w-4 rounded border-gray-300 text-burgundy-600 focus:ring-burgundy-500" />
            <label for="isFeatured" class="text-xs font-semibold text-gray-700 dark:text-gray-300">Featured product</label>
          </div>

          <!-- Bestseller -->
          <div class="flex items-center gap-2">
            <input type="checkbox" id="isBestseller" name="isBestseller" checked={product.is_bestseller} class="h-4 w-4 rounded border-gray-300 text-burgundy-600 focus:ring-burgundy-500" />
            <label for="isBestseller" class="text-xs font-semibold text-gray-700 dark:text-gray-300">Best seller flag</label>
          </div>

          <!-- New arrival -->
          <div class="flex items-center gap-2">
            <input type="checkbox" id="isNewArrival" name="isNewArrival" checked={product.is_new_arrival} class="h-4 w-4 rounded border-gray-300 text-burgundy-600 focus:ring-burgundy-500" />
            <label for="isNewArrival" class="text-xs font-semibold text-gray-700 dark:text-gray-300">New arrival flag</label>
          </div>
        </div>

        <hr class="border-gray-100 dark:border-gray-800" />

        <Button
          type="submit"
          disabled={loading}
          class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3 flex items-center justify-center gap-2"
        >
          <Save class="h-4 w-4" />
          {loading ? 'Saving Changes...' : 'Save Changes'}
        </Button>
      </div>
    </div>
  </form>
</div>
