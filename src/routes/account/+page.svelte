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

  $effect(() => {
    if (form?.success) {
      toast.success('Profile updated successfully');
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

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
        value={profile?.full_name || ''}
        placeholder="Enter your full name"
      />
    </div>

    <div class="space-y-1">
      <label for="phone" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Phone Number</label>
      <Input
        id="phone"
        name="phone"
        type="tel"
        value={profile?.phone || ''}
        placeholder="+880 1XXX-XXXXXX"
      />
    </div>

    <Button
      type="submit"
      disabled={loading}
      class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold rounded-xl px-6 py-2.5"
    >
      {loading ? 'Saving Changes...' : 'Save Profile'}
    </Button>
  </form>
</div>
