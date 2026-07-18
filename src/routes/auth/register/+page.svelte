<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { enhance } from '$app/forms';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { toast } from 'svelte-sonner';

  let fullName = $state('');
  let email = $state('');
  let phone = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let loading = $state(false);

  // Phone Validation Regex: 11 digits, starts with 01, numbers only
  const phoneRegex = /^01\d{9}$/;
  let isPhoneValid = $derived(phone === '' || phoneRegex.test(phone));
  let phoneErrorMsg = $derived(
    phone !== '' && !phoneRegex.test(phone)
      ? 'Must start with 01, contain exactly 11 digits, with no spaces, dashes, or letters.'
      : ''
  );
</script>

<svelte:head>
  <title>Register</title>
</svelte:head>

<div class="flex min-h-[80vh] items-center justify-center bg-[var(--bg-secondary)] px-4 py-12">
  <div class="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-xl dark:bg-gray-950 border border-gray-100 dark:border-gray-900">
    <div class="text-center">
      <img src="/logo.jpg" alt="PerfumeDecantsBD" class="mx-auto h-16 w-16 rounded-full object-cover" />
      <h2 class="font-heading mt-6 text-3xl font-bold tracking-tight text-burgundy-950 dark:text-cream-200">
        Create a new account
      </h2>
      <p class="mt-2 text-sm text-[var(--text-muted)]">
        Or
        <a href="/auth/login{page.url.search ? page.url.search : ''}" class="font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline">
          sign in to your existing account
        </a>
      </p>
    </div>

    <form
      class="mt-8 space-y-4"
      method="POST"
      action="?/register"
      use:enhance={() => {
        // Double check client side validations before submitting
        if (!fullName || !email || !phone || !password || !confirmPassword) {
          toast.error('All fields are required.');
          return;
        }

        if (!phoneRegex.test(phone)) {
          toast.error('Phone number must start with 01 and be exactly 11 digits.');
          return;
        }

        if (password !== confirmPassword) {
          toast.error('Passwords do not match.');
          return;
        }

        loading = true;
        return async ({ result }) => {
          loading = false;
          if (result.type === 'success') {
            toast.success('Registration successful! Please check your email to verify your account.');
            setTimeout(() => {
              goto('/auth/login' + page.url.search);
            }, 1500);
          } else if (result.type === 'failure') {
            const data = result.data as { message?: string };
            toast.error(data?.message || 'Failed to register.');
          }
        };
      }}
    >
      <div class="space-y-1">
        <label for="name" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Full Name</label>
        <Input
          id="name"
          name="fullName"
          type="text"
          required
          placeholder="John Doe"
          bind:value={fullName}
        />
      </div>

      <div class="space-y-1">
        <label for="email" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Email address</label>
        <Input
          id="email"
          name="email"
          type="email"
          required
          placeholder="yourname@example.com"
          bind:value={email}
        />
      </div>

      <div class="space-y-1">
        <label for="phone" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Phone Number</label>
        <Input
          id="phone"
          name="phone"
          type="tel"
          required
          placeholder="01770207576"
          bind:value={phone}
          class={!isPhoneValid ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : ''}
        />
        {#if phoneErrorMsg}
          <p class="text-[10px] text-red-500 font-semibold mt-0.5 leading-tight">{phoneErrorMsg}</p>
        {/if}
      </div>

      <div class="space-y-1">
        <label for="password" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Password</label>
        <Input
          id="password"
          name="password"
          type="password"
          required
          placeholder="••••••••"
          bind:value={password}
        />
      </div>

      <div class="space-y-1">
        <label for="confirm-password" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Confirm Password</label>
        <Input
          id="confirm-password"
          name="confirmPassword"
          type="password"
          required
          placeholder="••••••••"
          bind:value={confirmPassword}
        />
      </div>

      <Button
        type="submit"
        disabled={loading}
        class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3 mt-6"
      >
        {loading ? 'Registering...' : 'Register'}
      </Button>
    </form>
  </div>
</div>
