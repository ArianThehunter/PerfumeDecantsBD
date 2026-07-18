<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { createSupabaseClient } from '$lib/supabase';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { toast } from 'svelte-sonner';

  let email = $state('');
  let password = $state('');
  let loading = $state(false);

  // Initialize supabase browser client
  const supabase = createSupabaseClient(fetch);

  async function handleLogin(e: Event) {
    e.preventDefault();
    if (!email || !password) return;

    loading = true;
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password
    });

    if (error) {
      toast.error(error.message || 'Failed to login');
      loading = false;
    } else {
      toast.success('Successfully logged in');
      
      let redirectTo = page.url.searchParams.get('redirect');
      if (!redirectTo) {
        if (email.trim().toLowerCase() === 'admin@perfumedecantsbd.com') {
          redirectTo = '/admin';
        } else {
          redirectTo = '/';
        }
      }
      
      // Wait a brief moment to sync session
      setTimeout(() => {
        goto(redirectTo, { invalidateAll: true });
      }, 500);
    }
  }
</script>

<svelte:head>
  <title>Login</title>
</svelte:head>

<div class="flex min-h-[75vh] items-center justify-center bg-[var(--bg-secondary)] px-4 py-12">
  <div class="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-xl dark:bg-gray-950 border border-gray-100 dark:border-gray-900">
    <div class="text-center">
      <img src="/logo.jpg" alt="PerfumeDecantsBD" class="mx-auto h-16 w-16 rounded-full object-cover" />
      <h2 class="font-heading mt-6 text-3xl font-bold tracking-tight text-burgundy-950 dark:text-cream-200">
        Sign in to your account
      </h2>
      <p class="mt-2 text-sm text-[var(--text-muted)]">
        Or
        <a href="/auth/register{page.url.search ? page.url.search : ''}" class="font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline">
          register a new account
        </a>
      </p>
    </div>

    <form class="mt-8 space-y-4" onsubmit={handleLogin}>
      <div class="space-y-1">
        <label for="email" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Email address</label>
        <Input
          id="email"
          type="email"
          autocomplete="email"
          required
          placeholder="yourname@example.com"
          bind:value={email}
        />
      </div>

      <div class="space-y-1">
        <div class="flex items-center justify-between">
          <label for="password" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Password</label>
          <a href="/auth/forgot-password" class="text-xs font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline">
            Forgot password?
          </a>
        </div>
        <Input
          id="password"
          type="password"
          autocomplete="current-password"
          required
          placeholder="••••••••"
          bind:value={password}
        />
      </div>

      <Button
        type="submit"
        disabled={loading}
        class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3 mt-6"
      >
        {loading ? 'Signing in...' : 'Sign in'}
      </Button>
    </form>
  </div>
</div>
