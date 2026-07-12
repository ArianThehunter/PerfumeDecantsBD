<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { createSupabaseClient } from '$lib/supabase';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { toast } from 'svelte-sonner';

  let fullName = $state('');
  let email = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let loading = $state(false);

  // Initialize supabase browser client
  const supabase = createSupabaseClient(fetch);

  async function handleRegister(e: Event) {
    e.preventDefault();
    if (!fullName || !email || !password) return;

    if (email.trim().toLowerCase() === 'admin@perfumedecantsbd.com') {
      toast.error('Registration is restricted for this email address.');
      return;
    }

    if (password !== confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }

    loading = true;
    const { error, data } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName
        }
      }
    });

    if (error) {
      toast.error(error.message || 'Failed to register');
      loading = false;
    } else {
      toast.success('Registration successful! Please check your email to verify your account.');
      // Auto redirect to login or check target
      setTimeout(() => {
        goto('/auth/login' + page.url.search);
      }, 1500);
    }
  }
</script>

<svelte:head>
  <title>Register — PerfumeDecantsBD</title>
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

    <form class="mt-8 space-y-4" onsubmit={handleRegister}>
      <div class="space-y-1">
        <label for="name" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Full Name</label>
        <Input
          id="name"
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
          type="email"
          required
          placeholder="yourname@example.com"
          bind:value={email}
        />
      </div>

      <div class="space-y-1">
        <label for="password" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Password</label>
        <Input
          id="password"
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
