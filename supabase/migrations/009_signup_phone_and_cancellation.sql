-- 1. Add district to saved addresses
alter table public.addresses add column if not exists district text;

-- 2. Add cancellation timestamp to orders
alter table public.orders add column if not exists cancelled_at timestamp with time zone;

-- 3. Update handle_new_user to extract and insert phone number from raw user metadata
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

    insert into public.profiles (id, full_name, role, phone)
    values (
        new.id,
        username,
        case
            when new.email = 'admin@perfumedecantsbd.com' then 'admin'
            else 'user'
        end,
        coalesce(new.raw_user_meta_data->>'phone', new.phone)
    )
    on conflict (id) do update
    set full_name = excluded.full_name,
        phone = coalesce(excluded.phone, public.profiles.phone);
    return new;
end;
$$ language plpgsql security definer;

-- 4. Update existing settings data to point to the new email
update public.settings 
set value = jsonb_set(value, '{email}', '"readusshalehin22@gmail.com"') 
where value ? 'email';
