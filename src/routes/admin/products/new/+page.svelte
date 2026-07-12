<script lang="ts">
  import { enhance } from '$app/forms';
  import { ArrowLeft, Save, Plus } from '@lucide/svelte';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { Textarea } from '$lib/components/ui/textarea';
  import { toast } from 'svelte-sonner';
  import type { PageData, ActionData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let categories = $derived(data.categories);
  let loading = $state(false);

  // Helper state to input decant sizes visually
  let sizeLabel = $state('');
  let sizePrice = $state(0);
  let sizesList = $state<{ label: string; price: number; ml: number }[]>([]);

  // Computed json string for form submit
  const sizesJson = $derived(sizesList.length > 0 ? JSON.stringify(sizesList) : '');

  function addSizeOption() {
    if (!sizeLabel || sizePrice <= 0) return;
    
    // Parse ml from label or guess, e.g. "5ml" -> 5
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
  <title>New Product — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex items-center gap-3">
    <a href="/admin/products" class="flex h-8 w-8 items-center justify-center rounded-full hover:bg-gray-100 transition-colors">
      <ArrowLeft class="h-4 w-4" />
    </a>
    <div>
      <h1 class="font-heading text-2xl font-bold">Add New Product</h1>
      <p class="text-xs text-[var(--text-muted)]">Configure a new perfume decant option in your inventory.</p>
    </div>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <form
    method="post"
    action="?/createProduct"
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
    <!-- Hidden fields -->
    <input type="hidden" name="sizesJson" value={sizesJson} />

    <!-- Left Column: Core Fields -->
    <div class="lg:col-span-2 space-y-6">
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">1. General Information</h3>
        
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-1">
            <label for="name" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Name</label>
            <Input id="name" name="name" type="text" placeholder="Creed Aventus" required />
          </div>
          <div class="space-y-1">
            <label for="brand" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Brand</label>
            <Input id="brand" name="brand" type="text" placeholder="Creed" required />
          </div>
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-1">
            <label for="slug" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Slug</label>
            <Input id="slug" name="slug" type="text" placeholder="creed-aventus" required />
          </div>
          <div class="space-y-1">
            <label for="categoryId" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Category</label>
            <select
              id="categoryId"
              name="categoryId"
              class="flex h-10 w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3.5 py-2 text-sm text-[var(--text-primary)] focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 transition-all"
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
          <Input id="shortDesc" name="shortDesc" type="text" placeholder="Brief tagline summarizing fragrance" />
        </div>

        <div class="space-y-1">
          <label for="description" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Long Description</label>
          <Textarea id="description" name="description" placeholder="Full descriptive overview..." rows={5} />
        </div>
      </div>

      <!-- Notes -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">2. Fragrance Notes (Comma Separated)</h3>
        
        <div class="space-y-3">
          <div class="space-y-1">
            <label for="topNotes" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Top Notes</label>
            <Input id="topNotes" name="topNotes" type="text" placeholder="Pineapple, Bergamot, Apple" />
          </div>
          <div class="space-y-1">
            <label for="middleNotes" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Middle Notes</label>
            <Input id="middleNotes" name="middleNotes" type="text" placeholder="Birch, Patchouli, Jasmine" />
          </div>
          <div class="space-y-1">
            <label for="baseNotes" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Base Notes</label>
            <Input id="baseNotes" name="baseNotes" type="text" placeholder="Musk, Oakmoss, Ambergris" />
          </div>
        </div>
      </div>

      <!-- Decant Sizes Builder -->
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

    <!-- Right Column: Settings & Pricing -->
    <div class="space-y-6">
      <!-- Media Settings -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">4. Product Media</h3>
        <div class="space-y-3">
          <div class="space-y-1">
            <label for="imageFile" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Upload Image File</label>
            <Input id="imageFile" name="imageFile" type="file" accept="image/*" />
          </div>
          
          <div class="relative flex py-1.5 items-center">
            <div class="flex-grow border-t border-gray-200 dark:border-gray-800"></div>
            <span class="flex-shrink mx-3 text-[10px] text-[var(--text-muted)] font-bold uppercase tracking-widest">or</span>
            <div class="flex-grow border-t border-gray-200 dark:border-gray-800"></div>
          </div>

          <div class="space-y-1">
            <label for="imageUrl" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Or Main Image URL</label>
            <Input id="imageUrl" name="imageUrl" type="url" placeholder="https://unsplash.com/..." />
          </div>
        </div>
      </div>

      <!-- Pricing / Stock -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">5. Pricing & Stock</h3>
        
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-1">
            <label for="price" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Base Price (৳)</label>
            <Input id="price" name="price" type="number" required />
          </div>
          <div class="space-y-1">
            <label for="discountPrice" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Discount Price (৳)</label>
            <Input id="discountPrice" name="discountPrice" type="number" />
          </div>
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-1">
            <label for="stockQuantity" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Stock count</label>
            <Input id="stockQuantity" name="stockQuantity" type="number" value="10" required />
          </div>
          <div class="space-y-1">
            <label for="gender" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Gender</label>
            <select
              id="gender"
              name="gender"
              class="flex h-10 w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3.5 py-2 text-sm text-[var(--text-primary)] focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 transition-all"
            >
              <option value="unisex">Unisex</option>
              <option value="men">Men</option>
              <option value="women">Women</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Flags & Status -->
      <div class="card-premium p-6 space-y-4">
        <h3 class="font-heading text-base font-bold">6. Settings & Visibility</h3>
        
        <div class="space-y-1">
          <label for="status" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Status</label>
          <select
            id="status"
            name="status"
            class="flex h-10 w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3.5 py-2 text-sm text-[var(--text-primary)] focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 transition-all"
          >
            <option value="active">Active</option>
            <option value="draft">Draft</option>
          </select>
        </div>

        <div class="space-y-3 pt-2">
          <!-- Featured -->
          <div class="flex items-center gap-2">
            <input type="checkbox" id="isFeatured" name="isFeatured" class="h-4 w-4 rounded border-gray-300 text-burgundy-600 focus:ring-burgundy-500" />
            <label for="isFeatured" class="text-xs font-semibold text-gray-700 dark:text-gray-300">Featured product</label>
          </div>

          <!-- Bestseller -->
          <div class="flex items-center gap-2">
            <input type="checkbox" id="isBestseller" name="isBestseller" class="h-4 w-4 rounded border-gray-300 text-burgundy-600 focus:ring-burgundy-500" />
            <label for="isBestseller" class="text-xs font-semibold text-gray-700 dark:text-gray-300">Best seller flag</label>
          </div>

          <!-- New arrival -->
          <div class="flex items-center gap-2">
            <input type="checkbox" id="isNewArrival" name="isNewArrival" class="h-4 w-4 rounded border-gray-300 text-burgundy-600 focus:ring-burgundy-500" />
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
          {loading ? 'Creating Product...' : 'Save Product'}
        </Button>
      </div>
    </div>
  </form>
</div>
