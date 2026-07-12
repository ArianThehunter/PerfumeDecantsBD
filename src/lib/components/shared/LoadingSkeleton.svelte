<script lang="ts">
  let { count = 4, layout = 'grid' } = $props<{ count?: number; layout?: 'grid' | 'list' | 'detail' }>();
</script>

{#if layout === 'grid'}
  <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
    {#each Array(count) as _}
      <div class="card-premium overflow-hidden">
        <div class="aspect-[4/5] w-full skeleton"></div>
        <div class="space-y-3 p-4">
          <div class="h-3 w-1/4 skeleton"></div>
          <div class="h-5 w-3/4 skeleton"></div>
          <div class="h-3 w-1/2 skeleton"></div>
          <div class="flex items-center justify-between pt-2">
            <div class="h-6 w-1/3 skeleton"></div>
          </div>
        </div>
      </div>
    {/each}
  </div>
{:else if layout === 'list'}
  <div class="space-y-4">
    {#each Array(count) as _}
      <div class="flex gap-4 rounded-xl border p-4">
        <div class="h-24 w-24 shrink-0 rounded-lg skeleton"></div>
        <div class="flex-1 space-y-3 py-1">
          <div class="h-4 w-1/3 skeleton"></div>
          <div class="h-6 w-3/4 skeleton"></div>
          <div class="h-4 w-1/2 skeleton"></div>
        </div>
      </div>
    {/each}
  </div>
{:else if layout === 'detail'}
  <div class="grid gap-8 lg:grid-cols-2">
    <!-- Image Gallery Skeleton -->
    <div class="space-y-4">
      <div class="aspect-square w-full rounded-2xl skeleton"></div>
      <div class="flex gap-3">
        {#each Array(4) as _}
          <div class="aspect-square w-20 rounded-xl skeleton"></div>
        {/each}
      </div>
    </div>
    <!-- Info Skeleton -->
    <div class="space-y-6">
      <div class="space-y-2">
        <div class="h-4 w-20 skeleton"></div>
        <div class="h-10 w-3/4 skeleton"></div>
        <div class="h-4 w-1/4 skeleton"></div>
      </div>
      <div class="h-8 w-1/3 skeleton"></div>
      <div class="space-y-2 pt-4">
        <div class="h-4 w-full skeleton"></div>
        <div class="h-4 w-full skeleton"></div>
        <div class="h-4 w-3/4 skeleton"></div>
      </div>
      <!-- Sizes -->
      <div class="space-y-2 pt-4">
        <div class="h-4 w-16 skeleton"></div>
        <div class="flex gap-3">
          <div class="h-10 w-20 rounded-lg skeleton"></div>
          <div class="h-10 w-20 rounded-lg skeleton"></div>
          <div class="h-10 w-20 rounded-lg skeleton"></div>
        </div>
      </div>
      <!-- Add to Cart -->
      <div class="flex gap-4 pt-6">
        <div class="h-12 w-24 rounded-xl skeleton"></div>
        <div class="h-12 flex-1 rounded-xl skeleton"></div>
      </div>
    </div>
  </div>
{/if}
