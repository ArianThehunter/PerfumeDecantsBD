import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, locals }) => {
  const supabase = locals.supabase;
  const user = locals.user;

  if (!user) {
    throw error(401, 'Unauthorized');
  }

  const orderId = url.searchParams.get('id');
  if (!orderId) {
    throw error(400, 'Order ID is required');
  }

  const { data: order, error: orderErr } = await supabase
    .from('orders')
    .select('*')
    .eq('id', orderId)
    .single();

  if (orderErr || !order) {
    throw error(404, 'Order not found');
  }

  if (order.user_id !== user.id) {
    throw error(403, 'Forbidden');
  }

  return {
    order
  };
};
