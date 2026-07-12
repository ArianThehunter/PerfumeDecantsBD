<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { createSupabaseClient } from '$lib/supabase';
  import { User, ShoppingBag, MapPin, LogOut } from '@lucide/svelte';
  import { toast } from 'svelte-sonner';

  let { children } = $props();

  // Initialize supabase browser client
  const supabase = createSupabaseClient(fetch);

  const accountLinks = [
    { href: '/account', label: 'My Profile', icon: User },
    { href: '/account/orders', label: 'Order History', icon: ShoppingBag },
    { href: '/account/addresses', label: 'Saved Addresses', icon: MapPin }
  ];

  async function handleLogout() {
    const { error } = await supabase.auth.signOut();
    if (error) {
      toast.error('Failed to log out');
    } else {
      toast.success('Logged out successfully');
      goto('/', { invalidateAll: true });
    }
  }
</script>

<div class="bg-[var(--bg-secondary)] py-10 min-h-[80vh]">
  <div class="container-luxury">
    <div class="grid gap-8 lg:grid-cols-[280px_1fr]">
      <!-- Account Navigation Sidebar -->
      <aside class="space-y-4">
        <div class="card-premium p-6 text-center space-y-4">
          <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-burgundy-100 font-heading text-2xl font-bold text-burgundy-700 dark:bg-burgundy-900 dark:text-gold-400">
            {page.data.user?.email?.[0].toUpperCase() || 'U'}
          </div>
          <div>
            <h2 class="font-heading text-lg font-bold">{page.data.user?.email}</h2>
            <p class="text-xs text-[var(--text-muted)] uppercase tracking-wider">Customer Account</p>
          </div>
        </div>

        <nav class="card-premium overflow-hidden p-2 space-y-1">
          {#each accountLinks as link}
            {@const Icon = link.icon}
            <a
              href={link.href}
              class="flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-semibold transition-all {page.url.pathname === link.href 
                ? 'bg-burgundy-700 text-white dark:bg-gold-500 dark:text-burgundy-950' 
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-900'}"
            >
              <Icon class="h-4.5 w-4.5" />
              {link.label}
            </a>
          {/each}

          <button
            onclick={handleLogout}
            class="w-full flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-semibold text-red-600 hover:bg-red-50 dark:hover:bg-red-950/20 transition-all text-left"
          >
            <LogOut class="h-4.5 w-4.5" />
            Logout
          </button>
        </nav>
      </aside>

      <!-- Account Panel Content -->
      <main class="card-premium p-6 md:p-8 bg-white dark:bg-gray-950">
        {@render children()}
      </main>
    </div>
  </div>
</div>
