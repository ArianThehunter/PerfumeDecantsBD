<!--
  PerfumeDecantBD — Multi-Step Checkout
-->
<script lang="ts">
  let currentStep = $state(1);
  const steps = ['Shipping', 'Payment', 'Review'];

  // Shipping form
  let shipping = $state({
    firstName: '', lastName: '', email: '', phone: '',
    address1: '', address2: '', city: '', state: '', postal: '', country: 'Bangladesh',
  });

  // Payment
  let paymentMethod = $state('cash_on_delivery');

  const orderItems = [
    { name: 'Bleu de Chanel', variant: '100ml EDP', price: 4500, quantity: 1 },
    { name: 'Sauvage', variant: '100ml EDP', price: 4200, quantity: 2 },
  ];

  const subtotal = 12900;
  const shipping_cost = 0;
  const tax = 645;
  const total = 13545;

  const formatPrice = (price: number) => `৳${price.toLocaleString()}`;
</script>

<svelte:head>
  <title>Checkout — PerfumeDecantBD</title>
</svelte:head>

<div class="pt-32 pb-16 bg-warm-50 min-h-screen">
  <div class="container-luxury">
    <!-- Progress Steps -->
    <div class="flex items-center justify-center mb-12">
      {#each steps as step, i}
        <div class="flex items-center">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all
              {currentStep > i + 1 ? 'bg-green-500 text-white' : currentStep === i + 1 ? 'bg-primary-500 text-white' : 'bg-warm-200 text-warm-500'}">
              {#if currentStep > i + 1}
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" /></svg>
              {:else}
                {i + 1}
              {/if}
            </div>
            <span class="text-sm font-medium {currentStep >= i + 1 ? 'text-warm-900' : 'text-warm-400'} hidden sm:block">{step}</span>
          </div>
          {#if i < steps.length - 1}
            <div class="w-12 md:w-24 h-0.5 mx-4 {currentStep > i + 1 ? 'bg-green-500' : 'bg-warm-200'}"></div>
          {/if}
        </div>
      {/each}
    </div>

    <div class="grid lg:grid-cols-3 gap-10">
      <!-- Form Area -->
      <div class="lg:col-span-2">
        {#if currentStep === 1}
          <!-- Shipping Form -->
          <div class="luxury-card p-8 animate-fade-in">
            <h2 class="text-xl font-semibold font-[var(--font-heading)] text-warm-950 mb-6">Shipping Information</h2>
            <form class="space-y-4" onsubmit={(e) => { e.preventDefault(); currentStep = 2; }}>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-warm-700 mb-2">First Name</label>
                  <input bind:value={shipping.firstName} type="text" class="luxury-input" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-warm-700 mb-2">Last Name</label>
                  <input bind:value={shipping.lastName} type="text" class="luxury-input" required />
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-warm-700 mb-2">Email</label>
                  <input bind:value={shipping.email} type="email" class="luxury-input" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-warm-700 mb-2">Phone</label>
                  <input bind:value={shipping.phone} type="tel" class="luxury-input" required />
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-warm-700 mb-2">Address Line 1</label>
                <input bind:value={shipping.address1} type="text" class="luxury-input" required />
              </div>
              <div>
                <label class="block text-sm font-medium text-warm-700 mb-2">Address Line 2 (Optional)</label>
                <input bind:value={shipping.address2} type="text" class="luxury-input" />
              </div>
              <div class="grid grid-cols-3 gap-4">
                <div>
                  <label class="block text-sm font-medium text-warm-700 mb-2">City</label>
                  <input bind:value={shipping.city} type="text" class="luxury-input" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-warm-700 mb-2">State/Division</label>
                  <input bind:value={shipping.state} type="text" class="luxury-input" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-warm-700 mb-2">Postal Code</label>
                  <input bind:value={shipping.postal} type="text" class="luxury-input" required />
                </div>
              </div>
              <div class="flex justify-between pt-6">
                <a href="/cart" class="btn-ghost">← Back to Cart</a>
                <button type="submit" class="btn-primary">Continue to Payment</button>
              </div>
            </form>
          </div>

        {:else if currentStep === 2}
          <!-- Payment -->
          <div class="luxury-card p-8 animate-fade-in">
            <h2 class="text-xl font-semibold font-[var(--font-heading)] text-warm-950 mb-6">Payment Method</h2>
            <div class="space-y-4">
              {#each [{ value: 'cash_on_delivery', label: 'Cash on Delivery', icon: '💵', desc: 'Pay when you receive your order' }, { value: 'bkash', label: 'bKash', icon: '📱', desc: 'Pay via bKash mobile payment' }, { value: 'card', label: 'Credit/Debit Card', icon: '💳', desc: 'Visa, Mastercard, AMEX (Coming Soon)' }] as method}
                <label class="flex items-center gap-4 p-4 border cursor-pointer transition-all
                  {paymentMethod === method.value ? 'border-primary-500 bg-primary-50' : 'border-warm-200 hover:border-warm-300'}
                  {method.value === 'card' ? 'opacity-50 cursor-not-allowed' : ''}">
                  <input
                    type="radio"
                    name="payment"
                    value={method.value}
                    bind:group={paymentMethod}
                    disabled={method.value === 'card'}
                    class="w-4 h-4 border-warm-300 text-primary-500"
                  />
                  <span class="text-2xl">{method.icon}</span>
                  <div>
                    <p class="font-medium text-warm-900 text-sm">{method.label}</p>
                    <p class="text-warm-500 text-xs">{method.desc}</p>
                  </div>
                </label>
              {/each}
            </div>
            <div class="flex justify-between pt-8">
              <button onclick={() => currentStep = 1} class="btn-ghost">← Back</button>
              <button onclick={() => currentStep = 3} class="btn-primary">Review Order</button>
            </div>
          </div>

        {:else if currentStep === 3}
          <!-- Review -->
          <div class="luxury-card p-8 animate-fade-in">
            <h2 class="text-xl font-semibold font-[var(--font-heading)] text-warm-950 mb-6">Review Your Order</h2>

            <div class="space-y-6">
              <div>
                <h3 class="text-sm font-semibold uppercase tracking-wider text-warm-700 mb-3">Shipping To</h3>
                <div class="p-4 bg-warm-50 border border-warm-200 text-sm text-warm-700">
                  <p class="font-medium">{shipping.firstName || 'John'} {shipping.lastName || 'Doe'}</p>
                  <p>{shipping.address1 || '123 Main St'}</p>
                  <p>{shipping.city || 'Dhaka'}, {shipping.postal || '1205'}</p>
                  <p>{shipping.phone || '+880 1712-345678'}</p>
                </div>
              </div>

              <div>
                <h3 class="text-sm font-semibold uppercase tracking-wider text-warm-700 mb-3">Items ({orderItems.length})</h3>
                <div class="space-y-3">
                  {#each orderItems as item}
                    <div class="flex justify-between text-sm p-3 bg-warm-50 border border-warm-200">
                      <div>
                        <p class="font-medium text-warm-900">{item.name}</p>
                        <p class="text-warm-500 text-xs">{item.variant} × {item.quantity}</p>
                      </div>
                      <p class="font-medium text-warm-900">{formatPrice(item.price * item.quantity)}</p>
                    </div>
                  {/each}
                </div>
              </div>

              <div>
                <h3 class="text-sm font-semibold uppercase tracking-wider text-warm-700 mb-3">Payment</h3>
                <p class="text-sm text-warm-700 p-3 bg-warm-50 border border-warm-200">
                  💵 Cash on Delivery
                </p>
              </div>
            </div>

            <div class="flex justify-between pt-8">
              <button onclick={() => currentStep = 2} class="btn-ghost">← Back</button>
              <a href="/checkout/confirmation" class="btn-primary py-4 px-10">Place Order — {formatPrice(total)}</a>
            </div>
          </div>
        {/if}
      </div>

      <!-- Order Summary Sidebar -->
      <div class="lg:col-span-1">
        <div class="luxury-card p-6 sticky top-32">
          <h3 class="text-lg font-semibold font-[var(--font-heading)] text-warm-950 mb-4">Order Summary</h3>
          <div class="space-y-3 text-sm">
            {#each orderItems as item}
              <div class="flex justify-between text-warm-600">
                <span>{item.name} × {item.quantity}</span>
                <span>{formatPrice(item.price * item.quantity)}</span>
              </div>
            {/each}
            <div class="luxury-divider"></div>
            <div class="flex justify-between text-warm-600"><span>Subtotal</span><span>{formatPrice(subtotal)}</span></div>
            <div class="flex justify-between text-warm-600"><span>Shipping</span><span>Free</span></div>
            <div class="flex justify-between text-warm-600"><span>Tax (5%)</span><span>{formatPrice(tax)}</span></div>
            <div class="luxury-divider"></div>
            <div class="flex justify-between text-warm-950 font-semibold text-base"><span>Total</span><span>{formatPrice(total)}</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
