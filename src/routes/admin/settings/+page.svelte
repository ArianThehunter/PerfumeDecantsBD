<script lang="ts">
  import { enhance } from '$app/forms';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import { Textarea } from '$lib/components/ui/textarea';
  import { toast } from 'svelte-sonner';
  import type { PageData, ActionData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  let settings = $derived(data.settings);
  let activeTab = $state<'footer' | 'about' | 'contact' | 'shop' | 'hero'>('footer');
  let loading = $state(false);
  let selectedHeroProductIds = $state<string[]>([]);

  $effect(() => {
    if (data.settings?.hero_slides?.product_ids) {
      selectedHeroProductIds = [...data.settings.hero_slides.product_ids];
    }
  });

  $effect(() => {
    if (form?.success) {
      toast.success('Site settings updated successfully');
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<svelte:head>
  <title>Manage Site Settings — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-6">
  <div>
    <h1 class="font-heading text-2xl font-bold">Dynamic Site Settings</h1>
    <p class="text-xs text-[var(--text-muted)]">Customize navigation text, contact details, story pages, and brand parameters.</p>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <!-- Tabs Navigation -->
  <div class="flex border-b border-gray-150 dark:border-gray-800">
    {#each [
      { key: 'footer', label: 'Footer & Brands' },
      { key: 'about', label: 'About Us Page' },
      { key: 'contact', label: 'Contact Us Page' },
      { key: 'shop', label: 'Shop Page' },
      { key: 'hero', label: 'Hero Slider' }
    ] as tab}
      <button
        onclick={() => (activeTab = tab.key as any)}
        class="border-b-2 px-6 py-3.5 text-xs font-bold uppercase tracking-wider transition-all {activeTab === tab.key 
          ? 'border-burgundy-700 text-burgundy-800 dark:border-gold-500 dark:text-gold-400' 
          : 'border-transparent text-gray-500 hover:text-burgundy-700'}"
      >
        {tab.label}
      </button>
    {/each}
  </div>

  <div class="py-4">
    <!-- Footer settings -->
    {#if activeTab === 'footer'}
      {@const f = settings.footer || {}}
      <form
        method="post"
        action="?/updateFooter"
        use:enhance={() => {
          loading = true;
          return async ({ update }) => {
            loading = false;
            await update();
          };
        }}
        class="space-y-4 max-w-2xl"
      >
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1">
            <label for="newsletter_title" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Newsletter Title</label>
            <Input id="newsletter_title" name="newsletter_title" type="text" value={f.newsletter_title} required />
          </div>
          <div class="space-y-1">
            <label for="newsletter_desc" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Newsletter Description</label>
            <Input id="newsletter_desc" name="newsletter_desc" type="text" value={f.newsletter_desc} required />
          </div>
        </div>

        <div class="space-y-1">
          <label for="brand_desc" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Brand Description</label>
          <Textarea id="brand_desc" name="brand_desc" rows={3} value={f.brand_desc} required />
        </div>

        <div class="grid grid-cols-3 gap-4">
          <div class="space-y-1">
            <label for="facebook_url" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Facebook Link</label>
            <Input id="facebook_url" name="facebook_url" type="url" value={f.facebook_url} />
          </div>
          <div class="space-y-1">
            <label for="instagram_url" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Instagram Link</label>
            <Input id="instagram_url" name="instagram_url" type="url" value={f.instagram_url} />
          </div>
          <div class="space-y-1">
            <label for="telegram_url" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Telegram Link</label>
            <Input id="telegram_url" name="telegram_url" type="url" value={f.telegram_url} />
          </div>
        </div>

        <div class="grid grid-cols-3 gap-4">
          <div class="space-y-1">
            <label for="address" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Atelier Address</label>
            <Input id="address" name="address" type="text" value={f.address} required />
          </div>
          <div class="space-y-1">
            <label for="phone" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Phone Number</label>
            <Input id="phone" name="phone" type="text" value={f.phone} required />
          </div>
          <div class="space-y-1">
            <label for="email" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Email Address</label>
            <Input id="email" name="email" type="email" value={f.email} required />
          </div>
        </div>

        <div class="space-y-1">
          <label for="copyright" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Copyright Label</label>
          <Input id="copyright" name="copyright" type="text" value={f.copyright} required />
        </div>

        <div class="pt-4">
          <Button type="submit" disabled={loading} class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold">
            {loading ? 'Saving Settings...' : 'Save Layout Settings'}
          </Button>
        </div>
      </form>
    {/if}

    <!-- About Us Page settings -->
    {#if activeTab === 'about'}
      {@const a = settings.about_page || {}}
      <form
        method="post"
        action="?/updateAbout"
        use:enhance={() => {
          loading = true;
          return async ({ update }) => {
            loading = false;
            await update();
          };
        }}
        class="space-y-4 max-w-2xl"
      >
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1">
            <label for="about_title" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Banner Title</label>
            <Input id="about_title" name="title" type="text" value={a.title} required />
          </div>
          <div class="space-y-1">
            <label for="about_subtitle" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Banner Subtitle</label>
            <Input id="about_subtitle" name="subtitle" type="text" value={a.subtitle} required />
          </div>
        </div>

        <div class="space-y-1">
          <label for="story_title" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Story Header Title</label>
          <Input id="story_title" name="story_title" type="text" value={a.story_title} required />
        </div>

        <div class="space-y-1">
          <label for="story_content_1" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Story Paragraph 1</label>
          <Textarea id="story_content_1" name="story_content_1" rows={4} value={a.story_content_1} required />
        </div>

        <div class="space-y-1">
          <label for="story_content_2" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Story Paragraph 2</label>
          <Textarea id="story_content_2" name="story_content_2" rows={4} value={a.story_content_2} required />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1">
            <label for="mission" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Our Mission</label>
            <Textarea id="mission" name="mission" rows={3} value={a.mission} required />
          </div>
          <div class="space-y-1">
            <label for="vision" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Our Vision</label>
            <Textarea id="vision" name="vision" rows={3} value={a.vision} required />
          </div>
        </div>

        <div class="space-y-1">
          <label for="about_image_url" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Cover Image URL</label>
          <Input id="about_image_url" name="image_url" type="url" value={a.image_url} required />
        </div>

        <div class="pt-4">
          <Button type="submit" disabled={loading} class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold">
            {loading ? 'Saving Page Details...' : 'Save About Page'}
          </Button>
        </div>
      </form>
    {/if}

    <!-- Contact Page settings -->
    {#if activeTab === 'contact'}
      {@const c = settings.contact_page || {}}
      <form
        method="post"
        action="?/updateContact"
        use:enhance={() => {
          loading = true;
          return async ({ update }) => {
            loading = false;
            await update();
          };
        }}
        class="space-y-4 max-w-2xl"
      >
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1">
            <label for="contact_title" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Banner Title</label>
            <Input id="contact_title" name="title" type="text" value={c.title} required />
          </div>
          <div class="space-y-1">
            <label for="contact_subtitle" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Banner Subtitle</label>
            <Input id="contact_subtitle" name="subtitle" type="text" value={c.subtitle} required />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1">
            <label for="form_title" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Form Header Title</label>
            <Input id="form_title" name="form_title" type="text" value={c.form_title} required />
          </div>
          <div class="space-y-1">
            <label for="form_subtitle" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Form Subtitle</label>
            <Input id="form_subtitle" name="form_subtitle" type="text" value={c.form_subtitle} required />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1">
            <label for="contact_address" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Physical Address</label>
            <Input id="contact_address" name="address" type="text" value={c.address} required />
          </div>
          <div class="space-y-1">
            <label for="contact_phone" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Phone Number</label>
            <Input id="contact_phone" name="phone" type="text" value={c.phone} required />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1">
            <label for="contact_email" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Contact Email</label>
            <Input id="contact_email" name="email" type="email" value={c.email} required />
          </div>
          <div class="space-y-1">
            <label for="hours" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Business Hours</label>
            <Input id="hours" name="hours" type="text" value={c.hours} required />
          </div>
        </div>

        <div class="pt-4">
          <Button type="submit" disabled={loading} class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold">
            {loading ? 'Saving Page Details...' : 'Save Contact Page'}
          </Button>
        </div>
      </form>
    {/if}

    <!-- Shop Page settings -->
    {#if activeTab === 'shop'}
      {@const sh = settings.shop_page || {}}
      <form
        method="post"
        action="?/updateShop"
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
          <label for="shop_title" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Shop Page Header Title</label>
          <Input id="shop_title" name="title" type="text" value={sh.title} required />
        </div>
        <div class="space-y-1">
          <label for="shop_subtitle" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Shop Page Subtitle</label>
          <Input id="shop_subtitle" name="subtitle" type="text" value={sh.subtitle} required />
        </div>

        <div class="pt-4">
          <Button type="submit" disabled={loading} class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold">
            {loading ? 'Saving Shop Config...' : 'Save Shop Page'}
          </Button>
        </div>
      </form>
    {/if}

    <!-- Hero Slider settings -->
    {#if activeTab === 'hero'}
      {@const hs = settings.hero_slides || { product_ids: [] }}
      {@const allProducts = data.products || []}
      <form
        method="post"
        action="?/updateHeroSlides"
        use:enhance={() => {
          loading = true;
          return async ({ update }) => {
            loading = false;
            await update();
          };
        }}
        class="space-y-4 max-w-3xl"
      >
        <div class="space-y-4">
          <div>
            <h3 class="text-sm font-bold">Select Products for Hero Slider</h3>
            <p class="text-xs text-[var(--text-muted)] mt-1">Check the products you want to feature in the homepage animated hero slider.</p>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-3 gap-4 border border-gray-100 dark:border-gray-800 p-4 rounded-xl max-h-96 overflow-y-auto">
            {#each allProducts as product}
              <label class="flex items-start gap-3 p-3 rounded-lg border hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer {selectedHeroProductIds.includes(product.id) ? 'border-burgundy-500 bg-burgundy-50/30 dark:border-gold-500 dark:bg-gold-900/10' : 'border-gray-100 dark:border-gray-800'}">
                <input
                  type="checkbox"
                  class="mt-1 h-4 w-4 rounded border-gray-300 text-burgundy-700 focus:ring-burgundy-700"
                  checked={selectedHeroProductIds.includes(product.id)}
                  onchange={(e) => {
                    const checked = e.currentTarget.checked;
                    if (checked) {
                      selectedHeroProductIds = [...selectedHeroProductIds, product.id];
                    } else {
                      selectedHeroProductIds = selectedHeroProductIds.filter((id: string) => id !== product.id);
                    }
                  }}
                />
                <div class="flex flex-col gap-1 overflow-hidden">
                  {#if product.image_url}
                    <img src={product.image_url} alt={product.name} class="h-10 w-10 object-cover rounded-md" />
                  {/if}
                  <span class="text-xs font-semibold truncate">{product.name}</span>
                  <span class="text-[10px] text-gray-500">{product.brand}</span>
                </div>
              </label>
            {/each}
          </div>

          <!-- Hidden input to send array -->
          <input type="hidden" name="product_ids" value={JSON.stringify(selectedHeroProductIds)} />
        </div>

        <div class="pt-4">
          <Button type="submit" disabled={loading} class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold">
            {loading ? 'Saving Slider Config...' : 'Save Hero Slider'}
          </Button>
        </div>
      </form>
    {/if}
  </div>
</div>
