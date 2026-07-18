import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { env } from '$env/dynamic/private';
import { createClient } from '@supabase/supabase-js';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ url, locals }) => {
  const orderId = url.searchParams.get('orderId');
  const phone = url.searchParams.get('phone');

  if (!orderId || !phone) {
    return {
      order: null,
      items: [],
      searched: false
    };
  }

  // Sanitize and validate inputs
  const sanitizedOrderId = orderId.trim();
  const sanitizedPhone = phone.trim();

  if (!sanitizedOrderId || !sanitizedPhone) {
    return fail(400, { message: 'Order ID and Phone Number are required.' });
  }

  const supabase = locals.supabase;

  // Dual-layer secure query:
  // 1. Try calling the SECURITY DEFINER RPC first (standard production-ready way)
  const { data: rpcOrder, error: rpcErr } = await supabase.rpc('track_guest_order', {
    p_order_identifier: sanitizedOrderId,
    p_phone: sanitizedPhone
  });

  if (!rpcErr && rpcOrder && rpcOrder.length > 0) {
    const orderObj = rpcOrder[0];
    const { data: rpcItems } = await supabase.rpc('track_guest_order_items', {
      p_order_identifier: sanitizedOrderId,
      p_phone: sanitizedPhone
    });

    return {
      order: orderObj,
      items: rpcItems || [],
      searched: true
    };
  }

  // 2. Fallback to Service Role Client if environment variable is set
  if (env.SUPABASE_SERVICE_ROLE_KEY) {
    const adminClient = createClient(PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY, {
      auth: { persistSession: false }
    });

    // Query order
    const { data: order, error: orderErr } = await adminClient
      .from('orders')
      .select('*')
      .or(`order_number.eq.${sanitizedOrderId},id.eq.${sanitizedOrderId}`)
      .single();

    if (!orderErr && order) {
      // Validate phone matches shipping address snapshot
      const shippingAddress = order.shipping_address as any;
      if (shippingAddress && shippingAddress.phone === sanitizedPhone) {
        // Query items
        const { data: items } = await adminClient
          .from('order_items')
          .select('*')
          .eq('order_id', order.id);

        return {
          order,
          items: items || [],
          searched: true
        };
      }
    }
  }

  // If no match found or validation failed, return error status
  return {
    order: null,
    items: [],
    searched: true,
    error: 'No order found with the provided Order ID and Phone Number.'
  };
};

export const actions: Actions = {
  track: async ({ request }) => {
    const formData = await request.formData();
    const orderId = formData.get('orderId') as string;
    const phone = formData.get('phone') as string;

    if (!orderId || !phone) {
      return fail(400, { message: 'Order ID and Phone Number are required.' });
    }

    return {
      orderId,
      phone
    };
  }
};
