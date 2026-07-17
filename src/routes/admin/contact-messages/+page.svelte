<script lang="ts">
  import { enhance } from '$app/forms';
  import { Mail, Trash2, Search, CheckCircle, Eye, Calendar, User, Clock, ArrowLeft } from '@lucide/svelte';
  import { formatDate } from '$lib/utils';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import type { PageData } from './$types';

  let { data } = $props<{ data: PageData }>();

  let messages = $derived(data.messages || []);
  let searchQuery = $state('');
  let selectedMessage = $state<any>(null);
  let detailOpen = $state(false);

  const filteredMessages = $derived(
    messages.filter((msg: any) => {
      const query = searchQuery.toLowerCase();
      return (
        msg.name.toLowerCase().includes(query) ||
        msg.email.toLowerCase().includes(query) ||
        msg.subject.toLowerCase().includes(query) ||
        msg.message.toLowerCase().includes(query)
      );
    })
  );

  function openDetails(msg: any) {
    selectedMessage = msg;
    detailOpen = true;

    // Auto mark as read if unread
    if (!msg.is_read) {
      const formData = new FormData();
      formData.append('id', msg.id);
      fetch('?/markRead', {
        method: 'POST',
        body: formData
      });
      msg.is_read = true; // Optimistic update
    }
  }
</script>

<svelte:head>
  <title>Contact Messages — PerfumeDecantsBD</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <div>
      <h1 class="font-heading text-2xl font-bold">Contact Messages</h1>
      <p class="text-xs text-[var(--text-muted)]">Read and manage inquiries sent through the website contact form.</p>
    </div>
    
    <div class="relative w-full sm:w-80">
      <Input
        type="search"
        placeholder="Search messages..."
        bind:value={searchQuery}
        class="pl-10 pr-4"
      />
      <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
    </div>
  </div>

  <hr class="border-gray-100 dark:border-gray-800" />

  <div class="card-premium overflow-hidden">
    {#if filteredMessages.length === 0}
      <div class="flex min-h-[250px] flex-col items-center justify-center p-8 text-center">
        <Mail class="h-10 w-10 text-gray-400" />
        <h3 class="mt-4 text-base font-semibold">No Messages Found</h3>
        <p class="text-xs text-[var(--text-muted)] mt-1">
          {searchQuery ? 'Adjust your search query.' : 'Inquiries from users will appear here.'}
        </p>
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100 dark:bg-gray-900 dark:border-gray-800 font-bold uppercase tracking-wider text-[var(--text-secondary)]">
              <th class="p-4">Status</th>
              <th class="p-4">Sender</th>
              <th class="p-4">Subject</th>
              <th class="p-4">Date Received</th>
              <th class="p-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            {#each filteredMessages as msg}
              <tr class="hover:bg-gray-50/50 dark:hover:bg-gray-900/50 transition-colors {!msg.is_read ? 'font-bold bg-burgundy-50/10 dark:bg-gold-500/5' : ''}">
                <td class="p-4">
                  {#if msg.is_read}
                    <span class="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-gray-600 dark:bg-gray-800 dark:text-gray-400">
                      Read
                    </span>
                  {:else}
                    <span class="inline-flex items-center rounded-full bg-burgundy-100 px-2.5 py-0.5 text-burgundy-800 dark:bg-burgundy-950/50 dark:text-gold-400 animate-pulse">
                      Unread
                    </span>
                  {/if}
                </td>
                <td class="p-4">
                  <div class="text-gray-900 dark:text-white font-medium">{msg.name}</div>
                  <div class="text-[10px] text-gray-500">{msg.email}</div>
                </td>
                <td class="p-4 max-w-xs truncate text-gray-800 dark:text-gray-300">{msg.subject}</td>
                <td class="p-4 text-gray-500">{formatDate(msg.created_at)}</td>
                <td class="p-4 text-center">
                  <div class="flex items-center justify-center gap-2">
                    <button
                      onclick={() => openDetails(msg)}
                      class="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-150 hover:bg-gray-50 text-gray-600 dark:border-gray-800 dark:hover:bg-gray-900 dark:text-gray-300"
                      title="View Full Message"
                    >
                      <Eye class="h-4 w-4" />
                    </button>

                    {#if msg.is_read}
                      <form method="post" action="?/markUnread" use:enhance>
                        <input type="hidden" name="id" value={msg.id} />
                        <button
                          type="submit"
                          class="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-150 hover:bg-gray-50 text-gray-500 dark:border-gray-800 dark:hover:bg-gray-900"
                          title="Mark as Unread"
                        >
                          <CheckCircle class="h-4 w-4 text-green-600 dark:text-green-400" />
                        </button>
                      </form>
                    {:else}
                      <form method="post" action="?/markRead" use:enhance>
                        <input type="hidden" name="id" value={msg.id} />
                        <button
                          type="submit"
                          class="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-150 hover:bg-gray-50 text-gray-500 dark:border-gray-800 dark:hover:bg-gray-900"
                          title="Mark as Read"
                        >
                          <CheckCircle class="h-4 w-4 text-gray-300 dark:text-gray-600" />
                        </button>
                      </form>
                    {/if}

                    <form method="post" action="?/deleteMessage" use:enhance>
                      <input type="hidden" name="id" value={msg.id} />
                      <button
                        type="submit"
                        class="flex h-8 w-8 items-center justify-center rounded-lg border border-red-200/50 hover:bg-red-50 text-red-500 dark:border-red-950 dark:hover:bg-red-950/20"
                        title="Delete Message"
                        onclick={(e) => {
                          if (!confirm('Are you sure you want to delete this message?')) {
                            e.preventDefault();
                          }
                        }}
                      >
                        <Trash2 class="h-4 w-4" />
                      </button>
                    </form>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>

<!-- Details Dialog -->
<Dialog.Root bind:open={detailOpen}>
  <Dialog.Content class="w-full max-w-lg bg-white dark:bg-gray-950 text-gray-900 dark:text-white rounded-2xl border border-gray-150 dark:border-gray-800 p-6">
    <Dialog.Header>
      <Dialog.Title class="font-heading text-xl font-bold flex items-center gap-2">
        <Mail class="h-5 w-5 text-burgundy-700 dark:text-gold-400" />
        Message Inquiry
      </Dialog.Title>
      <Dialog.Description class="text-xs text-[var(--text-muted)]">
        Detailed inquiry information from visitor.
      </Dialog.Description>
    </Dialog.Header>

    {#if selectedMessage}
      <div class="mt-4 space-y-4 text-sm">
        <div class="grid grid-cols-2 gap-4 border-b border-gray-100 dark:border-gray-800 pb-3">
          <div>
            <span class="block text-[10px] font-bold uppercase tracking-wider text-gray-500">Sender</span>
            <span class="font-semibold text-gray-850 dark:text-gray-200">{selectedMessage.name}</span>
          </div>
          <div>
            <span class="block text-[10px] font-bold uppercase tracking-wider text-gray-500">Email Address</span>
            <a href="mailto:{selectedMessage.email}" class="font-semibold text-burgundy-700 dark:text-gold-400 hover:underline">{selectedMessage.email}</a>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 border-b border-gray-100 dark:border-gray-800 pb-3">
          <div>
            <span class="block text-[10px] font-bold uppercase tracking-wider text-gray-500">Subject</span>
            <span class="text-gray-800 dark:text-gray-200">{selectedMessage.subject}</span>
          </div>
          <div>
            <span class="block text-[10px] font-bold uppercase tracking-wider text-gray-500">Received Date</span>
            <span class="text-gray-800 dark:text-gray-200">{formatDate(selectedMessage.created_at)}</span>
          </div>
        </div>

        <div class="space-y-1">
          <span class="block text-[10px] font-bold uppercase tracking-wider text-gray-500">Message</span>
          <div class="bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-800 rounded-xl p-4 text-xs leading-relaxed text-gray-800 dark:text-gray-300 max-h-60 overflow-y-auto whitespace-pre-wrap">
            {selectedMessage.message}
          </div>
        </div>
      </div>
    {/if}

    <div class="mt-6 flex justify-end">
      <Button onclick={() => (detailOpen = false)} class="bg-burgundy-700 hover:bg-burgundy-800 text-white rounded-xl">
        Close
      </Button>
    </div>
  </Dialog.Content>
</Dialog.Root>
