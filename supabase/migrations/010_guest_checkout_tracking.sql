-- Create tracking RPC functions for secure guest checkout tracking
-- These run as SECURITY DEFINER to bypass RLS, but strictly require both order number/ID and phone number to match.

create or replace function public.track_guest_order(p_order_identifier text, p_phone text)
returns table (
    id uuid,
    user_id uuid,
    order_number text,
    status text,
    subtotal numeric,
    shipping_cost numeric,
    total numeric,
    payment_method text,
    shipping_address jsonb,
    notes text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
) security definer
set search_path = public
as $$
begin
    return query
    select o.id, o.user_id, o.order_number, o.status, o.subtotal, o.shipping_cost, o.total, o.payment_method, o.shipping_address, o.notes, o.created_at, o.updated_at
    from public.orders o
    where (o.order_number = p_order_identifier or o.id::text = p_order_identifier)
      and o.shipping_address->>'phone' = p_phone;
end;
$$ language plpgsql;

create or replace function public.track_guest_order_items(p_order_identifier text, p_phone text)
returns table (
    id uuid,
    order_id uuid,
    product_id uuid,
    product_name text,
    product_image text,
    size text,
    quantity integer,
    unit_price numeric,
    total_price numeric,
    created_at timestamp with time zone
) security definer
set search_path = public
as $$
begin
    return query
    select oi.id, oi.order_id, oi.product_id, oi.product_name, oi.product_image, oi.size, oi.quantity, oi.unit_price, oi.total_price, oi.created_at
    from public.order_items oi
    join public.orders o on o.id = oi.order_id
    where (o.order_number = p_order_identifier or o.id::text = p_order_identifier)
      and o.shipping_address->>'phone' = p_phone;
end;
$$ language plpgsql;

-- Count unclaimed guest orders by email
create or replace function public.count_unclaimed_guest_orders(p_email text)
returns bigint security definer
set search_path = public
as $$
begin
    return (
        select count(*)
        from public.orders
        where user_id is null
          and shipping_address->>'email' = p_email
    );
end;
$$ language plpgsql;

-- Claim guest orders by email and assign to registered user ID
create or replace function public.claim_guest_orders(p_user_id uuid, p_email text)
returns integer security definer
set search_path = public
as $$
declare
    updated_rows integer;
begin
    update public.orders
    set user_id = p_user_id
    where user_id is null
      and shipping_address->>'email' = p_email;
    
    get diagnostics updated_rows = row_count;
    return updated_rows;
end;
$$ language plpgsql;
