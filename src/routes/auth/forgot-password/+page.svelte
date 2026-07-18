<script lang="ts">
  import { createSupabaseClient } from '$lib/supabase';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { toast } from 'svelte-sonner';

  let email = $state('');
  let loading = $state(false);

  // Initialize supabase browser client
  const supabase = createSupabaseClient(fetch);

  async function handleReset(e: Event) {
    e.preventDefault();
    if (!email) return;

    loading = true;
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/callback?next=/reset-password`
    });

    if (error) {
      toast.error(error.message || 'Failed to send reset email');
      loading = false;
    } else {
      toast.success('Password reset link sent to your email.');
      email = '';
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Forgot Password</title>
</svelte:head>

<div class="flex min-h-[75vh] items-center justify-center bg-[var(--bg-secondary)] px-4 py-12">
  <div class="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-xl dark:bg-gray-950 border border-gray-100 dark:border-gray-900">
    <div class="text-center">
      <img src="/logo.jpg" alt="PerfumeDecantsBD" class="mx-auto h-16 w-16 rounded-full object-cover" />
      <h2 class="font-heading mt-6 text-3xl font-bold tracking-tight text-burgundy-950 dark:text-cream-200">
        Reset your password
      </h2>
      <p class="mt-2 text-sm text-[var(--text-muted)]">
        We'll send you an email containing instructions on how to set a new password.
      </p>
    </div>

    <form class="mt-8 space-y-4" onsubmit={handleReset}>
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

      <Button
        type="submit"
        disabled={loading}
        class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3 mt-6"
      >
        {loading ? 'Sending link...' : 'Send reset link'}
      </Button>

      <div class="text-center mt-4">
        <a href="/auth/login" class="text-xs font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline">
          Back to sign in
        </a>
      </div>
    </form>
  </div>
</div>
