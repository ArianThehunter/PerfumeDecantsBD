import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase;
  const user = locals.user;

  if (!user) return { profile: null };

  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user.id)
    .single();

  // Check for any unclaimed guest orders matching the email of the logged-in user
  const { data: unclaimedCount } = await supabase.rpc('count_unclaimed_guest_orders', {
    p_email: user.email
  });

  return {
    profile,
    unclaimedCount: unclaimedCount ? Number(unclaimedCount) : 0
  };
};

export const actions: Actions = {
  updateProfile: async ({ request, locals }) => {
    const supabase = locals.supabase as any;
    const user = locals.user;

    if (!user) return fail(401, { message: 'Unauthorized' });

    const formData = await request.formData();
    const fullName = formData.get('fullName') as string;
    const phone = formData.get('phone') as string;

    if (!fullName || !fullName.trim()) {
      return fail(400, { message: 'Full Name is required.' });
    }

    if (!phone || !/^01\d{9}$/.test(phone)) {
      return fail(400, { message: 'Phone number must start with 01 and contain exactly 11 digits.' });
    }

    const { error } = await supabase
      .from('profiles')
      .update({
        full_name: fullName.trim(),
        phone: phone,
        updated_at: new Date().toISOString()
      })
      .eq('id', user.id);

    if (error) {
      console.error('Failed to update profile details:', error);
      return fail(500, { message: 'An internal error occurred while updating your profile. Please try again.' });
    }

    return { success: true };
  },

  claimGuestOrders: async ({ locals }) => {
    const supabase = locals.supabase;
    const user = locals.user;

    if (!user || !user.email) return fail(401, { message: 'Unauthorized' });

    const { data: claimedCount, error } = await supabase.rpc('claim_guest_orders', {
      p_user_id: user.id,
      p_email: user.email
    });

    if (error) {
      console.error('Failed to claim guest orders:', error);
      return fail(500, { message: 'An internal error occurred while associating your previous orders.' });
    }

    return { success: true, claimedCount };
  }
};
