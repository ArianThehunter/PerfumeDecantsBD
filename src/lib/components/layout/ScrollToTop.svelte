<script lang="ts">
  import { ArrowUp } from '@lucide/svelte';

  let visible = $state(false);

  function handleScroll() {
    visible = window.scrollY > 400;
  }

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
</script>

<svelte:window onscroll={handleScroll} />

{#if visible}
  <button
    onclick={scrollToTop}
    class="fixed bottom-6 right-6 z-40 flex h-11 w-11 items-center justify-center rounded-full bg-burgundy-700 text-white shadow-lg transition-all hover:bg-burgundy-800 hover:shadow-xl animate-scale-in btn-press"
    aria-label="Scroll to top"
  >
    <ArrowUp class="h-5 w-5" />
  </button>
{/if}
