-- Create contact messages table
create table public.contact_messages (
    id uuid default gen_random_uuid() primary key,
    name text not null,
    email text not null,
    subject text not null,
    message text not null,
    is_read boolean default false not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Enable Row Level Security
alter table public.contact_messages enable row level security;

-- Drop existing policies if any
drop policy if exists "Anyone can insert contact messages" on public.contact_messages;
drop policy if exists "Admins can view and manage contact messages" on public.contact_messages;

-- Policy to allow anonymous/public insert
create policy "Anyone can insert contact messages" on public.contact_messages for insert
with check (true);

-- Policy to allow admins full control
create policy "Admins can view and manage contact messages" on public.contact_messages for all
using (public.is_admin());
