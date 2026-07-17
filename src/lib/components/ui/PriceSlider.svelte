<script lang="ts">
  let { min = $bindable(200), max = $bindable(20000), rangeMin = 200, rangeMax = 20000, onchange } = $props<{
    min: number;
    max: number;
    rangeMin?: number;
    rangeMax?: number;
    onchange?: (min: number, max: number) => void;
  }>();

  let sliderRef = $state<HTMLDivElement | null>(null);
  let activeHandle = $state<'min' | 'max' | null>(null);

  function getPercentage(value: number) {
    return ((value - rangeMin) / (rangeMax - rangeMin)) * 100;
  }

  function handleTrackClick(e: MouseEvent) {
    if (!sliderRef) return;
    const rect = sliderRef.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const percentage = Math.max(0, Math.min(100, (clickX / rect.width) * 100));
    const value = Math.round(rangeMin + (percentage / 100) * (rangeMax - rangeMin));

    // Determine which handle is closer
    if (Math.abs(value - min) < Math.abs(value - max)) {
      min = Math.min(value, max - 100);
    } else {
      max = Math.max(value, min + 100);
    }
    onchange?.(min, max);
  }

  function handleStart(handle: 'min' | 'max') {
    activeHandle = handle;
  }

  function handleMove(clientX: number) {
    if (!activeHandle || !sliderRef) return;
    const rect = sliderRef.getBoundingClientRect();
    const relativeX = clientX - rect.left;
    const percentage = Math.max(0, Math.min(100, (relativeX / rect.width) * 100));
    let value = Math.round(rangeMin + (percentage / 100) * (rangeMax - rangeMin));

    // Round to nearest 50 or 100 for smoother increments
    value = Math.round(value / 50) * 50;
    value = Math.max(rangeMin, Math.min(rangeMax, value));

    if (activeHandle === 'min') {
      min = Math.min(value, max - 100);
    } else {
      max = Math.max(value, min + 100);
    }
  }

  function handleMouseMove(e: MouseEvent) {
    if (activeHandle) {
      handleMove(e.clientX);
    }
  }

  function handleTouchMove(e: TouchEvent) {
    if (activeHandle && e.touches.length > 0) {
      handleMove(e.touches[0].clientX);
    }
  }

  function handleEnd() {
    if (activeHandle) {
      activeHandle = null;
      onchange?.(min, max);
    }
  }
</script>

<svelte:window 
  onmousemove={handleMouseMove} 
  onmouseup={handleEnd}
  ontouchmove={handleTouchMove}
  ontouchend={handleEnd}
/>

<div class="space-y-4">
  <div class="flex justify-between text-xs text-[var(--text-secondary)] font-semibold">
    <span>Min: ৳{min}</span>
    <span>Max: ৳{max}</span>
  </div>

  <div 
    bind:this={sliderRef}
    class="relative h-2 w-full rounded-full bg-gray-200 dark:bg-gray-800 cursor-pointer select-none"
    onclick={handleTrackClick}
  >
    <!-- Highlighted Track -->
    <div 
      class="absolute h-full rounded-full bg-burgundy-700 dark:bg-gold-500"
      style="left: {getPercentage(min)}%; right: {100 - getPercentage(max)}%"
    ></div>

    <!-- Min Handle -->
    <button
      type="button"
      class="absolute top-1/2 h-5 w-5 -translate-y-1/2 -translate-x-1/2 rounded-full border-2 border-burgundy-700 bg-white dark:border-gold-500 dark:bg-gray-900 shadow-md focus:outline-none cursor-grab active:cursor-grabbing"
      style="left: {getPercentage(min)}%"
      onmousedown={() => handleStart('min')}
      ontouchstart={() => handleStart('min')}
      aria-label="Minimum price handle"
    ></button>

    <!-- Max Handle -->
    <button
      type="button"
      class="absolute top-1/2 h-5 w-5 -translate-y-1/2 -translate-x-1/2 rounded-full border-2 border-burgundy-700 bg-white dark:border-gold-500 dark:bg-gray-900 shadow-md focus:outline-none cursor-grab active:cursor-grabbing"
      style="left: {getPercentage(max)}%"
      onmousedown={() => handleStart('max')}
      ontouchstart={() => handleStart('max')}
      aria-label="Maximum price handle"
    ></button>
  </div>
</div>
