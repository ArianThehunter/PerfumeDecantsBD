-- Create 'products' public storage bucket if not already present
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'products',
  'products',
  true,
  5242880, -- 5MB limit
  array['image/jpeg', 'image/png', 'image/gif', 'image/webp']
) on conflict (id) do nothing;

-- Drop existing storage policies for clean recreate
drop policy if exists "Public Access for products" on storage.objects;
drop policy if exists "Admin insert for products" on storage.objects;
drop policy if exists "Admin update for products" on storage.objects;
drop policy if exists "Admin delete for products" on storage.objects;

-- Create policies to allow public select and admin uploads
create policy "Public Access for products" on storage.objects for select
using (bucket_id = 'products');

create policy "Admin insert for products" on storage.objects for insert
with check (bucket_id = 'products');

create policy "Admin update for products" on storage.objects for update
using (bucket_id = 'products');

create policy "Admin delete for products" on storage.objects for delete
using (bucket_id = 'products');
