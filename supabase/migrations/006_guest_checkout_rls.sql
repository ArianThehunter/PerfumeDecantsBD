-- Drop restrictive insert policies to allow both registered users and guest visitors to place orders
drop policy if exists "Users can insert own orders." on public.orders;
drop policy if exists "Users can insert own order items." on public.order_items;

-- Create anyone insert policies (required for guest checkout procedures)
create policy "Anyone can insert orders." on public.orders for insert with check (true);
create policy "Anyone can insert order items." on public.order_items for insert with check (true);
