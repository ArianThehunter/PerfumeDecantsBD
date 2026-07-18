import { error, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { logger } from '$lib/services/logger';

export const load: PageServerLoad = async ({ params, locals }) => {
  const supabase = locals.supabase as any;
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

export const actions: Actions = {
  cancelOrder: async ({ params, locals }) => {
    const supabase = locals.supabase as any;
    const user = locals.user;

    if (!user) {
      return fail(401, { message: 'Unauthorized' });
    }

    // Load order to verify ownership and status
    const { data: order, error: fetchErr } = await supabase
      .from('orders')
      .select('status, user_id')
      .eq('id', params.id)
      .single();

    if (fetchErr || !order) {
      return fail(404, { message: 'Order not found' });
    }

    if (order.user_id !== user.id) {
      return fail(403, { message: 'You are not authorized to cancel this order.' });
    }

    if (order.status !== 'pending' && order.status !== 'confirmed') {
      return fail(400, { message: 'This order is already being processed and cannot be cancelled.' });
    }

    // Cancel order in database
    const { error: updateErr } = await supabase
      .from('orders')
      .update({
        status: 'cancelled',
        cancelled_at: new Date().toISOString()
      })
      .eq('id', params.id);

    if (updateErr) {
      console.error('Failed to cancel order:', updateErr);
      return fail(500, { message: 'An internal error occurred. Could not cancel order. Please try again.' });
    }

    // Log order cancellation success
    logger.info('Order cancelled by customer', { orderId: params.id }, user.id, user.email);

    return { success: true };
  }
};
