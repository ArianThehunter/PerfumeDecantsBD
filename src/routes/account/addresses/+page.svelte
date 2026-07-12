<script lang="ts">
  import { enhance } from '$app/forms';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { Plus, Trash2, Home, Briefcase, MapPin, Check } from '@lucide/svelte';
  import { toast } from 'svelte-sonner';
  import * as Dialog from '$lib/components/ui/dialog';
  import type { ActionData, PageData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let addresses = $derived(data.addresses);
  let showAddModal = $state(false);
  let loading = $state(false);

  $effect(() => {
    if (form?.success) {
      toast.success('Addresses updated successfully');
      showAddModal = false;
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div>
      <h2 class="font-heading text-2xl font-bold">Saved Addresses</h2>
      <p class="text-sm text-[var(--text-muted)]">Manage your shipping destinations for faster checkout.</p>
    </div>
    <Button
      class="bg-burgundy-700 hover:bg-burgundy-800 text-white flex items-center gap-2 rounded-xl"
      onclick={() => (showAddModal = true)}
    >
      <Plus class="h-4 w-4" />
      Add New
    </Button>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  {#if addresses.length === 0}
    <div class="flex min-h-[250px] flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-200 p-8 text-center dark:border-gray-800">
      <MapPin class="h-10 w-10 text-gray-400" />
      <h3 class="mt-4 text-base font-semibold">No saved addresses</h3>
      <p class="mt-1 text-xs text-[var(--text-muted)]">Add a shipping address to use during checkout.</p>
      <Button
        variant="outline"
        class="mt-4"
        onclick={() => (showAddModal = true)}
      >
        Create New Address
      </Button>
    </div>
  {:else}
    <div class="grid gap-6 md:grid-cols-2">
      {#each addresses as addr}
        <div class="card-premium p-6 flex flex-col justify-between border relative {addr.is_default ? 'border-burgundy-600 bg-burgundy-50/10 dark:border-gold-500/50' : 'border-gray-100 dark:border-gray-800'}">
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="inline-flex items-center gap-1.5 rounded-full bg-gray-100 px-3 py-1 text-xs font-bold text-gray-800 capitalize dark:bg-gray-800 dark:text-gray-200">
                {#if addr.label.toLowerCase() === 'home'}
                  <Home class="h-3 w-3" />
                {:else if addr.label.toLowerCase() === 'office'}
                  <Briefcase class="h-3 w-3" />
                {:else}
                  <MapPin class="h-3 w-3" />
                {/if}
                {addr.label}
              </span>

              {#if addr.is_default}
                <span class="text-xs font-semibold text-burgundy-700 dark:text-gold-400 flex items-center gap-1">
                  <Check class="h-3.5 w-3.5" />
                  Default Shipping
                </span>
              {/if}
            </div>

            <h3 class="font-heading font-bold text-base text-gray-900 dark:text-white pt-1">{addr.full_name}</h3>
            <p class="text-xs text-[var(--text-muted)] font-medium">Phone: {addr.phone}</p>
            <p class="text-xs text-[var(--text-secondary)] leading-relaxed pt-1">
              {addr.address_line_1}
              {#if addr.address_line_2}
                <br />{addr.address_line_2}
              {/if}
              <br />{addr.city} - {addr.postal_code}
            </p>
          </div>

          <div class="flex items-center gap-3 border-t pt-4 mt-6">
            {#if !addr.is_default}
              <form method="post" action="?/setDefault" use:enhance>
                <input type="hidden" name="id" value={addr.id} />
                <button
                  type="submit"
                  class="text-xs font-bold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline"
                >
                  Set as Default
                </button>
              </form>
            {/if}

            <form
              method="post"
              action="?/deleteAddress"
              use:enhance={() => {
                loading = true;
                return async ({ update }) => {
                  loading = false;
                  await update();
                };
              }}
              class="ml-auto"
            >
              <input type="hidden" name="id" value={addr.id} />
              <button
                type="submit"
                disabled={loading}
                class="flex h-8 w-8 items-center justify-center rounded-lg text-gray-400 hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-950/20 transition-colors"
                aria-label="Delete address"
              >
                <Trash2 class="h-4 w-4" />
              </button>
            </form>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<!-- Add Address Dialog Modal -->
<Dialog.Root open={showAddModal} onOpenChange={(open) => (showAddModal = open)}>
  <Dialog.Content class="max-w-lg">
    <Dialog.Header>
      <Dialog.Title class="font-heading text-xl font-bold">Add Shipping Address</Dialog.Title>
    </Dialog.Header>

    <form
      method="post"
      action="?/addAddress"
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
          <label for="label" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Label</label>
          <Input id="label" name="label" type="text" placeholder="Home, Office, etc." required />
        </div>
        <div>
          <label for="fullName" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Full Name</label>
          <Input id="fullName" name="fullName" type="text" placeholder="Recipient's Name" required />
        </div>
      </div>

      <div>
        <label for="phone" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Phone Number</label>
        <Input id="phone" name="phone" type="tel" placeholder="+880 1XXX-XXXXXX" required />
      </div>

      <div>
        <label for="addressLine1" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Address Line 1</label>
        <Input id="addressLine1" name="addressLine1" type="text" placeholder="House/Flat No., Road/Street name" required />
      </div>

      <div>
        <label for="addressLine2" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Address Line 2 (Optional)</label>
        <Input id="addressLine2" name="addressLine2" type="text" placeholder="Area, Landmark" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="city" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">City</label>
          <Input id="city" name="city" type="text" placeholder="Dhaka, Chittagong, etc." required />
        </div>
        <div>
          <label for="postalCode" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Postal Code</label>
          <Input id="postalCode" name="postalCode" type="text" placeholder="1212" required />
        </div>
      </div>

      <div class="flex items-center gap-2 pt-2">
        <input type="checkbox" id="isDefault" name="isDefault" class="h-4 w-4 rounded border-gray-300 text-burgundy-600 focus:ring-burgundy-500" />
        <label for="isDefault" class="text-xs font-semibold text-gray-700 dark:text-gray-300">Set as default shipping address</label>
      </div>

      <div class="flex justify-end gap-3 pt-4 border-t">
        <Button variant="outline" type="button" onclick={() => (showAddModal = false)}>
          Cancel
        </Button>
        <Button type="submit" disabled={loading} class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold">
          {loading ? 'Adding...' : 'Add Address'}
        </Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>
