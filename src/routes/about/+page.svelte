<script lang="ts">
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  // Dynamic Settings
  const s = $derived(data.aboutSettings || {});
  const title = $derived(s.title || 'Maison de Fragrance');
  const subtitle = $derived(s.subtitle || 'Bridging the gap between perfume enthusiasts and authentic luxury experiences.');
  const storyTitle = $derived(s.story_title || 'Our Fragrant Narrative');
  const storyContent1 = $derived(s.story_content_1 || 'PerfumeDecantsBD started from a simple, personal aspiration: the love for fine fragrances and the frustration of full-bottle commitments. We recognized that buying an expensive designer or niche bottle is a huge investment, especially when you are unsure if the scent suits your skin chemistry or personal lifestyle.');
  const storyContent2 = $derived(s.story_content_2 || 'Our goal is to curate a library of authentic fragrances that can be sampled, explored, and worn before committing to a full luxury bottle. Every decant we assemble is handled with professional tools, clean procedures, and housed in high-quality spray atomizers that protect the juice inside.');
  const mission = $derived(s.mission || 'To provide fragrance enthusiasts in Bangladesh access to premium, authentic luxury and niche perfumes through accessible decant sizes. We guarantee authenticity, premium customer experience, and expert guidance.');
  const vision = $derived(s.vision || 'To become the most trusted and curated marketplace in Bangladesh for luxury fragrance discovery, offering an educational journey of perfume notes, skin chemistry, and signature scent profile creation.');
  const imageUrl = $derived(s.image_url || 'https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?w=800&fit=crop');
</script>

<svelte:head>
  <title>{title} — About Us | PerfumeDecantsBD</title>
</svelte:head>

<div class="bg-[var(--bg-primary)]">
  <!-- Page Hero -->
  <section class="relative min-h-[40vh] overflow-hidden bg-burgundy-950 flex items-center">
    <div class="absolute inset-0">
      <img src="/cover.png" alt="" class="h-full w-full object-cover opacity-15" />
      <div class="absolute inset-0 bg-gradient-to-t from-burgundy-950 to-transparent"></div>
    </div>
    <div class="container-luxury relative z-10 py-16 text-center text-white">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-400">About Us</span>
      <h1 class="font-heading mt-4 text-4xl font-bold lg:text-5xl">{title}</h1>
      <p class="mx-auto mt-4 max-w-lg text-sm text-cream-300/70">
        {subtitle}
      </p>
    </div>
  </section>

  <!-- Content Section -->
  <section class="section-padding">
    <div class="container-luxury">
      <div class="grid gap-12 lg:grid-cols-2 lg:items-center">
        <!-- Story Text -->
        <div class="space-y-6">
          <span class="text-xs font-semibold uppercase tracking-widest text-gold-500">The Beginning</span>
          <h2 class="font-heading text-3xl font-bold text-burgundy-950 dark:text-cream-200">{storyTitle}</h2>
          <p class="text-sm leading-relaxed text-[var(--text-secondary)]">
            {storyContent1}
          </p>
          <p class="text-sm leading-relaxed text-[var(--text-secondary)]">
            {storyContent2}
          </p>
        </div>

        <!-- Visual Image -->
        <div class="aspect-video overflow-hidden rounded-2xl bg-gray-150 shadow-lg lg:aspect-square">
          <img
            src={imageUrl}
            alt="Maison de Perfume Decants"
            class="h-full w-full object-cover"
            loading="lazy"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Mission & Vision -->
  <section class="section-padding bg-[var(--bg-secondary)]">
    <div class="container-luxury">
      <div class="grid gap-8 md:grid-cols-2">
        <div class="card-premium p-8 space-y-4">
          <h3 class="font-heading text-xl font-bold text-burgundy-900 dark:text-gold-400">Our Mission</h3>
          <p class="text-sm leading-relaxed text-[var(--text-secondary)]">
            {mission}
          </p>
        </div>
        <div class="card-premium p-8 space-y-4">
          <h3 class="font-heading text-xl font-bold text-burgundy-900 dark:text-gold-400">Our Vision</h3>
          <p class="text-sm leading-relaxed text-[var(--text-secondary)]">
            {vision}
          </p>
        </div>
      </div>
    </div>
  </section>
</div>
