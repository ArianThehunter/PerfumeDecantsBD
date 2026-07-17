import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase;
  const user = locals.user;

  if (!user) return { addresses: [] };

  const { data: addresses } = await supabase
    .from('addresses')
    .select('*')
    .eq('user_id', user.id)
    .order('is_default', { ascending: false })
    .order('created_at', { ascending: false });

  return {
    addresses: addresses || []
  };
};

export const actions: Actions = {
  addAddress: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const user = locals.user;

    if (!user) return fail(401, { message: 'Unauthorized' });

    const formData = await request.formData();
    const label = formData.get('label') as string;
    const fullName = formData.get('fullName') as string;
    const phone = formData.get('phone') as string;
    const addressLine1 = formData.get('addressLine1') as string;
    const addressLine2 = formData.get('addressLine2') as string;
    const city = formData.get('city') as string;
    const district = formData.get('district') as string;
    const postalCode = formData.get('postalCode') as string;
    const isDefault = formData.get('isDefault') === 'on';

    // If isDefault is checked, reset other defaults first
    if (isDefault) {
      await supabase
        .from('addresses')
        .update({ is_default: false })
        .eq('user_id', user.id);
    }

    // Insert new address
    const { error } = await supabase
      .from('addresses')
      .insert({
        user_id: user.id,
        label,
        full_name: fullName,
        phone,
        address_line_1: addressLine1,
        address_line_2: addressLine2 || null,
        city,
        district,
        postal_code: postalCode,
        is_default: isDefault
      });

    if (error) {
      return fail(500, { message: error.message });
    }

    return { success: true };
  },

  deleteAddress: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const user = locals.user;

    if (!user) return fail(401, { message: 'Unauthorized' });

    const formData = await request.formData();
    const id = formData.get('id') as string;

    const { error } = await supabase
      .from('addresses')
      .delete()
      .eq('id', id)
      .eq('user_id', user.id);

    if (error) {
      return fail(500, { message: error.message });
    }

    return { success: true };
  },

  setDefault: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const user = locals.user;

    if (!user) return fail(401, { message: 'Unauthorized' });

    const formData = await request.formData();
    const id = formData.get('id') as string;

    // Reset others
    await supabase
      .from('addresses')
      .update({ is_default: false })
      .eq('user_id', user.id);

    // Set this as default
    const { error } = await supabase
      .from('addresses')
      .update({ is_default: true })
      .eq('id', id)
      .eq('user_id', user.id);

    if (error) {
      return fail(500, { message: error.message });
    }

    return { success: true };
  }
};
