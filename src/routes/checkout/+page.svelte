<script lang="ts">
  import { enhance } from '$app/forms';
  import { goto } from '$app/navigation';
  import { cart } from '$lib/stores/cart.svelte';
  import { formatPrice } from '$lib/utils/formatters';
  import { ArrowLeft, CreditCard, Banknote, ShieldAlert } from '@lucide/svelte';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Textarea } from '$lib/components/ui/textarea';
  import { toast } from 'svelte-sonner';
  import type { PageData, ActionData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let addresses = $derived(data.addresses);
  let profile = $derived(data.profile);

  // Form states
  let selectedAddressId = $state('new');
  let paymentMethod = $state<'cod' | 'bank_transfer'>('cod');
  let notes = $state('');
  let transactionId = $state('');
  let loading = $state(false);

  // Address entry fields (used if selectedAddressId === 'new')
  let fullName = $state('');
  let phone = $state('');
  let addressLine1 = $state('');
  let addressLine2 = $state('');
  let city = $state('');
  let postalCode = $state('');

  $effect(() => {
    if (addresses.length > 0 && selectedAddressId === 'new') {
      selectedAddressId = addresses[0].id;
    }
  });

  $effect(() => {
    if (profile) {
      if (!fullName) fullName = profile.full_name || '';
      if (!phone) phone = profile.phone || '';
    }
  });

  // Auto-redirect if cart is empty
  $effect(() => {
    if (cart.items.length === 0 && !loading && !form?.success) {
      toast.error('Your shopping cart is empty');
      goto('/shop');
    }
  });

  $effect(() => {
    if (form?.success && form.orderId) {
      // Clear cart
      cart.clearCart();
      toast.success('Order placed successfully!');
      goto(`/checkout/confirmation?id=${form.orderId}`);
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<svelte:head>
  <title>Checkout — PerfumeDecantsBD</title>
</svelte:head>

<div class="bg-[var(--bg-secondary)] py-10 lg:py-16 min-h-[85vh]">
  <div class="container-luxury">
    <!-- Header -->
    <div class="mb-8 flex items-center gap-3">
      <a href="/cart" class="flex h-9 w-9 items-center justify-center rounded-full hover:bg-gray-200 transition-colors">
        <ArrowLeft class="h-5 w-5" />
      </a>
      <h1 class="font-heading text-3xl font-bold">Secure Checkout</h1>
    </div>

    <div class="grid gap-8 lg:grid-cols-[1fr_380px]">
      <!-- Left: Checkout Form -->
      <div class="space-y-6">
        <form
          method="post"
          action="?/placeOrder"
          use:enhance={() => {
            loading = true;
            return async ({ update }) => {
              loading = false;
              await update();
            };
          }}
          class="space-y-6"
        >
          <!-- Hidden inputs for form action -->
          <input type="hidden" name="cartItems" value={JSON.stringify(cart.items)} />
          <input type="hidden" name="paymentMethod" value={paymentMethod} />

          <!-- Shipping Destination Card -->
          <div class="card-premium p-6 space-y-4">
            <h3 class="font-heading text-lg font-bold">1. Shipping Address</h3>
            <hr class="border-gray-100 dark:border-gray-800" />

            {#if addresses.length > 0}
              <div class="space-y-2">
                <label for="address-selector" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Choose saved address</label>
                <select
                  id="address-selector"
                  name="addressId"
                  bind:value={selectedAddressId}
                  class="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                >
                  {#each addresses as addr}
                    <option value={addr.id}>
                      {addr.label}: {addr.full_name} - {addr.address_line_1}, {addr.city}
                    </option>
                  {/each}
                  <option value="new">+ Ship to a new address</option>
                </select>
              </div>
            {/if}

            {#if selectedAddressId === 'new' || addresses.length === 0}
              <input type="hidden" name="addressId" value="new" />
              <div class="space-y-4 pt-2">
                {#if !profile}
                  <div class="space-y-1">
                    <label for="guestEmail" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Email Address</label>
                    <Input id="guestEmail" name="guestEmail" type="email" placeholder="yourname@example.com" required />
                  </div>
                {/if}

                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-1">
                    <label for="fullName" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Full Name</label>
                    <Input id="fullName" name="fullName" type="text" placeholder="Recipient's name" required bind:value={fullName} />
                  </div>
                  <div class="space-y-1">
                    <label for="phone" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Phone Number</label>
                    <Input id="phone" name="phone" type="tel" placeholder="+880 1XXX-XXXXXX" required bind:value={phone} />
                  </div>
                </div>

                <div class="space-y-1">
                  <label for="addressLine1" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Address Line 1</label>
                  <Input id="addressLine1" name="addressLine1" type="text" placeholder="House/Flat No., Road/Street" required bind:value={addressLine1} />
                </div>

                <div class="space-y-1">
                  <label for="addressLine2" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Address Line 2 (Optional)</label>
                  <Input id="addressLine2" name="addressLine2" type="text" placeholder="Area, Landmark" bind:value={addressLine2} />
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-1">
                    <label for="city" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">City</label>
                    <Input id="city" name="city" type="text" placeholder="Dhaka" required bind:value={city} />
                  </div>
                  <div class="space-y-1">
                    <label for="postalCode" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Postal Code</label>
                    <Input id="postalCode" name="postalCode" type="text" placeholder="1212" required bind:value={postalCode} />
                  </div>
                </div>
              </div>
            {/if}
          </div>

          <!-- Order Notes -->
          <div class="card-premium p-6 space-y-4">
            <h3 class="font-heading text-lg font-bold">2. Order Notes (Optional)</h3>
            <hr class="border-gray-100 dark:border-gray-800" />
            <Textarea
              name="notes"
              rows={3}
              placeholder="Notes about your order, e.g. special instructions for delivery."
              bind:value={notes}
            />
          </div>

          <!-- Payment Methods -->
          <div class="card-premium p-6 space-y-4">
            <h3 class="font-heading text-lg font-bold">3. Payment Method</h3>
            <hr class="border-gray-100 dark:border-gray-800" />

            <div class="grid gap-4 sm:grid-cols-2">
              <!-- COD -->
              <button
                type="button"
                onclick={() => (paymentMethod = 'cod')}
                class="flex items-center gap-4 rounded-xl border-2 p-4 text-left transition-all {paymentMethod === 'cod' 
                  ? 'border-burgundy-700 bg-burgundy-50/10 dark:border-gold-500 dark:bg-gold-950/15' 
                  : 'border-gray-200 dark:border-gray-850'}"
              >
                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                  <Banknote class="h-5 w-5 text-gray-700 dark:text-gray-300" />
                </div>
                <div>
                  <h4 class="font-bold text-sm">Cash on Delivery</h4>
                  <p class="text-[10px] text-[var(--text-muted)]">Pay when items are delivered.</p>
                </div>
              </button>

              <!-- Bank Transfer -->
              <button
                type="button"
                onclick={() => (paymentMethod = 'bank_transfer')}
                class="flex items-center gap-4 rounded-xl border-2 p-4 text-left transition-all {paymentMethod === 'bank_transfer' 
                  ? 'border-burgundy-700 bg-burgundy-50/10 dark:border-gold-500 dark:bg-gold-950/15' 
                  : 'border-gray-200 dark:border-gray-850'}"
              >
                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                  <CreditCard class="h-5 w-5 text-gray-700 dark:text-gray-300" />
                </div>
                <div>
                  <h4 class="font-bold text-sm">Bank Transfer</h4>
                  <p class="text-[10px] text-[var(--text-muted)]">Manual bank or bKash payment.</p>
                </div>
              </button>
            </div>

            {#if paymentMethod === 'bank_transfer'}
              <div class="animate-scale-in rounded-xl bg-burgundy-50/45 p-5 text-xs dark:bg-burgundy-950/20 text-[var(--text-secondary)] space-y-3">
                <p class="font-bold text-burgundy-850 dark:text-gold-400 flex items-center gap-1.5 text-sm">
                  <ShieldAlert class="h-4.5 w-4.5 shrink-0" />
                  bKash / Nagad / Bank Transfer Payment
                </p>
                <div class="space-y-2 leading-relaxed">
                  <p>Please follow these steps to complete your payment:</p>
                  <ol class="list-decimal pl-4 space-y-1">
                    <li>Open your **bKash** or **Nagad** app (or use *247# / *167#).</li>
                    <li>Select **Send Money** (Personal account).</li>
                    <li>Enter Number: <strong class="text-burgundy-900 dark:text-gold-400">017XX-XXXXXX</strong> (bKash) or <strong class="text-burgundy-900 dark:text-gold-400">019XX-XXXXXX</strong> (Nagad).</li>
                    <li>Send the exact grand total.</li>
                    <li>Keep the Transaction ID (TxnID) and enter it below.</li>
                  </ol>
                </div>
                
                <hr class="border-gray-200 dark:border-gray-800" />
                
                <div class="space-y-1.5">
                  <label for="transactionId" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Payment Transaction ID (TxnID) / Reference</label>
                  <Input
                    id="transactionId"
                    name="transactionId"
                    type="text"
                    placeholder="e.g. AM12BD34G5 or Your Name"
                    required={paymentMethod === 'bank_transfer'}
                    bind:value={transactionId}
                    class="bg-white dark:bg-gray-900 border-gray-300 dark:border-gray-800"
                  />
                  <p class="text-[10px] text-[var(--text-muted)]">This will help us confirm your payment faster.</p>
                </div>
              </div>
            {/if}
          </div>

          <!-- Submit order -->
          <Button
            type="submit"
            disabled={loading}
            class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-bold h-12 rounded-xl text-base shadow-md"
          >
            {#if loading}
              Processing Order...
            {:else}
              Place Order — {formatPrice(cart.total)}
            {/if}
          </Button>
        </form>
      </div>

      <!-- Right: Order Summary -->
      <div>
        <div class="card-premium p-6 space-y-4 sticky top-24 bg-white dark:bg-gray-950">
          <h3 class="font-heading text-xl font-bold">Your Order</h3>
          <hr class="border-gray-100 dark:border-gray-800" />

          <!-- Cart items preview -->
          <div class="divide-y divide-gray-100 max-h-60 overflow-y-auto pr-1 dark:divide-gray-850">
            {#each cart.items as item}
              <div class="py-3 flex gap-3 items-center">
                <div class="h-10 w-10 shrink-0 overflow-hidden rounded-lg bg-gray-50 border border-gray-100 dark:bg-gray-900 dark:border-gray-850">
                  <img src={item.product_image} alt="" class="h-full w-full object-cover" />
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="text-xs font-semibold truncate text-gray-900 dark:text-white leading-none">{item.product_name}</h4>
                  <span class="text-[10px] text-[var(--text-muted)] uppercase tracking-wider">{item.size || 'Default'} × {item.quantity}</span>
                </div>
                <span class="text-xs font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(item.unit_price * item.quantity)}</span>
              </div>
            {/each}
          </div>

          <hr class="border-gray-100 dark:border-gray-800" />

          <!-- Prices -->
          <div class="space-y-2.5 text-xs text-[var(--text-secondary)] font-medium">
            <div class="flex justify-between">
              <span>Subtotal</span>
              <span class="text-gray-900 dark:text-white font-bold">{formatPrice(cart.subtotal)}</span>
            </div>
            <div class="flex justify-between">
              <span>Shipping Fee</span>
              <span class="text-gray-900 dark:text-white font-bold">
                {#if cart.shippingCost === 0}
                  <span class="text-green-600">Free</span>
                {:else}
                  {formatPrice(cart.shippingCost)}
                {/if}
              </span>
            </div>
            <hr class="border-gray-100 dark:border-gray-800" />
            <div class="flex justify-between text-sm">
              <span class="font-heading font-bold text-gray-900 dark:text-white">Grand Total</span>
              <span class="font-heading font-bold text-burgundy-700 dark:text-gold-400">{formatPrice(cart.total)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
