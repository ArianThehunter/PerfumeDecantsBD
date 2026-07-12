<script lang="ts">
  import { enhance } from '$app/forms';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { Textarea } from '$lib/components/ui/textarea';
  import { Plus, Edit3, Trash2, FolderHeart, X } from '@lucide/svelte';
  import { toast } from 'svelte-sonner';
  import * as Dialog from '$lib/components/ui/dialog';
  import type { ActionData, PageData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let categories = $derived(data.categories);
  
  // Dialog state
  let showAddModal = $state(false);
  let showEditModal = $state(false);
  let loading = $state(false);

  // Edit fields
  let editId = $state('');
  let editName = $state('');
  let editSlug = $state('');
  let editDesc = $state('');
  let editImage = $state('');
  let editOrder = $state(0);

  function openEdit(cat: any) {
    editId = cat.id;
    editName = cat.name;
    editSlug = cat.slug;
    editDesc = cat.description || '';
    editImage = cat.image_url || '';
    editOrder = cat.display_order;
    showEditModal = true;
  }

  $effect(() => {
    if (form?.success) {
      toast.success('Categories updated successfully');
      showAddModal = false;
      showEditModal = false;
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<svelte:head>
  <title>Manage Categories — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div>
      <h1 class="font-heading text-2xl font-bold">Category Management</h1>
      <p class="text-xs text-[var(--text-muted)]">Organize perfume classifications for filters and menus.</p>
    </div>
    <Button
      class="bg-burgundy-700 hover:bg-burgundy-800 text-white flex items-center gap-2 rounded-xl"
      onclick={() => (showAddModal = true)}
    >
      <Plus class="h-4 w-4" />
      Create Category
    </Button>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <div class="card-premium overflow-hidden">
    {#if categories.length === 0}
      <div class="flex min-h-[250px] flex-col items-center justify-center p-8 text-center">
        <FolderHeart class="h-10 w-10 text-gray-400" />
        <h3 class="mt-4 text-base font-semibold">No Categories Available</h3>
        <p class="text-xs text-[var(--text-muted)] mt-1">Start by creating your first perfume category.</p>
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100 dark:bg-gray-900 dark:border-gray-800 font-bold uppercase tracking-wider text-[var(--text-secondary)]">
              <th class="p-4">Image</th>
              <th class="p-4">Category Name</th>
              <th class="p-4">Slug</th>
              <th class="p-4">Description</th>
              <th class="p-4 text-center">Display Order</th>
              <th class="p-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            {#each categories as cat}
              <tr class="hover:bg-gray-50/50 dark:hover:bg-gray-900/50 transition-colors">
                <td class="p-4">
                  <div class="h-12 w-16 overflow-hidden rounded-lg bg-gray-50 border">
                    <img src={cat.image_url} alt="" class="h-full w-full object-cover" />
                  </div>
                </td>
                <td class="p-4 font-bold text-gray-900 dark:text-white text-sm">{cat.name}</td>
                <td class="p-4 font-mono">{cat.slug}</td>
                <td class="p-4 max-w-xs truncate text-[var(--text-secondary)]">{cat.description || 'No description'}</td>
                <td class="p-4 text-center font-bold">{cat.display_order}</td>
                <td class="p-4">
                  <div class="flex items-center justify-center gap-2">
                    <button
                      onclick={() => openEdit(cat)}
                      class="flex h-8 w-8 items-center justify-center rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800"
                      aria-label="Edit category"
                    >
                      <Edit3 class="h-4 w-4" />
                    </button>
                    <form
                      method="post"
                      action="?/deleteCategory"
                      use:enhance={() => {
                        loading = true;
                        return async ({ update }) => {
                          loading = false;
                          await update();
                        };
                      }}
                    >
                      <input type="hidden" name="id" value={cat.id} />
                      <button
                        type="submit"
                        disabled={loading}
                        class="flex h-8 w-8 items-center justify-center rounded-lg text-gray-400 hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-950/20"
                        aria-label="Delete category"
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

<!-- Create Category Modal -->
<Dialog.Root open={showAddModal} onOpenChange={(open) => (showAddModal = open)}>
  <Dialog.Content class="max-w-md">
    <Dialog.Header>
      <Dialog.Title class="font-heading text-lg font-bold">Add Category</Dialog.Title>
    </Dialog.Header>

    <form
      method="post"
      action="?/createCategory"
      use:enhance={() => {
        loading = true;
        return async ({ update }) => {
          loading = false;
          await update();
        };
      }}
      class="space-y-4 pt-4"
    >
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="name" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Name</label>
          <Input id="name" name="name" type="text" placeholder="Eau de Parfum" required />
        </div>
        <div>
          <label for="slug" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Slug</label>
          <Input id="slug" name="slug" type="text" placeholder="eau-de-parfum" required />
        </div>
      </div>

      <div>
        <label for="description" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Description</label>
        <Textarea id="description" name="description" placeholder="Description of this category..." rows={3} />
      </div>

      <div class="grid grid-cols-3 gap-4 items-end">
        <div class="col-span-2">
          <label for="imageUrl" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Image URL</label>
          <Input id="imageUrl" name="imageUrl" type="url" placeholder="https://unsplash.com/..." />
        </div>
        <div>
          <label for="displayOrder" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Order</label>
          <Input id="displayOrder" name="displayOrder" type="number" value="0" />
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-4 border-t mt-4">
        <Button variant="outline" type="button" onclick={() => (showAddModal = false)}>
          Cancel
        </Button>
        <Button type="submit" disabled={loading} class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold">
          {loading ? 'Creating...' : 'Create'}
        </Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>

<!-- Edit Category Modal -->
<Dialog.Root open={showEditModal} onOpenChange={(open) => (showEditModal = open)}>
  <Dialog.Content class="max-w-md">
    <Dialog.Header>
      <Dialog.Title class="font-heading text-lg font-bold">Edit Category</Dialog.Title>
    </Dialog.Header>

    <form
      method="post"
      action="?/updateCategory"
      use:enhance={() => {
        loading = true;
        return async ({ update }) => {
          loading = false;
          await update();
        };
      }}
      class="space-y-4 pt-4"
    >
      <input type="hidden" name="id" value={editId} />

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="editName" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Name</label>
          <Input id="editName" name="name" type="text" required bind:value={editName} />
        </div>
        <div>
          <label for="editSlug" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Slug</label>
          <Input id="editSlug" name="slug" type="text" required bind:value={editSlug} />
        </div>
      </div>

      <div>
        <label for="editDesc" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Description</label>
        <Textarea id="editDesc" name="description" rows={3} bind:value={editDesc} />
      </div>

      <div class="grid grid-cols-3 gap-4 items-end">
        <div class="col-span-2">
          <label for="editImage" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Image URL</label>
          <Input id="editImage" name="imageUrl" type="url" bind:value={editImage} />
        </div>
        <div>
          <label for="editOrder" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Order</label>
          <Input id="editOrder" name="displayOrder" type="number" bind:value={editOrder} />
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-4 border-t mt-4">
        <Button variant="outline" type="button" onclick={() => (showEditModal = false)}>
          Cancel
        </Button>
        <Button type="submit" disabled={loading} class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold">
          {loading ? 'Saving...' : 'Save Changes'}
        </Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>
