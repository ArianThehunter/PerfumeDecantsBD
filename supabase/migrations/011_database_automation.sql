-- 1. Create trigger function to automatically update updated_at column
create or replace function public.update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = timezone('utc'::text, now());
    return new;
end;
$$ language plpgsql;

-- Bind updated_at trigger to tables
create trigger trigger_update_profiles_updated_at before update on public.profiles
    for each row execute function public.update_updated_at_column();

create trigger trigger_update_categories_updated_at before update on public.categories
    for each row execute function public.update_updated_at_column();

create trigger trigger_update_products_updated_at before update on public.products
    for each row execute function public.update_updated_at_column();

create trigger trigger_update_addresses_updated_at before update on public.addresses
    for each row execute function public.update_updated_at_column();

create trigger trigger_update_orders_updated_at before update on public.orders
    for each row execute function public.update_updated_at_column();


-- 2. Add status timestamp columns to orders table
alter table public.orders add column if not exists confirmed_at timestamp with time zone;
alter table public.orders add column if not exists processing_at timestamp with time zone;
alter table public.orders add column if not exists completed_at timestamp with time zone;

-- Create trigger to automatically record timestamps on status change
create or replace function public.handle_order_status_timestamps()
returns trigger as $$
begin
    if new.status is distinct from old.status then
        if new.status = 'confirmed' then
            new.confirmed_at = timezone('utc'::text, now());
        elsif new.status = 'processing' then
            new.processing_at = timezone('utc'::text, now());
        elsif new.status = 'completed' then
            new.completed_at = timezone('utc'::text, now());
        elsif new.status = 'cancelled' then
            new.cancelled_at = timezone('utc'::text, now());
        end if;
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trigger_orders_status_timestamps before update on public.orders
    for each row execute function public.handle_order_status_timestamps();


-- 3. Create trigger to automatically recalculate order subtotal and grand total based on items
create or replace function public.recalculate_order_totals()
returns trigger as $$
declare
    v_subtotal numeric;
    v_shipping numeric;
begin
    -- Calculate subtotal from order_items
    select coalesce(sum(total_price), 0)
    into v_subtotal
    from public.order_items
    where order_id = coalesce(new.order_id, old.order_id);
    
    -- Fetch shipping cost from order
    select shipping_cost
    into v_shipping
    from public.orders
    where id = coalesce(new.order_id, old.order_id);
    
    -- Update the order's subtotal and grand total
    update public.orders
    set subtotal = v_subtotal,
        total = v_subtotal + v_shipping
    where id = coalesce(new.order_id, old.order_id);
    
    return new;
end;
$$ language plpgsql;

create trigger trigger_order_items_recalculate_totals
    after insert or update or delete on public.order_items
    for each row execute function public.recalculate_order_totals();


-- 4. Create trigger to automatically reduce product stock when order becomes completed, and restore if cancelled
create or replace function public.handle_order_completion_stock()
returns trigger as $$
declare
    item_record record;
begin
    -- Case 1: Status becomes 'completed' -> Decrement stock
    if new.status = 'completed' and old.status is distinct from 'completed' then
        for item_record in 
            select product_id, quantity 
            from public.order_items 
            where order_id = new.id
        loop
            update public.products
            set stock_quantity = greatest(0, stock_quantity - item_record.quantity)
            where id = item_record.product_id;
        end loop;
    
    -- Case 2: Status transitions away from 'completed' (e.g. cancelled/returned) -> Restore stock
    elsif old.status = 'completed' and new.status is distinct from 'completed' then
        for item_record in 
            select product_id, quantity 
            from public.order_items 
            where order_id = new.id
        loop
            update public.products
            set stock_quantity = stock_quantity + item_record.quantity;
        end loop;
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trigger_orders_completion_stock
    after update of status on public.orders
    for each row execute function public.handle_order_completion_stock();


-- 5. Helper function to generate slug from text
create or replace function public.slugify(v_text text)
returns text as $$
begin
    return lower(regexp_replace(regexp_replace(v_text, '[^a-zA-Z0-9\s-]', '', 'g'), '\s+', '-', 'g'));
end;
$$ language plpgsql;

-- Trigger to automatically generate product slugs if not manually set
create or replace function public.auto_generate_product_slug()
returns trigger as $$
begin
    if new.slug is null or new.slug = '' or (old.slug is not null and old.name is distinct from new.name and new.slug = old.slug) then
        new.slug = public.slugify(new.name);
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trigger_products_auto_slug
    before insert or update on public.products
    for each row execute function public.auto_generate_product_slug();

-- Trigger to automatically generate category slugs if not manually set
create or replace function public.auto_generate_category_slug()
returns trigger as $$
begin
    if new.slug is null or new.slug = '' or (old.slug is not null and old.name is distinct from new.name and new.slug = old.slug) then
        new.slug = public.slugify(new.name);
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trigger_categories_auto_slug
    before insert or update on public.categories
    for each row execute function public.auto_generate_category_slug();


-- 6. Seed default config for low stock threshold
insert into public.settings (key, value)
values ('inventory_settings', '{"low_stock_threshold": 5}'::jsonb)
on conflict (key) do nothing;


-- 7. Create database performance optimization indexes for foreign keys
create index if not exists idx_orders_user_id on public.orders(user_id);
create index if not exists idx_order_items_order_id on public.order_items(order_id);
create index if not exists idx_products_category_id on public.products(category_id);
create index if not exists idx_addresses_user_id on public.addresses(user_id);
