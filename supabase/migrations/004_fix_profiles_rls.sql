-- Allow users to insert their own profile to resolve RLS violations during registration/login syncs
create policy "Users can insert their own profile" on public.profiles for insert with check (auth.uid() = id);
