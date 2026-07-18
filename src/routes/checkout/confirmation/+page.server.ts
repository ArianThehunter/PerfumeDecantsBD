import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, locals, cookies }) => {
  const supabase = locals.supabase as any;
  const user = locals.user;

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

  // If order belongs to a user, make sure that user matches
  if (order.user_id) {
    if (!user || order.user_id !== user.id) {
      throw error(403, 'Forbidden');
    }
  } else {
    // If guest checkout, verify using the temporary session cookie
    const placedOrderId = cookies.get('placed_order_id');
    if (placedOrderId !== order.id) {
      throw error(403, 'Forbidden');
    }
  }

  return {
    order,
    isAuthenticated: !!user
  };
};
