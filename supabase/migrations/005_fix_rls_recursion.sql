-- Create security definer function to check admin status without triggering RLS recursion
create or replace function public.is_admin()
returns boolean as $$
begin
  return exists (
    select 1 from public.profiles
    where id = auth.uid()
    and role = 'admin'
  );
end;
$$ language plpgsql security definer;

-- 1. PROFILES POLICIES
drop policy if exists "Admins have full access on profiles" on public.profiles;
create policy "Admins have full access on profiles" on public.profiles for all using (
    public.is_admin()
);

-- 2. CATEGORIES POLICIES
drop policy if exists "Admins have full access on categories" on public.categories;
create policy "Admins have full access on categories" on public.categories for all using (
    public.is_admin()
);

-- 3. PRODUCTS POLICIES
drop policy if exists "Products are viewable by anyone if active." on public.products;
create policy "Products are viewable by anyone if active." on public.products for select using (
    status = 'active' or public.is_admin()
);

drop policy if exists "Admins have full access on products" on public.products;
create policy "Admins have full access on products" on public.products for all using (
    public.is_admin()
);

-- 4. PRODUCT IMAGES POLICIES
drop policy if exists "Admins have full access on product_images" on public.product_images;
create policy "Admins have full access on product_images" on public.product_images for all using (
    public.is_admin()
);

-- 5. ORDERS POLICIES
drop policy if exists "Users can read own orders." on public.orders;
create policy "Users can read own orders." on public.orders for select using (
    auth.uid() = user_id or public.is_admin()
);

drop policy if exists "Admins can update orders." on public.orders;
create policy "Admins can update orders." on public.orders for update using (
    public.is_admin()
);

-- 6. ORDER ITEMS POLICIES
drop policy if exists "Users can read own order items." on public.order_items;
create policy "Users can read own order items." on public.order_items for select using (
    exists (
        select 1 from public.orders
        where orders.id = order_items.order_id
        and (orders.user_id = auth.uid() or public.is_admin())
    )
);

-- 7. SETTINGS POLICIES
drop policy if exists "Admins can update settings." on public.settings;
create policy "Admins can update settings." on public.settings for update using (
    public.is_admin()
);
