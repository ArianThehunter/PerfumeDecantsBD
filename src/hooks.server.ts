import { createServerClient } from '@supabase/ssr';
import { type Handle, redirect } from '@sveltejs/kit';
import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';
import type { Database } from '$lib/types/database';

export const handle: Handle = async ({ event, resolve }) => {
  // Create Supabase client for this request
  event.locals.supabase = createServerClient<Database>(
    PUBLIC_SUPABASE_URL,
    PUBLIC_SUPABASE_ANON_KEY,
    {
      global: { fetch: event.fetch },
      cookies: {
        getAll: () => event.cookies.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) => {
            event.cookies.set(name, value, {
              ...options,
              path: '/'
            });
          });
        }
      }
    }
  );

  // Helper to safely get session
  event.locals.safeGetSession = async () => {
    const {
      data: { session }
    } = await event.locals.supabase.auth.getSession();

    if (!session) {
      return { session: null, user: null };
    }

    // Verify the user with getUser() for security
    const {
      data: { user },
      error
    } = await event.locals.supabase.auth.getUser();

    if (error) {
      return { session: null, user: null };
    }

    return { session, user };
  };

  // Get session for all requests
  const { session, user } = await event.locals.safeGetSession();
  event.locals.session = session;
  event.locals.user = user;

  // Protect admin routes
  if (event.url.pathname.startsWith('/admin')) {
    if (!user) {
      throw redirect(303, '/auth/login?redirect=/admin');
    }

    // Direct role bypass & sync for admin email
    if (user.email === 'admin@perfumedecantsbd.com') {
      const { data: profile } = await event.locals.supabase
        .from('profiles')
        .select('role')
        .eq('id', user.id)
        .single();
      
      if (!profile || profile.role !== 'admin') {
        await event.locals.supabase
          .from('profiles')
          .upsert({ id: user.id, role: 'admin', full_name: 'Administrator' });
      }
    } else {
      // Check admin role
      const { data: profile } = await event.locals.supabase
        .from('profiles')
        .select('role')
        .eq('id', user.id)
        .single();

      if (!profile || profile.role !== 'admin') {
        throw redirect(303, '/');
      }
    }
  }

  // Protect account routes
  if (event.url.pathname.startsWith('/account')) {
    if (!user) {
      throw redirect(303, '/auth/login?redirect=' + event.url.pathname);
    }
    // Redirect admin user to admin portal
    if (user.email === 'admin@perfumedecantsbd.com') {
      throw redirect(303, '/admin');
    }
  }

  return resolve(event, {
    filterSerializedResponseHeaders(name) {
      return name === 'content-range' || name === 'x-supabase-api-version';
    }
  });
};
