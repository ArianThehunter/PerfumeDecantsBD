<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { createSupabaseClient } from '$lib/supabase';
  import { LayoutDashboard, ShoppingBag, FolderHeart, FileSpreadsheet, Home, LogOut, Sun, Moon, Settings, Mail } from '@lucide/svelte';
  import { theme } from '$lib/stores/theme.svelte';
  import { toast } from 'svelte-sonner';

  let { children } = $props();

  const supabase = createSupabaseClient(fetch);

  const sidebarLinks = [
    { href: '/admin', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/admin/products', label: 'Products', icon: ShoppingBag },
    { href: '/admin/categories', label: 'Categories', icon: FolderHeart },
    { href: '/admin/orders', label: 'Orders', icon: FileSpreadsheet },
    { href: '/admin/contact-messages', label: 'Contact Messages', icon: Mail },
    { href: '/admin/settings', label: 'Settings', icon: Settings }
  ];

  async function handleLogout() {
    const { error } = await supabase.auth.signOut();
    if (error) {
      toast.error('Logout failed');
    } else {
      toast.success('Logged out successfully');
      goto('/', { invalidateAll: true });
    }
  }
</script>

<svelte:head>
  <title>Admin Dashboard — PerfumeDecantsBD</title>
</svelte:head>

<div class="min-h-screen bg-[var(--bg-secondary)] flex flex-col lg:flex-row">
  <!-- Sidebar -->
  <aside class="w-full lg:w-64 shrink-0 bg-burgundy-950 text-cream-100 flex flex-col justify-between border-r border-burgundy-900">
    <div>
      <!-- Brand Header -->
      <div class="h-16 lg:h-20 flex items-center gap-3 px-6 border-b border-burgundy-900">
        <img src="/logo.jpg" alt="Logo" class="h-9 w-9 rounded-full object-cover" />
        <div>
          <span class="font-heading text-base font-bold text-white block">Decants Admin</span>
          <span class="text-[10px] text-gold-400 tracking-widest uppercase">PerfumeDecantsBD</span>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="p-4 space-y-1.5 flex flex-row lg:flex-col overflow-x-auto lg:overflow-x-visible">
        {#each sidebarLinks as link}
          {@const Icon = link.icon}
          <a
            href={link.href}
            class="flex items-center gap-3 rounded-lg px-4 py-2.5 text-xs lg:text-sm font-semibold transition-all shrink-0 {page.url.pathname === link.href 
              ? 'bg-gold-500 text-burgundy-950 font-bold' 
              : 'text-cream-300/80 hover:bg-burgundy-900/60 hover:text-white'}"
          >
            <Icon class="h-4.5 w-4.5" />
            {link.label}
          </a>
        {/each}
      </nav>
    </div>

    <!-- Bottom Actions -->
    <div class="p-4 border-t border-burgundy-900 hidden lg:block space-y-2">
      <!-- Dark mode switch -->
      <button
        onclick={() => theme.toggle()}
        class="w-full flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-semibold text-cream-300/85 hover:bg-burgundy-900/50 transition-all text-left"
      >
        {#if theme.isDark}
          <Sun class="h-4.5 w-4.5" />
          Light Mode
        {:else}
          <Moon class="h-4.5 w-4.5" />
          Dark Mode
        {/if}
      </button>

      <!-- Store View link -->
      <a
        href="/"
        class="w-full flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-semibold text-cream-300/85 hover:bg-burgundy-900/50 transition-all"
      >
        <Home class="h-4.5 w-4.5" />
        Back to Store
      </a>

      <!-- Logout -->
      <button
        onclick={handleLogout}
        class="w-full flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-semibold text-red-400 hover:bg-red-950/20 transition-all text-left"
      >
        <LogOut class="h-4.5 w-4.5" />
        Logout
      </button>
    </div>
  </aside>

  <!-- Main panel -->
  <div class="flex-1 flex flex-col min-w-0">
    <!-- Top Bar -->
    <header class="h-16 bg-white dark:bg-gray-950 border-b flex items-center justify-between px-6 shrink-0">
      <h2 class="font-heading text-lg font-bold">Atelier Dashboard</h2>
      <div class="flex items-center gap-4">
        <span class="text-xs font-semibold bg-gold-100 dark:bg-gold-950 text-gold-800 dark:text-gold-400 rounded-full px-3 py-1 uppercase tracking-wider">
          Admin Session
        </span>
        <div class="h-8 w-8 rounded-full bg-burgundy-700 text-white font-heading font-bold flex items-center justify-center text-xs">
          A
        </div>
      </div>
    </header>

    <!-- Page children content -->
    <main class="flex-1 overflow-y-auto p-6 lg:p-8">
      {@render children()}
    </main>
  </div>
</div>
