<script lang="ts">
  import { enhance } from '$app/forms';
  import { page } from '$app/state';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { toast } from 'svelte-sonner';
  import type { ActionData, PageData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let profile = $derived(data.profile);
  let loading = $state(false);

  let phoneValue = $state(profile?.phone || '');
  let fullNameValue = $state(profile?.full_name || '');

  // Phone validation
  let phoneValid = $derived(/^01\d{9}$/.test(phoneValue));
  let phoneTouched = $state(false);
  let phoneError = $derived.by(() => {
    if (!phoneTouched || phoneValue === '') return '';
    if (!/^\d+$/.test(phoneValue)) return 'Only numbers are allowed.';
    if (!phoneValue.startsWith('01')) return 'Must start with 01.';
    if (phoneValue.length !== 11) return 'Must be exactly 11 digits.';
    return '';
  });

  $effect(() => {
    if (form?.success) {
      toast.success('Profile updated successfully');
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<svelte:head>
  <title>Customer Dashboard</title>
</svelte:head>

<div class="space-y-6">
  <div>
    <h2 class="font-heading text-2xl font-bold">Account Profile</h2>
    <p class="text-sm text-[var(--text-muted)]">Update your basic account credentials and contact details.</p>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <form
    method="post"
    action="?/updateProfile"
    use:enhance={() => {
      loading = true;
      return async ({ update }) => {
        loading = false;
        await update();
      };
    }}
    class="space-y-4 max-w-xl"
  >
    <div class="space-y-1">
      <label for="email" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Email Address</label>
      <Input
        id="email"
        type="email"
        value={page.data.user?.email}
        disabled
        class="bg-gray-50 dark:bg-gray-900 cursor-not-allowed"
      />
      <span class="text-[10px] text-[var(--text-muted)]">Email cannot be changed after registration.</span>
    </div>

    <div class="space-y-1">
      <label for="fullName" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Full Name</label>
      <Input
        id="fullName"
        name="fullName"
        type="text"
        required
        bind:value={fullNameValue}
        placeholder="Enter your full name"
      />
    </div>

    <div class="space-y-1">
      <label for="phone" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">
        Phone Number <span class="text-red-500">*</span>
      </label>
      <Input
        id="phone"
        name="phone"
        type="tel"
        required
        bind:value={phoneValue}
        oninput={() => { phoneTouched = true; }}
        placeholder="01XXXXXXXXX"
      />
      {#if phoneError}
        <p class="text-[10px] text-red-500 font-semibold mt-0.5">{phoneError}</p>
      {:else if phoneTouched && phoneValid}
        <p class="text-[10px] text-green-600 dark:text-green-400 font-semibold mt-0.5">✓ Valid phone number</p>
      {:else}
        <p class="text-[10px] text-[var(--text-muted)] mt-0.5">Must be 11 digits, starting with 01.</p>
      {/if}
    </div>

    <Button
      type="submit"
      disabled={loading || !phoneValid || !fullNameValue.trim()}
      class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold rounded-xl px-6 py-2.5"
    >
      {loading ? 'Saving Changes...' : 'Save Profile'}
    </Button>
  </form>
</div>
