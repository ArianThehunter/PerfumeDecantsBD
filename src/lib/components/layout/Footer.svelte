<script lang="ts">
  import { page } from '$app/state';
  import { Mail, MapPin, Phone, Send, ArrowRight } from '@lucide/svelte';

  let email = $state('');
  let subscribed = $state(false);

  // Dynamic Settings
  const s = $derived(page.data.settings?.footer || {});
  const newsletterTitle = $derived(s.newsletter_title || 'Join Our Fragrance Journey');
  const newsletterDesc = $derived(s.newsletter_desc || 'Get exclusive access to new arrivals, special offers & fragrance tips');
  const brandDesc = $derived(s.brand_desc || 'Your premier destination for authentic luxury perfume decants in Bangladesh. Experience world-class fragrances without the full-bottle commitment.');
  const fbUrl = $derived(s.facebook_url || '#');
  const instaUrl = $derived(s.instagram_url || '#');
  const telegramUrl = $derived(s.telegram_url || '#');
  const address = $derived(s.address || 'Dhaka, Bangladesh');
  const phone = $derived(s.phone || '+880 1XXX-XXXXXX');
  const emailAddr = $derived(s.email || 'hello@perfumedecantsbd.com');
  const copyright = $derived(s.copyright || `© ${new Date().getFullYear()} PerfumeDecantsBD. All rights reserved.`);

  function handleSubscribe(e: Event) {
    e.preventDefault();
    if (email) {
      subscribed = true;
      email = '';
      setTimeout(() => (subscribed = false), 3000);
    }
  }
</script>

<footer class="bg-burgundy-950 text-cream-200">


  <!-- Main Footer -->
  <div class="container-luxury py-16">
    <div class="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
      <!-- Brand -->
      <div class="sm:col-span-2 lg:col-span-1">
        <div class="flex items-center gap-2">
          <img src="/logo.jpg" alt="PerfumeDecantsBD" class="h-10 w-10 rounded-full" />
          <span class="font-heading text-xl font-bold text-white">
            PerfumeDecants<span class="text-gold-400">BD</span>
          </span>
        </div>
        <p class="mt-4 text-sm leading-relaxed text-cream-300/60">
          {brandDesc}
        </p>
        <div class="mt-5 flex gap-3">
          <a
            href={fbUrl}
            target="_blank"
            rel="noopener noreferrer"
            class="flex h-9 w-9 items-center justify-center rounded-full bg-burgundy-900 text-cream-300 transition-all hover:bg-gold-500 hover:text-burgundy-950"
            aria-label="Facebook"
          >
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
          </a>
        </div>
      </div>

      <!-- Quick Links -->
      <div>
        <h4 class="font-heading text-sm font-bold uppercase tracking-wider text-gold-400">Quick Links</h4>
        <ul class="mt-4 space-y-2.5">
          {#each [
            { href: '/shop', label: 'Shop All' },
            { href: '/about', label: 'About Us' },
            { href: '/contact', label: 'Contact' },
            { href: '/auth/login', label: 'My Account' }
          ] as link}
            <li>
              <a
                href={link.href}
                class="text-sm text-cream-300/60 transition-colors hover:text-gold-400"
              >
                {link.label}
              </a>
            </li>
          {/each}
        </ul>
      </div>

      <!-- Categories -->
      <div>
        <h4 class="font-heading text-sm font-bold uppercase tracking-wider text-gold-400">Categories</h4>
        <ul class="mt-4 space-y-2.5">
          {#each ['Eau de Parfum', 'Eau de Toilette', 'Cologne', 'Unisex', 'Gift Sets'] as cat}
            <li>
              <a
                href="/shop?category={cat.toLowerCase().replace(/ /g, '-')}"
                class="text-sm text-cream-300/60 transition-colors hover:text-gold-400"
              >
                {cat}
              </a>
            </li>
          {/each}
        </ul>
      </div>

      <!-- Contact -->
      <div>
        <h4 class="font-heading text-sm font-bold uppercase tracking-wider text-gold-400">Contact Us</h4>
        <ul class="mt-4 space-y-3">
          <li class="flex items-start gap-3 text-sm text-cream-300/60">
            <MapPin class="mt-0.5 h-4 w-4 shrink-0 text-gold-500" />
            <span>{address}</span>
          </li>
          <li class="flex items-center gap-3 text-sm text-cream-300/60">
            <Phone class="h-4 w-4 shrink-0 text-gold-500" />
            <span>{phone}</span>
          </li>
          <li class="flex items-center gap-3 text-sm text-cream-300/60">
            <Mail class="h-4 w-4 shrink-0 text-gold-500" />
            <span>{emailAddr}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Bottom Bar -->
  <div class="border-t border-burgundy-900">
    <div class="container-luxury flex flex-col items-center justify-between gap-4 py-6 sm:flex-row">
      <p class="text-xs text-cream-300/40">
        {copyright}
      </p>
      <div class="flex gap-6">
        <a href="/about" class="text-xs text-cream-300/40 transition-colors hover:text-gold-400">Privacy Policy</a>
        <a href="/contact" class="text-xs text-cream-300/40 transition-colors hover:text-gold-400">Terms of Service</a>
        <a href="/contact" class="text-xs text-cream-300/40 transition-colors hover:text-gold-400">Refund Policy</a>
      </div>
    </div>
  </div>
</footer>
