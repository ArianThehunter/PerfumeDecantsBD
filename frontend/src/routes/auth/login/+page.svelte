<!--
  PerfumeDecantBD — Login Page
-->
<script lang="ts">
  let email = $state('');
  let password = $state('');
  let showPassword = $state(false);
  let loading = $state(false);
</script>

<svelte:head>
  <title>Sign In — PerfumeDecantBD</title>
</svelte:head>

<div class="min-h-screen flex">
  <!-- Left: Form -->
  <div class="flex-1 flex items-center justify-center px-6 py-32 bg-white">
    <div class="w-full max-w-md">
      <div class="text-center mb-10">
        <a href="/" class="inline-flex items-center gap-2 mb-8">
          <div class="w-10 h-10 rounded-full bg-gradient-gold flex items-center justify-center text-white font-bold text-lg font-[var(--font-heading)]">P</div>
          <span class="text-xl font-bold font-[var(--font-heading)] text-warm-950">PerfumeDecant<span class="text-gradient-gold">BD</span></span>
        </a>
        <h1 class="text-3xl font-bold font-[var(--font-heading)] text-warm-950 mb-2">Welcome Back</h1>
        <p class="text-warm-500 font-light">Sign in to access your account and orders</p>
      </div>

      <form class="space-y-5" onsubmit={(e) => { e.preventDefault(); loading = true; }}>
        <div>
          <label for="login-email" class="block text-sm font-medium text-warm-700 mb-2">Email Address</label>
          <input id="login-email" bind:value={email} type="email" placeholder="your@email.com" class="luxury-input" required />
        </div>
        <div>
          <label for="login-password" class="block text-sm font-medium text-warm-700 mb-2">Password</label>
          <div class="relative">
            <input
              id="login-password"
              bind:value={password}
              type={showPassword ? 'text' : 'password'}
              placeholder="Enter your password"
              class="luxury-input pr-12"
              required
            />
            <button type="button" onclick={() => showPassword = !showPassword} class="absolute right-3 top-1/2 -translate-y-1/2 text-warm-400 hover:text-warm-600">
              {#if showPassword}
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" /></svg>
              {:else}
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /></svg>
              {/if}
            </button>
          </div>
        </div>

        <div class="flex items-center justify-between">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" class="w-4 h-4 rounded-none border-warm-300 text-primary-500 focus:ring-primary-500" />
            <span class="text-sm text-warm-600">Remember me</span>
          </label>
          <a href="/auth/forgot-password" class="text-sm text-primary-600 hover:text-primary-700 font-medium">Forgot password?</a>
        </div>

        <button type="submit" class="btn-primary w-full py-4" disabled={loading}>
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <div class="luxury-divider my-8"></div>

      <p class="text-center text-sm text-warm-500">
        Don't have an account?
        <a href="/auth/register" class="text-primary-600 hover:text-primary-700 font-medium">Create one</a>
      </p>
    </div>
  </div>

  <!-- Right: Visual -->
  <div class="hidden lg:block lg:w-[480px] xl:w-[560px] relative bg-gradient-hero">
    <div class="absolute inset-0 flex items-center justify-center p-12">
      <div class="text-center">
        <div class="text-8xl mb-8 animate-float">🧴</div>
        <h2 class="text-3xl font-bold text-white font-[var(--font-heading)] mb-4">Discover Your Signature</h2>
        <p class="text-warm-400 font-light font-[var(--font-accent)] text-lg">
          Over 500 authentic luxury fragrances await. Find the one that defines you.
        </p>
      </div>
    </div>
    <div class="absolute top-20 left-10 w-32 h-32 rounded-full bg-primary-500/10 blur-3xl animate-float"></div>
    <div class="absolute bottom-20 right-10 w-40 h-40 rounded-full bg-secondary-500/10 blur-3xl animate-float delay-300"></div>
  </div>
</div>
