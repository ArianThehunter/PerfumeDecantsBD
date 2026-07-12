import { createBrowserClient, createServerClient, isBrowser } from '@supabase/ssr';
import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';
import type { Database } from '$lib/types/database';

export function createSupabaseClient(
  fetch: typeof globalThis.fetch,
  cookies?: {
    getAll: () => { name: string; value: string }[];
    setAll: (cookies: { name: string; value: string; options: Record<string, unknown> }[]) => void;
  }
) {
  if (isBrowser()) {
    return createBrowserClient<Database>(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
      global: { fetch }
    });
  }

  if (!cookies) {
    throw new Error('Cookies must be provided for server-side Supabase client');
  }

  return createServerClient<Database>(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
    global: { fetch },
    cookies: {
      getAll: () => cookies.getAll(),
      setAll: (cookiesToSet) => {
        cookies.setAll(
          cookiesToSet.map(({ name, value, options }) => ({
            name,
            value,
            options: options as Record<string, unknown>
          }))
        );
      }
    }
  });
}
