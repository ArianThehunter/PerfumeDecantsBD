-- Enable pgcrypto for password hashing if not already enabled
create extension if not exists pgcrypto;

-- Clean up any conflicting users/profiles before inserting
delete from auth.users where email = 'admin@perfumedecantsbd.com';
delete from public.profiles where id = 'd0000000-0000-0000-0000-000000000001';

-- Insert Admin User into auth.users
insert into auth.users (
  instance_id,
  id,
  aud,
  role,
  email,
  encrypted_password,
  email_confirmed_at,
  recovery_sent_at,
  last_sign_in_at,
  raw_app_meta_data,
  raw_user_meta_data,
  created_at,
  updated_at,
  confirmation_token,
  email_change,
  email_change_token_new,
  recovery_token
) values (
  '00000000-0000-0000-0000-000000000000',
  'd0000000-0000-0000-0000-000000000001', -- Fixed Admin UUID
  'authenticated',
  'authenticated',
  'admin@perfumedecantsbd.com',
  -- IMPORTANT: This is a default password ('admin12345') for development purposes.
  -- You MUST change this password immediately in a production environment.
  crypt('admin12345', gen_salt('bf')),
  now(),
  null,
  null,
  '{"provider": "email", "providers": ["email"]}',
  '{"full_name": "Administrator"}',
  now(),
  now(),
  '',
  '',
  '',
  ''
);

-- Insert/Verify profile in public.profiles to ensure it exists with the correct admin role
insert into public.profiles (id, full_name, role)
values (
  'd0000000-0000-0000-0000-000000000001',
  'Administrator',
  'admin'
) on conflict (id) do update set role = 'admin';
