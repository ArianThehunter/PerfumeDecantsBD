<script lang="ts">
  import { Search, ChevronDown, Mail, ArrowRight, HelpCircle } from '@lucide/svelte';
  import { Button } from '$lib/components/ui/button';

  interface FAQItem {
    id: string;
    category: string;
    question: string;
    answer: string;
  }

  const faqData: FAQItem[] = [
    // Orders
    {
      id: 'o-place',
      category: 'Orders',
      question: 'How do I place an order?',
      answer: 'Placing an order is simple:\n1. Browse our collection of luxury perfume decants and choose your desired fragrance.\n2. Select your preferred decant size (e.g., 2ml, 5ml, 10ml) and click "Add to Cart".\n3. Click on the Shopping Cart drawer icon to review your selected decants.\n4. Click "Proceed to Checkout" where you will fill in your shipping details and select your payment method (Cash on Delivery or Bank Transfer).\n5. Confirm and place your order. You will receive an email/message confirmation once submitted.'
    },
    {
      id: 'o-cancel',
      category: 'Orders',
      question: 'Can I cancel my order?',
      answer: 'Yes, you can cancel your order before it has been shipped. To cancel, go to your Account Dashboard under "Order History", locate the order, and click the "Cancel Order" button (available for Pending or Confirmed orders). If the order has already been dispatched/shipped, it cannot be cancelled directly and applicable courier/return shipping charges will apply according to our company policy.'
    },
    {
      id: 'o-modify',
      category: 'Orders',
      question: 'Can I modify my order?',
      answer: 'You may modify your order (such as changing decant sizes, quantities, or updating delivery address details) before it has been shipped. Please contact our support team immediately at readusshalehin22@gmail.com with your order number to request modifications. Once an order is handed over to the courier, no further modifications can be made.'
    },
    // Shipping
    {
      id: 's-where',
      category: 'Shipping',
      question: 'Where do you deliver?',
      answer: 'We currently deliver only within Bangladesh. All 64 districts are covered under our courier network.'
    },
    {
      id: 's-time',
      category: 'Shipping',
      question: 'How long does delivery take?',
      answer: 'Standard delivery normally takes 2–4 business days. Inside Dhaka, deliveries are often completed within 24–48 hours. Please note that delivery timelines may vary during public holidays, severe weather conditions, political strikes, or other unforeseen courier service disruptions beyond our control.'
    },
    {
      id: 's-charges',
      category: 'Shipping',
      question: 'What are the delivery charges?',
      answer: 'Our standard shipping rates are:\n• Inside Dhaka City: BDT 80\n• Outside Dhaka City (All other districts): BDT 140\n\nThe final delivery charges are automatically calculated and displayed on the checkout page after you select or fill in your district and city.'
    },
    {
      id: 's-unavailable',
      category: 'Shipping',
      question: "What happens if I'm unavailable during delivery?",
      answer: 'Our delivery partner will typically attempt to contact you via phone before arriving. Courier re-attempt schedules depend entirely on the respective courier service provider\'s policy. Please make sure your phone number is active and reachable. Providing incorrect address details or failing to receive calls may cause the parcel to be returned to us, requiring additional delivery charges to re-ship.'
    },
    // Returns & Refunds
    {
      id: 'r-return',
      category: 'Returns & Refunds',
      question: 'Can I return a product?',
      answer: 'Returns are accepted only under the specific conditions defined in our Return Policy. To be eligible for a return, the product must be in its original, undamaged condition. Used products, sprayed decants, and opened bottles cannot be returned under any circumstances due to health and safety standards.'
    },
    {
      id: 'r-non-returnable',
      category: 'Returns & Refunds',
      question: 'Which products cannot be returned?',
      answer: 'The following products cannot be returned or exchanged under any circumstances:\n• Used or sprayed decants\n• Opened retail bottles (if the seal or wrapping has been broken)\n• Products showing signs of personal use'
    },
    {
      id: 'r-timeframe',
      category: 'Returns & Refunds',
      question: 'How long do I have to request a return?',
      answer: 'You must request a return or report any issue (e.g. transit leakage, wrong product, broken bottle) within 48 hours of receiving the parcel. Claims made after 48 hours of delivery will not be accepted.'
    },
    {
      id: 'r-cost',
      category: 'Returns & Refunds',
      question: 'Who pays the return shipping cost?',
      answer: 'If the return request is approved and meets our company policies (such as wrong item shipped, or product broken during transit), Perfume Decants BD will fully cover the return shipping costs. In other cases, returns are not accepted.'
    },
    {
      id: 'r-exchange',
      category: 'Returns & Refunds',
      question: 'Can I exchange a product?',
      answer: 'Yes, exchanges are permitted for eligible unused, defective, or incorrect products. Once our team receives and inspects the returned item to confirm it has not been used or sprayed, we will ship out the replacement item.'
    },
    {
      id: 'r-refund-time',
      category: 'Returns & Refunds',
      question: 'How long do refunds take?',
      answer: 'Refunds are normally processed within 24 hours after the return has been inspected and approved by our quality control team. Depending on your payment method (bKash, Nagad, or Bank Transfer), it may take slightly longer to reflect in your account due to standard banking settlement cycles.'
    },
    // Product Authenticity
    {
      id: 'a-auth',
      category: 'Product Authenticity',
      question: 'Are your perfumes authentic?',
      answer: 'Yes, 100% authenticity is guaranteed. All decants are poured directly from original designer and niche brand perfume bottles. We do not sell copies, duplicates, or testers of questionable origin. If you have concerns regarding authenticity, valid and objective evidence (such as batch checks or comparative documentation) is required before a return request can be evaluated.'
    },
    {
      id: 'a-color',
      category: 'Product Authenticity',
      question: 'Why does the perfume color sometimes look different?',
      answer: 'Juice colors may vary slightly due to different manufacturing batches, natural reformulation of ingredients by the perfume houses over time, or lighting conditions in photographs. A minor color variance is common in the fragrance industry and does not indicate that a product is duplicate or fake.'
    },
    {
      id: 'a-perf',
      category: 'Product Authenticity',
      question: 'Why does my fragrance perform differently?',
      answer: 'Fragrance performance (longevity and projection) is subject to many variables including manufacturer reformulations, storage environment (humidity/heat), current weather/seasons, skin moisturization levels, and individual skin chemistry. We recommend spraying on moisturized skin or clothing to enhance performance.'
    },
    // Delivery Inspection
    {
      id: 'd-inspect',
      category: 'Delivery Inspection',
      question: 'Should I inspect the parcel before accepting it?',
      answer: 'Yes. It is mandatory for customers to inspect the parcel immediately in front of the courier agent upon delivery. Please check for leaks, broken bottles, wrong products, or missing decants. Any claims regarding damages or missing items made after accepting the parcel without checking in front of the courier will not be eligible for returns or refunds.'
    },
    // Payments
    {
      id: 'p-advance',
      category: 'Payments',
      question: 'Do I need to make an advance payment?',
      answer: 'Advance payment may be requested in the following scenarios:\n1. Orders exceeding BDT 5,000: Up to 10% advance payment is required.\n2. Delivery Outside Dhaka: Courier charge advance is required for orders under BDT 5,000; 10% advance is required for orders above BDT 5,000.\n3. Previous Order Cancellations: Customers who have previously cancelled or returned orders without valid justification will be required to pay 10% to 100% of the order value in advance.'
    },
    {
      id: 'p-methods',
      category: 'Payments',
      question: 'Which payment methods do you accept?',
      answer: 'We currently accept the following payment methods:\n• Cash on Delivery (COD)\n• Mobile Banking (bKash & Nagad) via Send Money to 01770207576\n• Bank Transfer to our NRB Commercial Bank account:\n  - Account Name: Md Readus Shalehin\n  - Account Number: 520031100001718\n  - Branch: Mirpur 12\n  - Routing Number: 260261089'
    },
    // Accounts
    {
      id: 'ac-account',
      category: 'Accounts',
      question: 'Do I need an account to order?',
      answer: 'No, you do not need to register an account to place an order. Guest checkout is fully supported. However, registering an account allows you to securely save shipping addresses for faster checkout, view your tracking history, and check order statuses in your account dashboard.'
    },
    {
      id: 'ac-secure',
      category: 'Accounts',
      question: 'Is my personal information secure?',
      answer: 'Yes, your privacy is our top priority. We use industry-standard encryption protocols. Your contact details, addresses, and transaction histories are used exclusively for shipping coordination, order processing, and improving your discovery experience. We never sell or share customer data.'
    },
    // General
    {
      id: 'g-intl',
      category: 'General',
      question: 'Do you ship internationally?',
      answer: 'No, we currently deliver only within Bangladesh.'
    },
    {
      id: 'g-photos',
      category: 'General',
      question: 'Are all product photos real?',
      answer: 'Yes, product images displayed on our store are produced by Perfume Decants BD where applicable. The colors of perfume juice or bottles might differ slightly in real life due to studio lighting, camera settings, and batch variations.'
    },
    {
      id: 'g-price',
      category: 'General',
      question: 'Can prices change?',
      answer: 'Yes. Due to international sourcing costs, import duties, currency exchange rates, and brand pricing adjustments, perfume decant prices and availability are subject to change without prior notice.'
    }
  ];

  const categories = [
    'All',
    'Orders',
    'Shipping',
    'Returns & Refunds',
    'Product Authenticity',
    'Delivery Inspection',
    'Payments',
    'Accounts',
    'General'
  ];

  let searchQuery = $state('');
  let selectedCategory = $state('All');
  let expandedId = $state<string | null>(null);

  // Filter items based on search query and selected category
  let filteredItems = $derived.by(() => {
    let result = faqData;

    // Filter by search query across all text fields
    if (searchQuery.trim() !== '') {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(
        (item) =>
          item.question.toLowerCase().includes(q) ||
          item.answer.toLowerCase().includes(q) ||
          item.category.toLowerCase().includes(q)
      );
    } else if (selectedCategory !== 'All') {
      // If search query is empty, filter by category tab
      result = result.filter((item) => item.category === selectedCategory);
    }

    return result;
  });

  // Calculate count of items per category
  function getCategoryCount(cat: string): number {
    if (cat === 'All') return faqData.length;
    return faqData.filter((item) => item.category === cat).length;
  }

  function toggleItem(id: string) {
    if (expandedId === id) {
      expandedId = null;
    } else {
      expandedId = id;
    }
  }

  function resetSearch() {
    searchQuery = '';
    selectedCategory = 'All';
    expandedId = null;
  }
</script>

<svelte:head>
  <title>Frequently Asked Questions — PerfumeDecantsBD</title>
</svelte:head>

<div class="bg-[var(--bg-primary)] min-h-screen">
  <!-- Page Header -->
  <section class="relative min-h-[35vh] overflow-hidden bg-burgundy-950 flex items-center">
    <div class="absolute inset-0">
      <img src="/cover.png" alt="" class="h-full w-full object-cover opacity-15" />
      <div class="absolute inset-0 bg-gradient-to-t from-burgundy-950 to-transparent"></div>
    </div>
    <div class="container-luxury relative z-10 py-16 text-center text-white space-y-4">
      <span class="text-xs font-semibold uppercase tracking-widest text-gold-400">Atelier Help Center</span>
      <h1 class="font-heading text-4xl font-bold lg:text-5xl">Frequently Asked Questions</h1>
      <p class="mx-auto max-w-lg text-sm text-cream-300/70">
        Find quick answers regarding our decanting procedures, authentications, courier operations, and terms.
      </p>

      <!-- Search Input Container -->
      <div class="mx-auto max-w-lg pt-4">
        <div class="relative">
          <Search class="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-cream-400/50" />
          <input
            type="text"
            bind:value={searchQuery}
            placeholder="Search questions (e.g., authenticity, refunds, COD)..."
            class="w-full rounded-full border border-burgundy-900 bg-burgundy-900/35 py-3.5 pl-12 pr-4 text-sm text-white placeholder-cream-400/50 backdrop-blur-sm transition-all focus:border-gold-500 focus:outline-none focus:ring-2 focus:ring-gold-500/20"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ Body Content -->
  <div class="container-luxury py-12 lg:py-20">
    <div class="grid gap-10 lg:grid-cols-[250px_1fr]">
      <!-- Left Column: Category Navigation Tabs -->
      <div class="space-y-4">
        <h3 class="font-heading text-xs font-bold uppercase tracking-wider text-[var(--text-muted)] hidden lg:block">
          Categories
        </h3>

        <!-- Desktop Sidebar Menu -->
        <div class="hidden flex-col gap-1 lg:flex">
          {#each categories as cat}
            <button
              type="button"
              onclick={() => {
                selectedCategory = cat;
                searchQuery = '';
                expandedId = null;
              }}
              class="flex items-center justify-between rounded-xl px-4 py-3 text-left text-sm font-semibold transition-all {selectedCategory === cat && searchQuery === ''
                ? 'bg-burgundy-700 text-white dark:bg-gold-500 dark:text-burgundy-950 font-bold'
                : 'text-gray-700 hover:bg-gray-100 hover:text-burgundy-900 dark:text-gray-300 dark:hover:bg-gray-900 dark:hover:text-gold-450'}"
            >
              <span>{cat}</span>
              <span class="text-xs opacity-60">({getCategoryCount(cat)})</span>
            </button>
          {/each}
        </div>

        <!-- Mobile Scrollable Category Tabs -->
        <div class="flex gap-2 overflow-x-auto pb-3 scrollbar-none lg:hidden -mx-4 px-4">
          {#each categories as cat}
            <button
              type="button"
              onclick={() => {
                selectedCategory = cat;
                searchQuery = '';
                expandedId = null;
              }}
              class="shrink-0 rounded-full px-4 py-2 text-xs font-bold transition-all border {selectedCategory === cat && searchQuery === ''
                ? 'bg-burgundy-700 text-white border-burgundy-700 dark:bg-gold-500 dark:text-burgundy-950 dark:border-gold-500'
                : 'bg-white border-gray-200 text-gray-700 dark:bg-gray-950 dark:border-gray-800 dark:text-gray-300'}"
            >
              {cat} ({getCategoryCount(cat)})
            </button>
          {/each}
        </div>
      </div>

      <!-- Right Column: Accordions List -->
      <div class="space-y-6">
        <!-- Search query active banner -->
        {#if searchQuery.trim() !== ''}
          <div class="flex justify-between items-center text-xs text-[var(--text-secondary)] font-semibold border-b pb-3 dark:border-gray-800">
            <span>Found {filteredItems.length} results matching "{searchQuery}"</span>
            <button type="button" onclick={resetSearch} class="text-burgundy-700 dark:text-gold-400 underline font-bold">
              Clear Filter
            </button>
          </div>
        {/if}

        <!-- Empty state -->
        {#if filteredItems.length === 0}
          <div class="card-premium p-10 text-center space-y-4 max-w-lg mx-auto">
            <HelpCircle class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="font-heading text-lg font-bold text-gray-900 dark:text-white">No questions found</h3>
            <p class="text-xs text-[var(--text-muted)] leading-relaxed">
              We couldn't find any questions matching your query. Try searching for different keywords or browse our categories.
            </p>
            <Button variant="outline" class="rounded-xl text-xs" onclick={resetSearch}>
              Reset Filters
            </Button>
          </div>
        {:else}
          <!-- Accordion Panel Container -->
          <div class="card-premium p-6 divide-y divide-gray-100 dark:divide-gray-850">
            {#each filteredItems as item}
              <div class="py-4 first:pt-0 last:pb-0">
                <button
                  type="button"
                  class="flex w-full items-center justify-between text-left font-heading font-bold text-gray-900 dark:text-cream-200 hover:text-burgundy-700 dark:hover:text-gold-450 transition-colors py-2"
                  onclick={() => toggleItem(item.id)}
                  aria-expanded={expandedId === item.id}
                >
                  <span class="text-sm tracking-wide lg:text-base leading-snug">{item.question}</span>
                  <span class="ml-4 shrink-0 transition-transform duration-300 {expandedId === item.id ? 'rotate-180 text-burgundy-700 dark:text-gold-400' : 'text-gray-400 dark:text-gray-600'}">
                    <ChevronDown class="h-5 w-5" />
                  </span>
                </button>
                
                {#if expandedId === item.id}
                  <div class="mt-3 text-xs leading-relaxed text-[var(--text-secondary)] whitespace-pre-line pl-1 animate-scale-in lg:text-sm">
                    {item.answer}
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  </div>

  <!-- Still Have Questions Footer section -->
  <section class="border-t border-gray-100 bg-white py-16 text-center dark:border-gray-900 dark:bg-gray-950">
    <div class="container-luxury space-y-4 max-w-xl">
      <h2 class="font-heading text-2xl font-bold text-gray-900 dark:text-white">Still have questions?</h2>
      <p class="text-xs text-[var(--text-muted)] leading-relaxed max-w-sm mx-auto">
        If you couldn't find the answers you were looking for, please feel free to contact our customer support team directly.
      </p>
      
      <div class="pt-4 flex flex-col sm:flex-row gap-4 justify-center items-center">
        <a
          href="mailto:readusshalehin22@gmail.com"
          class="flex items-center gap-2 text-xs font-bold text-burgundy-800 dark:text-gold-400 hover:underline"
        >
          <Mail class="h-4 w-4" />
          readusshalehin22@gmail.com
        </a>
        
        <span class="hidden sm:inline text-gray-300">|</span>
        
        <a href="/contact">
          <Button class="bg-burgundy-700 hover:bg-burgundy-800 text-white font-semibold flex items-center gap-2 rounded-xl text-xs py-2 px-6">
            Contact Us
            <ArrowRight class="h-3.5 w-3.5" />
          </Button>
        </a>
      </div>
    </div>
  </section>
</div>

<style>
  /* Hide scrollbar for mobile categories selector scroll row */
  .scrollbar-none::-webkit-scrollbar {
    display: none;
  }
  .scrollbar-none {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
</style>
