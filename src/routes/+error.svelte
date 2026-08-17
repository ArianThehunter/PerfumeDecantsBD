<script lang="ts">
  import { page } from '$app/state';
  import { Button } from '$lib/components/ui/button';
  import { Compass, House as Home, MessageSquare } from '@lucide/svelte';

  const status = $derived(page.status);
  const error = $derived(page.error as any);

  const title = $derived.by(() => {
    if (status === 404) return 'Fragrance Not Found';
    if (status === 403) return 'Access Restricted';
    if (status === 500) return 'Internal Essence Error';
    return 'Unexpected Scent Trail';
  });

  const description = $derived.by(() => {
    if (status === 404) {
      return 'The bespoke bottle, decant, or page you are seeking seems to have evaporated into thin air.';
    }
    if (status === 403) {
      return 'You do not have the required administrative credentials to access this fragrance sanctum.';
    }
    if (status === 500) {
      return 'Our servers encountered an unexpected issue while blending this request. Our team has been notified.';
    }
    return error?.message || 'An unexpected error occurred while loading this page. Please try again.';
  });
</script>

<svelte:head>
  <title>{status} — {title} | PerfumeDecantsBD</title>
</svelte:head>

<div class="min-h-[70vh] flex items-center justify-center px-4 py-16">
  <div class="max-w-xl w-full text-center space-y-8 p-8 md:p-12 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-2xl backdrop-blur-md relative overflow-hidden">
    <!-- Ambient glow decorative element -->
    <div class="absolute -top-24 -left-24 w-48 h-48 bg-burgundy-500/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-24 -right-24 w-48 h-48 bg-gold-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="space-y-3 relative">
      <span class="inline-block text-6xl md:text-7xl font-serif font-black tracking-tight text-burgundy-700 dark:text-gold-500">
        {status}
      </span>
      <h1 class="text-2xl md:text-3xl font-serif font-bold text-[var(--text-primary)]">
        {title}
      </h1>
      <p class="text-sm md:text-base text-[var(--text-secondary)] leading-relaxed max-w-md mx-auto">
        {description}
      </p>
      {#if error?.errorId}
        <div class="inline-block mt-2 px-3 py-1 text-xs font-mono rounded bg-[var(--bg-card-hover)] text-[var(--text-muted)] border border-[var(--border-subtle)]">
          Reference Code: {error.errorId}
        </div>
      {/if}
    </div>

    <!-- Recovery Navigation Actions -->
    <div class="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4 border-t border-[var(--border-subtle)] relative">
      <Button href="/" variant="default" class="w-full sm:w-auto flex items-center justify-center gap-2">
        <Home class="w-4 h-4" />
        Return Home
      </Button>

      <Button href="/shop" variant="outline" class="w-full sm:w-auto flex items-center justify-center gap-2">
        <Compass class="w-4 h-4" />
        Explore Shop
      </Button>

      <Button href="/contact" variant="ghost" class="w-full sm:w-auto flex items-center justify-center gap-2">
        <MessageSquare class="w-4 h-4" />
        Contact Concierge
      </Button>
    </div>
  </div>
</div>
