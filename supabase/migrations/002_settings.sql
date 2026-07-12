-- SETTINGS TABLE
create table public.settings (
    key text primary key,
    value jsonb not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Enable RLS
alter table public.settings enable row level security;

-- Policies
create policy "Settings are viewable by anyone." on public.settings for select using (true);
create policy "Admins can update settings." on public.settings for update using (
    exists (
        select 1 from public.profiles 
        where profiles.id = auth.uid() 
        and profiles.role = 'admin'
    )
);

-- Populate default values
insert into public.settings (key, value) values
('footer', '{
  "newsletter_title": "Join Our Fragrance Journey",
  "newsletter_desc": "Get exclusive access to new arrivals, special offers & fragrance tips",
  "brand_desc": "Your premier destination for authentic luxury perfume decants in Bangladesh. Experience world-class fragrances without the full-bottle commitment.",
  "facebook_url": "https://facebook.com/perfumedecantsbd",
  "instagram_url": "https://instagram.com/perfumedecantsbd",
  "telegram_url": "https://t.me/perfumedecantsbd",
  "address": "Dhaka, Bangladesh",
  "phone": "+880 1XXX-XXXXXX",
  "email": "hello@perfumedecantsbd.com",
  "copyright": "© 2026 PerfumeDecantsBD. All rights reserved."
}'::jsonb),

('about_page', '{
  "title": "Maison de Fragrance",
  "subtitle": "Bridging the gap between perfume enthusiasts and authentic luxury experiences.",
  "story_title": "Our Fragrant Narrative",
  "story_content_1": "PerfumeDecantsBD started from a simple, personal aspiration: the love for fine fragrances and the frustration of full-bottle commitments. We recognized that buying an expensive designer or niche bottle is a huge investment, especially when you are unsure if the scent suits your skin chemistry or personal lifestyle.",
  "story_content_2": "Our goal is to curate a library of authentic fragrances that can be sampled, explored, and worn before committing to a full luxury bottle. Every decant we assemble is handled with professional tools, clean procedures, and housed in high-quality spray atomizers that protect the juice inside.",
  "mission": "To provide fragrance enthusiasts in Bangladesh access to premium, authentic luxury and niche perfumes through accessible decant sizes. We guarantee authenticity, premium customer experience, and expert guidance.",
  "vision": "To become the most trusted and curated marketplace in Bangladesh for luxury fragrance discovery, offering an educational journey of perfume notes, skin chemistry, and signature scent profile creation.",
  "image_url": "https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?w=800&fit=crop"
}'::jsonb),

('contact_page', '{
  "title": "Contact Our Atelier",
  "subtitle": "Have questions about fragrance notes, decanting procedure, or order shipping? We are here to assist.",
  "form_title": "Send Us a Message",
  "form_subtitle": "We typically respond within 24 business hours.",
  "address": "Dhaka, Bangladesh",
  "phone": "+880 1XXX-XXXXXX",
  "email": "hello@perfumedecantsbd.com",
  "hours": "Sat - Thu: 10AM - 8PM",
  "map_lat": "23.8103",
  "map_lng": "90.4125"
}'::jsonb),

('shop_page', '{
  "title": "All Fragrances",
  "subtitle": "Browse our hand-picked collection of authentic luxury perfume decants."
}'::jsonb);
