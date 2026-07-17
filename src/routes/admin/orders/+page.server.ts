import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase;

  const { data: orders } = await supabase
    .from('orders')
    .select('*')
    .order('created_at', { ascending: false });

  return {
    orders: orders || []
  };
};
