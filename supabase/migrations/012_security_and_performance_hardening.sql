-- Migration 012: Security & Performance Hardening
-- 1. Secure Storage Bucket RLS Policies (Fixing authorization vulnerability)
-- 2. Add Composite Performance Indexes for High-Traffic Scaling

-- ============================================================================
-- 1. STORAGE SECURITY HARDENING
-- ============================================================================
-- Drop existing open/insecure storage policies on storage.objects
drop policy if exists "Admin insert for products" on storage.objects;
drop policy if exists "Admin update for products" on storage.objects;
drop policy if exists "Admin delete for products" on storage.objects;
drop policy if exists "Public Access for products" on storage.objects;

-- Recreate Public Read Policy
create policy "Public Access for products" on storage.objects for select
using (bucket_id = 'products');

-- Strictly require administrator privileges for mutations
create policy "Admin insert for products" on storage.objects for insert
with check (
    bucket_id = 'products' 
    and public.is_admin()
);

create policy "Admin update for products" on storage.objects for update
using (
    bucket_id = 'products' 
    and public.is_admin()
);

create policy "Admin delete for products" on storage.objects for delete
using (
    bucket_id = 'products' 
    and public.is_admin()
);


-- ============================================================================
-- 2. HIGH-SCALE COMPOSITE INDEXES
-- ============================================================================
-- Catalog Filtering & Sorting Indexes
create index if not exists idx_products_status_category_brand 
    on public.products(status, category_id, brand);

create index if not exists idx_products_rating_price 
    on public.products(rating desc, price asc) 
    where status = 'active';

create index if not exists idx_products_featured_active 
    on public.products(is_featured, created_at desc) 
    where status = 'active';

create index if not exists idx_products_bestseller_active 
    on public.products(is_bestseller, created_at desc) 
    where status = 'active';

create index if not exists idx_products_new_arrival_active 
    on public.products(is_new_arrival, created_at desc) 
    where status = 'active';

-- Orders Performance Indexes
create index if not exists idx_orders_status_created_at 
    on public.orders(status, created_at desc);

create index if not exists idx_orders_order_number 
    on public.orders(order_number);

-- Contact Messages Management Indexes
create index if not exists idx_contact_messages_is_read_created 
    on public.contact_messages(is_read, created_at desc);
