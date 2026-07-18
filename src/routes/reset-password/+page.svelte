<script lang="ts">
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { toast } from 'svelte-sonner';
  import { enhance } from '$app/forms';
  import { goto } from '$app/navigation';
  import { Eye, EyeOff, Check, X, AlertTriangle, Lock } from '@lucide/svelte';
  import type { PageData, ActionData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let password = $state('');
  let confirmPassword = $state('');
  let showPassword = $state(false);
  let showConfirmPassword = $state(false);
  let loading = $state(false);
  let resetSuccess = $state(false);

  // Live password validation rules
  let hasMinLength = $derived(password.length >= 8);
  let hasUppercase = $derived(/[A-Z]/.test(password));
  let hasLowercase = $derived(/[a-z]/.test(password));
  let hasNumber = $derived(/[0-9]/.test(password));
  let hasSpecialChar = $derived(/[^A-Za-z0-9]/.test(password));
  let passwordsMatch = $derived(password === confirmPassword && password !== '');

  let isFormValid = $derived(
    hasMinLength &&
    hasUppercase &&
    hasLowercase &&
    hasNumber &&
    hasSpecialChar &&
    passwordsMatch
  );
</script>

<svelte:head>
  <title>Reset Password</title>
</svelte:head>

<div class="flex min-h-[80vh] items-center justify-center bg-[var(--bg-secondary)] px-4 py-12">
  <div class="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-xl dark:bg-gray-950 border border-gray-100 dark:border-gray-900">
    <!-- Branding Header -->
    <div class="text-center">
      <img src="/logo.jpg" alt="PerfumeDecantsBD" class="mx-auto h-16 w-16 rounded-full object-cover" />
      
      {#if !data.valid}
        <h2 class="font-heading mt-6 text-3xl font-bold tracking-tight text-burgundy-950 dark:text-cream-200">
          Invalid Reset Link
        </h2>
        <p class="mt-2 text-sm text-[var(--text-muted)] leading-relaxed">
          This password reset link is invalid or has expired. Please request a new link to reset your password.
        </p>
      {:else if resetSuccess}
        <h2 class="font-heading mt-6 text-3xl font-bold tracking-tight text-green-600 dark:text-green-400">
          Password Updated
        </h2>
        <p class="mt-2 text-sm text-[var(--text-muted)] leading-relaxed">
          Your password has been successfully updated. You can now sign in with your new password.
        </p>
      {:else}
        <h2 class="font-heading mt-6 text-3xl font-bold tracking-tight text-burgundy-950 dark:text-cream-200">
          Reset Password
        </h2>
        <p class="mt-2 text-sm text-[var(--text-muted)] leading-relaxed">
          Choose a secure, strong new password for your account below.
        </p>
      {/if}
    </div>

    {#if !data.valid}
      <!-- Invalid Session View -->
      <div class="space-y-4 pt-4">
        <div class="flex items-center gap-3 rounded-xl bg-red-50 border border-red-200/50 p-4 dark:bg-red-950/15 dark:border-red-900/30 text-red-800 dark:text-red-300">
          <AlertTriangle class="h-5 w-5 shrink-0 text-red-650 dark:text-red-400" />
          <span class="text-xs font-semibold">Verification link has expired or has already been used.</span>
        </div>
        
        <a href="/auth/forgot-password" class="block w-full">
          <Button class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3 mt-2">
            Request New Reset Link
          </Button>
        </a>
        
        <div class="text-center">
          <a href="/auth/login" class="text-xs font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline">
            Back to sign in
          </a>
        </div>
      </div>
    {:else if resetSuccess}
      <!-- Success Redirecting View -->
      <div class="space-y-6 pt-6 text-center">
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-950/50 text-green-600 dark:text-green-400 animate-scale-in">
          <Check class="h-6 w-6" />
        </div>
        <p class="text-xs text-[var(--text-muted)] animate-pulse">Redirecting you to sign in page...</p>
        
        <a href="/auth/login" class="block w-full">
          <Button class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3">
            Go to Login Now
          </Button>
        </a>
      </div>
    {:else}
      <!-- Reset Form View -->
      <form
        method="POST"
        action="?/resetPassword"
        use:enhance={() => {
          loading = true;
          return async ({ result }) => {
            loading = false;
            if (result.type === 'success') {
              toast.success('Password successfully reset!');
              resetSuccess = true;
              setTimeout(() => {
                goto('/auth/login');
              }, 2000);
            } else if (result.type === 'failure') {
              const msg = (result.data as any)?.message || 'Failed to reset password';
              toast.error(msg);
            }
          };
        }}
        class="mt-8 space-y-5"
      >
        <!-- New Password Field -->
        <div class="space-y-1">
          <label for="password" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">New Password</label>
          <div class="relative">
            <Input
              id="password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              required
              placeholder="••••••••"
              bind:value={password}
              class="pr-10"
            />
            <button
              type="button"
              onclick={() => (showPassword = !showPassword)}
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {#if showPassword}
                <EyeOff class="h-4 w-4" />
              {:else}
                <Eye class="h-4 w-4" />
              {/if}
            </button>
          </div>
        </div>

        <!-- Confirm Password Field -->
        <div class="space-y-1">
          <label for="confirmPassword" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Confirm Password</label>
          <div class="relative">
            <Input
              id="confirmPassword"
              name="confirmPassword"
              type={showConfirmPassword ? 'text' : 'password'}
              required
              placeholder="••••••••"
              bind:value={confirmPassword}
              class="pr-10"
            />
            <button
              type="button"
              onclick={() => (showConfirmPassword = !showConfirmPassword)}
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
            >
              {#if showConfirmPassword}
                <EyeOff class="h-4 w-4" />
              {:else}
                <Eye class="h-4 w-4" />
              {/if}
            </button>
          </div>
        </div>

        <!-- Live Password Strength Criteria Indicators -->
        <div class="rounded-xl bg-gray-50 dark:bg-gray-900/50 p-4 border border-gray-100 dark:border-gray-900 text-[11px] space-y-2 text-[var(--text-secondary)]">
          <p class="font-bold text-gray-800 dark:text-cream-300 text-xs">Password Requirements:</p>
          
          <div class="grid grid-cols-2 gap-x-2 gap-y-1.5">
            <div class="flex items-center gap-1.5 {hasMinLength ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-600'}">
              {#if hasMinLength}
                <Check class="h-3.5 w-3.5" />
              {:else}
                <X class="h-3.5 w-3.5" />
              {/if}
              <span>Min 8 characters</span>
            </div>

            <div class="flex items-center gap-1.5 {hasUppercase ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-600'}">
              {#if hasUppercase}
                <Check class="h-3.5 w-3.5" />
              {:else}
                <X class="h-3.5 w-3.5" />
              {/if}
              <span>One uppercase letter</span>
            </div>

            <div class="flex items-center gap-1.5 {hasLowercase ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-600'}">
              {#if hasLowercase}
                <Check class="h-3.5 w-3.5" />
              {:else}
                <X class="h-3.5 w-3.5" />
              {/if}
              <span>One lowercase letter</span>
            </div>

            <div class="flex items-center gap-1.5 {hasNumber ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-600'}">
              {#if hasNumber}
                <Check class="h-3.5 w-3.5" />
              {:else}
                <X class="h-3.5 w-3.5" />
              {/if}
              <span>One number (0-9)</span>
            </div>

            <div class="flex items-center gap-1.5 {hasSpecialChar ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-600'}">
              {#if hasSpecialChar}
                <Check class="h-3.5 w-3.5" />
              {:else}
                <X class="h-3.5 w-3.5" />
              {/if}
              <span>One special character</span>
            </div>

            <div class="flex items-center gap-1.5 {passwordsMatch ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-600'}">
              {#if passwordsMatch}
                <Check class="h-3.5 w-3.5" />
              {:else}
                <X class="h-3.5 w-3.5" />
              {/if}
              <span>Passwords match</span>
            </div>
          </div>
        </div>

        <!-- Submission Buttons -->
        <Button
          type="submit"
          disabled={loading || !isFormValid}
          class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3 mt-6"
        >
          {loading ? 'Updating password...' : 'Update Password'}
        </Button>

        <div class="text-center mt-4">
          <a href="/auth/login" class="text-xs font-semibold text-burgundy-700 hover:text-burgundy-800 dark:text-gold-400 underline">
            Cancel and back to sign in
          </a>
        </div>
      </form>
    {/if}
  </div>
</div>
