<script lang="ts">
  import { enhance } from '$app/forms';
  import { Mail, Phone, MapPin, Clock, Send } from '@lucide/svelte';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Textarea } from '$lib/components/ui/textarea';
  import { toast } from 'svelte-sonner';
  import type { PageData, ActionData } from './$types';

  let { data, form } = $props<{ data: PageData; form: ActionData }>();

  // Dynamic Settings
  const s = $derived(data.contactSettings || {});
  const title = $derived(s.title || 'Contact Our Atelier');
  const subtitle = $derived(s.subtitle || 'Have questions about fragrance notes, decanting procedure, or order shipping? We are here to assist.');
  const formTitle = $derived(s.form_title || 'Send Us a Message');
  const formSubtitle = $derived(s.form_subtitle || 'We typically respond within 24 business hours.');
  const address = $derived(s.address || 'Dhaka, Bangladesh');
  const phone = $derived(s.phone || '+880 1XXX-XXXXXX');
  const emailVal = 'readusshalehin22@gmail.com';
  const hours = $derived(s.hours || 'Sat - Thu: 10AM - 8PM');

  let name = $state('');
  let email = $state('');
  let subject = $state('');
  let message = $state('');
  let submitting = $state(false);

  $effect(() => {
    if (form?.success) {
      toast.success('Your message has been sent successfully. We will get back to you shortly.');
      name = '';
      email = '';
      subject = '';
      message = '';
    } else if (form?.message) {
      toast.error(form.message);
    }
  });
</script>

<svelte:head>
  <title>{title} — PerfumeDecantsBD</title>
</svelte:head>

<div class="bg-[var(--bg-primary)]">
  <!-- Page Hero -->
  <section class="relative min-h-[40vh] overflow-hidden bg-burgundy-950 flex items-center">
    <div class="absolute inset-0">
      <img src="/cover.png" alt="" class="h-full w-full object-cover opacity-15" />
      <div class="absolute inset-0 bg-gradient-to-t from-burgundy-950 to-transparent"></div>
    </div>
    <div class="container-luxury relative z-10 py-16 text-center text-white">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-400">Get In Touch</span>
      <h1 class="font-heading mt-4 text-4xl font-bold lg:text-5xl">{title}</h1>
      <p class="mx-auto mt-4 max-w-lg text-sm text-cream-300/70">
        {subtitle}
      </p>
    </div>
  </section>

  <!-- Contact Grid -->
  <section class="section-padding">
    <div class="container-luxury">
      <div class="grid gap-12 lg:grid-cols-2">
        <!-- Contact Form -->
        <div class="card-premium p-8">
          <h2 class="font-heading text-2xl font-bold text-burgundy-900 dark:text-gold-400">{formTitle}</h2>
          <p class="mt-2 text-sm text-[var(--text-muted)]">{formSubtitle}</p>

          <form
            method="post"
            action="?/submitMessage"
            use:enhance={() => {
              submitting = true;
              return async ({ update }) => {
                submitting = false;
                await update();
              };
            }}
            class="mt-6 space-y-4"
          >
            <div>
              <label for="name" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Your Name</label>
              <Input id="name" name="name" type="text" placeholder="Enter your full name" required bind:value={name} class="mt-1" />
            </div>

            <div>
              <label for="email" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Email Address</label>
              <Input id="email" name="email" type="email" placeholder="hello@example.com" required bind:value={email} class="mt-1" />
            </div>

            <div>
              <label for="subject" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Subject</label>
              <Input id="subject" name="subject" type="text" placeholder="How can we help?" required bind:value={subject} class="mt-1" />
            </div>

            <div>
              <label for="message" class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Message</label>
              <Textarea id="message" name="message" rows={5} placeholder="Write your message here..." required bind:value={message} class="mt-1" />
            </div>

            <Button
              type="submit"
              disabled={submitting}
              class="w-full bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold py-3 flex items-center justify-center gap-2"
            >
              {#if submitting}
                Sending Message...
              {:else}
                <Send class="h-4 w-4" />
                Send Message
              {/if}
            </Button>
          </form>
        </div>

        <!-- Contact Info & Map -->
        <div class="space-y-8">
          <div class="grid gap-6 sm:grid-cols-2">
            <!-- Address -->
            <div class="card-premium p-6 flex flex-col items-center text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
                <MapPin class="h-5 w-5" />
              </div>
              <h3 class="mt-4 font-heading text-base font-bold">Atelier Address</h3>
              <p class="mt-2 text-sm text-[var(--text-muted)]">{address}</p>
            </div>

            <!-- Phone -->
            <div class="card-premium p-6 flex flex-col items-center text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
                <Phone class="h-5 w-5" />
              </div>
              <h3 class="mt-4 font-heading text-base font-bold">Phone Number</h3>
              <p class="mt-2 text-sm text-[var(--text-muted)]">{phone}</p>
            </div>

            <!-- Email -->
            <div class="card-premium p-6 flex flex-col items-center text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
                <Mail class="h-5 w-5" />
              </div>
              <h3 class="mt-4 font-heading text-base font-bold">Email Atelier</h3>
              <a href="mailto:{emailVal}" class="mt-2 text-sm text-[var(--text-muted)] hover:text-burgundy-700 dark:hover:text-gold-400 break-all">{emailVal}</a>
            </div>

            <!-- Hours -->
            <div class="card-premium p-6 flex flex-col items-center text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-burgundy-50 text-burgundy-700 dark:bg-burgundy-950 dark:text-gold-400">
                <Clock class="h-5 w-5" />
              </div>
              <h3 class="mt-4 font-heading text-base font-bold">Business Hours</h3>
              <p class="mt-2 text-sm text-[var(--text-muted)]">{hours}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>
