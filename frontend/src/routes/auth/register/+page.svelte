<!--
  PerfumeDecantBD — Register Page
-->
<script lang="ts">
  let firstName = $state('');
  let lastName = $state('');
  let email = $state('');
  let phone = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let showPassword = $state(false);
  let loading = $state(false);
  let agreed = $state(false);
</script>

<svelte:head>
  <title>Create Account — PerfumeDecantBD</title>
</svelte:head>

<div class="min-h-screen flex">
  <!-- Left: Visual -->
  <div class="hidden lg:block lg:w-[480px] xl:w-[560px] relative bg-gradient-hero">
    <div class="absolute inset-0 flex items-center justify-center p-12">
      <div class="text-center">
        <div class="text-8xl mb-8 animate-float">✨</div>
        <h2 class="text-3xl font-bold text-white font-[var(--font-heading)] mb-4">Join Our World</h2>
        <p class="text-warm-400 font-light font-[var(--font-accent)] text-lg">
          Create an account to save your favorites, track orders, and earn reward points.
        </p>
        <div class="flex items-center justify-center gap-8 mt-10 text-warm-500 text-sm">
          <div class="text-center">
            <p class="text-2xl font-bold text-primary-400 font-[var(--font-heading)]">500+</p>
            <p class="text-xs">Fragrances</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-primary-400 font-[var(--font-heading)]">5000+</p>
            <p class="text-xs">Customers</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-primary-400 font-[var(--font-heading)]">100%</p>
            <p class="text-xs">Authentic</p>
          </div>
        </div>
      </div>
    </div>
    <div class="absolute top-20 right-10 w-32 h-32 rounded-full bg-primary-500/10 blur-3xl animate-float"></div>
    <div class="absolute bottom-20 left-10 w-40 h-40 rounded-full bg-secondary-500/10 blur-3xl animate-float delay-300"></div>
  </div>

  <!-- Right: Form -->
  <div class="flex-1 flex items-center justify-center px-6 py-32 bg-white">
    <div class="w-full max-w-md">
      <div class="text-center mb-10">
        <a href="/" class="inline-flex items-center gap-2 mb-8">
          <div class="w-10 h-10 rounded-full bg-gradient-gold flex items-center justify-center text-white font-bold text-lg font-[var(--font-heading)]">P</div>
          <span class="text-xl font-bold font-[var(--font-heading)] text-warm-950">PerfumeDecant<span class="text-gradient-gold">BD</span></span>
        </a>
        <h1 class="text-3xl font-bold font-[var(--font-heading)] text-warm-950 mb-2">Create Account</h1>
        <p class="text-warm-500 font-light">Join our community of fragrance enthusiasts</p>
      </div>

      <form class="space-y-4" onsubmit={(e) => { e.preventDefault(); loading = true; }}>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="reg-fname" class="block text-sm font-medium text-warm-700 mb-2">First Name</label>
            <input id="reg-fname" bind:value={firstName} type="text" placeholder="First name" class="luxury-input" required />
          </div>
          <div>
            <label for="reg-lname" class="block text-sm font-medium text-warm-700 mb-2">Last Name</label>
            <input id="reg-lname" bind:value={lastName} type="text" placeholder="Last name" class="luxury-input" required />
          </div>
        </div>

        <div>
          <label for="reg-email" class="block text-sm font-medium text-warm-700 mb-2">Email Address</label>
          <input id="reg-email" bind:value={email} type="email" placeholder="your@email.com" class="luxury-input" required />
        </div>

        <div>
          <label for="reg-phone" class="block text-sm font-medium text-warm-700 mb-2">Phone Number</label>
          <input id="reg-phone" bind:value={phone} type="tel" placeholder="+880 1XXX-XXXXXX" class="luxury-input" />
        </div>

        <div>
          <label for="reg-password" class="block text-sm font-medium text-warm-700 mb-2">Password</label>
          <input id="reg-password" bind:value={password} type={showPassword ? 'text' : 'password'} placeholder="Minimum 8 characters" class="luxury-input" required minlength="8" />
        </div>

        <div>
          <label for="reg-confirm" class="block text-sm font-medium text-warm-700 mb-2">Confirm Password</label>
          <input id="reg-confirm" bind:value={confirmPassword} type="password" placeholder="Re-enter password" class="luxury-input" required />
        </div>

        <label class="flex items-start gap-3 cursor-pointer">
          <input bind:checked={agreed} type="checkbox" class="w-4 h-4 mt-0.5 rounded-none border-warm-300 text-primary-500 focus:ring-primary-500" required />
          <span class="text-sm text-warm-600">
            I agree to the <a href="/terms" class="text-primary-600 hover:underline">Terms of Service</a> and <a href="/privacy" class="text-primary-600 hover:underline">Privacy Policy</a>
          </span>
        </label>

        <button type="submit" class="btn-primary w-full py-4" disabled={loading || !agreed}>
          {loading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      <div class="luxury-divider my-8"></div>

      <p class="text-center text-sm text-warm-500">
        Already have an account?
        <a href="/auth/login" class="text-primary-600 hover:text-primary-700 font-medium">Sign in</a>
      </p>
    </div>
  </div>
</div>
