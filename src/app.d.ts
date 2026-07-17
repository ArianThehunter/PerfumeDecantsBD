// See https://svelte.dev/docs/kit/types#app.d.ts
import type { SupabaseClient, Session } from '@supabase/supabase-js';
import type { Database } from '$lib/types/database';

declare global {
	namespace App {
		interface Error {
			message: string;
			code?: string;
		}
		interface Locals {
			supabase: any;
			safeGetSession: () => Promise<{
				session: Session | null;
				user: import('@supabase/supabase-js').User | null;
			}>;
			session: Session | null;
			user: import('@supabase/supabase-js').User | null;
		}
		interface PageData {
			session: Session | null;
			user: import('@supabase/supabase-js').User | null;
		}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
