import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
  const supabase = locals.supabase;

  // Fetch order details
  const { data: order, error: orderErr } = await supabase
    .from('orders')
    .select('*, profiles(full_name, email, phone)')
    .eq('id', params.id)
    .single();

  if (orderErr || !order) {
    throw fail(404, { message: 'Order not found' });
  }

  // Fetch items in order
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
  updateStatus: async ({ request, params, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();
    const status = formData.get('status') as string;

    if (!status) {
      return fail(400, { message: 'Status is required' });
    }

    const { error } = await supabase
      .from('orders')
      .update({
        status,
        updated_at: new Date().toISOString()
      })
      .eq('id', params.id);

    if (error) {
      return fail(500, { message: error.message });
    }

    return { success: true };
  }
};
