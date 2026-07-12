-- Create custom types / check constraints are in the table definitions.

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- PROFILES
create table public.profiles (
    id uuid references auth.users on delete cascade primary key,
    full_name text,
    phone text,
    avatar_url text,
    role text default 'user'::text check (role in ('user', 'admin')),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- CATEGORIES
create table public.categories (
    id uuid default gen_random_uuid() primary key,
    name text not null,
    slug text not null unique,
    description text,
    image_url text,
    display_order integer default 0 not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- PRODUCTS
create table public.products (
    id uuid default gen_random_uuid() primary key,
    name text not null,
    slug text not null unique,
    brand text not null,
    category_id uuid references public.categories(id) on delete set null,
    short_description text,
    description text,
    top_notes text[],
    middle_notes text[],
    base_notes text[],
    price numeric not null check (price >= 0),
    discount_price numeric check (discount_price >= 0),
    sizes jsonb, -- e.g. [{"label": "5ml", "price": 500, "ml": 5}, {"label": "10ml", "price": 950, "ml": 10}]
    stock_quantity integer default 0 check (stock_quantity >= 0) not null,
    rating numeric default 0 check (rating >= 0 and rating <= 5) not null,
    review_count integer default 0 not null,
    is_featured boolean default false not null,
    is_bestseller boolean default false not null,
    is_new_arrival boolean default false not null,
    status text default 'draft'::text check (status in ('active', 'draft')) not null,
    gender text default 'unisex'::text check (gender in ('men', 'women', 'unisex')) not null,
    display_order integer default 0 not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- PRODUCT IMAGES
create table public.product_images (
    id uuid default gen_random_uuid() primary key,
    product_id uuid references public.products(id) on delete cascade not null,
    url text not null,
    alt_text text,
    is_primary boolean default false not null,
    display_order integer default 0 not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- ADDRESSES
create table public.addresses (
    id uuid default gen_random_uuid() primary key,
    user_id uuid references auth.users(id) on delete cascade not null,
    label text not null, -- e.g., 'Home', 'Office'
    full_name text not null,
    phone text not null,
    address_line_1 text not null,
    address_line_2 text,
    city text not null,
    postal_code text not null,
    is_default boolean default false not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- ORDERS
create table public.orders (
    id uuid default gen_random_uuid() primary key,
    user_id uuid references auth.users(id) on delete set null,
    order_number text not null unique,
    status text default 'pending'::text check (status in ('pending', 'confirmed', 'processing', 'completed', 'cancelled')) not null,
    subtotal numeric not null,
    shipping_cost numeric default 0 not null,
    total numeric not null,
    payment_method text not null check (payment_method in ('cod', 'bank_transfer')),
    shipping_address jsonb not null, -- Snapshot of address
    notes text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- ORDER ITEMS
create table public.order_items (
    id uuid default gen_random_uuid() primary key,
    order_id uuid references public.orders(id) on delete cascade not null,
    product_id uuid references public.products(id) on delete set null,
    product_name text not null,
    product_image text,
    size text,
    quantity integer not null check (quantity > 0),
    unit_price numeric not null check (unit_price >= 0),
    total_price numeric not null check (total_price >= 0),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- AUTO UPDATED_AT TRIGGER FUNCTION
create or replace function public.handle_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

-- Apply updated_at trigger to tables
create trigger set_updated_at_profiles before update on public.profiles for each row execute procedure public.handle_updated_at();
create trigger set_updated_at_categories before update on public.categories for each row execute procedure public.handle_updated_at();
create trigger set_updated_at_products before update on public.products for each row execute procedure public.handle_updated_at();
create trigger set_updated_at_addresses before update on public.addresses for each row execute procedure public.handle_updated_at();
create trigger set_updated_at_orders before update on public.orders for each row execute procedure public.handle_updated_at();

-- AUTO CREATE PROFILE ON SIGNUP
create or replace function public.handle_new_user()
returns trigger as $$
declare
    username text;
begin
    -- Extract full name from raw_user_meta_data if present, otherwise use email name part
    username := coalesce(
        new.raw_user_meta_data->>'full_name',
        split_part(new.email, '@', 1)
    );

    insert into public.profiles (id, full_name, role)
    values (
        new.id,
        username,
        case
            when new.email = 'admin@perfumedecantsbd.com' then 'admin'
            else 'user'
        end
    );
    return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
    after insert on auth.users
    for each row execute procedure public.handle_new_user();

-- ORDER NUMBER GENERATOR FUNCTION
create or replace function public.generate_order_number()
returns trigger as $$
declare
    seq_val bigint;
    new_order_num text;
begin
    -- Simple format: PDBD-YYYYMMDD-XXXX
    -- Let's use simple random suffix or sequential check
    seq_val := (select count(*) from public.orders where created_at::date = now()::date) + 1;
    new_order_num := 'PDBD-' || to_char(now(), 'YYYYMMDD') || '-' || lpad(seq_val::text, 4, '0');
    new.order_number := new_order_num;
    return new;
end;
$$ language plpgsql;

create trigger set_order_number before insert on public.orders for each row execute procedure public.generate_order_number();

-- ROW LEVEL SECURITY (RLS)
alter table public.profiles enable row level security;
alter table public.categories enable row level security;
alter table public.products enable row level security;
alter table public.product_images enable row level security;
alter table public.addresses enable row level security;
alter table public.orders enable row level security;
alter table public.order_items enable row level security;

-- PROFILES POLICIES
create policy "Public profiles are viewable by anyone." on public.profiles for select using (true);
create policy "Users can update their own profiles." on public.profiles for update using (auth.uid() = id);
create policy "Admins have full access on profiles" on public.profiles for all using (
    exists (select 1 from public.profiles where id = auth.uid() and role = 'admin')
);

-- CATEGORIES POLICIES
create policy "Categories are viewable by anyone." on public.categories for select using (true);
create policy "Admins have full access on categories" on public.categories for all using (
    exists (select 1 from public.profiles where id = auth.uid() and role = 'admin')
);

-- PRODUCTS POLICIES
create policy "Products are viewable by anyone if active." on public.products for select using (
    status = 'active' or exists (select 1 from public.profiles where id = auth.uid() and role = 'admin')
);
create policy "Admins have full access on products" on public.products for all using (
    exists (select 1 from public.profiles where id = auth.uid() and role = 'admin')
);

-- PRODUCT IMAGES POLICIES
create policy "Product images are viewable by anyone." on public.product_images for select using (true);
create policy "Admins have full access on product_images" on public.product_images for all using (
    exists (select 1 from public.profiles where id = auth.uid() and role = 'admin')
);

-- ADDRESSES POLICIES
create policy "Users can read own addresses." on public.addresses for select using (auth.uid() = user_id);
create policy "Users can insert own addresses." on public.addresses for insert with check (auth.uid() = user_id);
create policy "Users can update own addresses." on public.addresses for update using (auth.uid() = user_id);
create policy "Users can delete own addresses." on public.addresses for delete using (auth.uid() = user_id);

-- ORDERS POLICIES
create policy "Users can read own orders." on public.orders for select using (
    auth.uid() = user_id or exists (select 1 from public.profiles where id = auth.uid() and role = 'admin')
);
create policy "Users can insert own orders." on public.orders for insert with check (auth.uid() = user_id);
create policy "Admins can update orders." on public.orders for update using (
    exists (select 1 from public.profiles where id = auth.uid() and role = 'admin')
);

-- ORDER ITEMS POLICIES
create policy "Users can read own order items." on public.order_items for select using (
    exists (
        select 1 from public.orders
        where orders.id = order_items.order_id
        and (orders.user_id = auth.uid() or exists (select 1 from public.profiles where id = auth.uid() and role = 'admin'))
    )
);
create policy "Users can insert own order items." on public.order_items for insert with check (
    exists (
        select 1 from public.orders
        where orders.id = order_items.order_id
        and orders.user_id = auth.uid()
    )
);
