import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
  const supabase = locals.supabase;
  const user = locals.user;

  if (!user) {
    throw error(401, 'Unauthorized');
  }

  // Load order details
  const { data: order, error: orderErr } = await supabase
    .from('orders')
    .select('*')
    .eq('id', params.id)
    .single();

  if (orderErr || !order) {
    throw error(404, 'Order not found');
  }

  // Check if order belongs to user or user is admin
  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single();

  const isAdmin = profile?.role === 'admin';
  if (order.user_id !== user.id && !isAdmin) {
    throw error(403, 'Forbidden');
  }

  // Load items in order
  const { data: items } = await supabase
    .from('order_items')
    .select('*')
    .eq('order_id', order.id);

  return {
    order,
    items: items || []
  };
};
