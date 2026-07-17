import { fail, redirect } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase as any;
  const user = locals.user;

  if (!user) {
    return {
      addresses: [],
      profile: null
    };
  }

  // Load saved addresses
  const { data: addresses } = await supabase
    .from('addresses')
    .select('*')
    .eq('user_id', user.id)
    .order('is_default', { ascending: false });

  // Load profile
  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user.id)
    .single();

  return {
    addresses: addresses || [],
    profile
  };
};

export const actions: Actions = {
  placeOrder: async ({ request, locals }) => {
    const supabase = locals.supabase as any;
    const user = locals.user;

    const formData = await request.formData();
    const addressId = formData.get('addressId') as string;
    const paymentMethod = formData.get('paymentMethod') as string;
    const notesInput = formData.get('notes') as string;
    const transactionId = formData.get('transactionId') as string;
    const cartItemsJson = formData.get('cartItems') as string;

    let notes = notesInput || null;
    if (paymentMethod === 'bank_transfer' && transactionId) {
      notes = `[bKash/Nagad TxnID: ${transactionId}]` + (notesInput ? ` \nNotes: ${notesInput}` : '');
    }

    // Parse cart items
    let cartItems = [];
    try {
      cartItems = JSON.parse(cartItemsJson);
    } catch (e) {
      return fail(400, { message: 'Invalid cart details' });
    }

    if (!cartItems || cartItems.length === 0) {
      return fail(400, { message: 'Your shopping cart is empty' });
    }

    // Resolve shipping address
    let shippingAddress = {};
    if (user && addressId && addressId !== 'new') {
      const { data: addr } = await supabase
        .from('addresses')
        .select('*')
        .eq('id', addressId)
        .eq('user_id', user.id)
        .single();
      
      if (addr) {
        shippingAddress = {
          full_name: addr.full_name,
          phone: addr.phone,
          email: user.email,
          address_line_1: addr.address_line_1,
          address_line_2: addr.address_line_2,
          city: addr.city,
          postal_code: addr.postal_code
        };
      } else {
        return fail(400, { message: 'Selected address not found' });
      }
    } else {
      // Manual entry address or Guest checkout
      const fullName = formData.get('fullName') as string;
      const phone = formData.get('phone') as string;
      const addressLine1 = formData.get('addressLine1') as string;
      const addressLine2 = formData.get('addressLine2') as string;
      const city = formData.get('city') as string;
      const postalCode = formData.get('postalCode') as string;
      const guestEmail = formData.get('guestEmail') as string;

      // Validate email for guest checkouts
      const orderEmail = user ? user.email : guestEmail;
      if (!orderEmail) {
        return fail(400, { message: 'Email address is required for checkout' });
      }

      if (!fullName || !phone || !addressLine1 || !city || !postalCode) {
        return fail(400, { message: 'All shipping address fields are required' });
      }

      shippingAddress = {
        full_name: fullName,
        phone: phone,
        email: orderEmail,
        address_line_1: addressLine1,
        address_line_2: addressLine2 || null,
        city: city,
        postal_code: postalCode
      };
    }

    // Calculate subtotal and shipping
    let subtotal = 0;
    for (const item of cartItems) {
      subtotal += item.unit_price * item.quantity;
    }
    const shippingCost = subtotal >= 5000 ? 0 : 120;
    const total = subtotal + shippingCost;

    // Validate and decrement stock
    for (const item of cartItems) {
      const { data: prod } = await supabase
        .from('products')
        .select('stock_quantity, name')
        .eq('id', item.product_id)
        .single();

      if (!prod || prod.stock_quantity < item.quantity) {
        return fail(400, { message: `Insufficient stock for product: ${prod?.name || 'Unknown'}` });
      }
    }

    // Insert Order
    const { data: order, error: orderErr } = await supabase
      .from('orders')
      .insert({
        user_id: user?.id || null,
        status: 'pending',
        subtotal,
        shipping_cost: shippingCost,
        total,
        payment_method: paymentMethod as any,
        shipping_address: shippingAddress as any,
        notes: notes || null
      })
      .select('id, order_number')
      .single();

    if (orderErr || !order) {
      return fail(500, { message: orderErr?.message || 'Failed to place order' });
    }

    // Insert Order Items and update stocks
    for (const item of cartItems) {
      // Insert item
      await supabase.from('order_items').insert({
        order_id: order.id,
        product_id: item.product_id,
        product_name: item.product_name,
        product_image: item.product_image,
        size: item.size,
        quantity: item.quantity,
        unit_price: item.unit_price,
        total_price: item.unit_price * item.quantity
      });

      // Update product stock
      const { data: currentProduct } = await supabase
        .from('products')
        .select('stock_quantity')
        .eq('id', item.product_id)
        .single();

      if (currentProduct) {
        const newStock = Math.max(0, currentProduct.stock_quantity - item.quantity);
        await supabase
          .from('products')
          .update({ stock_quantity: newStock })
          .eq('id', item.product_id);
      }
    }

    return { success: true, orderId: order.id, orderNumber: order.order_number };
  }
};
