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

  return {
    profile
  };
};

export const actions: Actions = {
  updateProfile: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const user = locals.user;

    if (!user) return fail(401, { message: 'Unauthorized' });

    const formData = await request.formData();
    const fullName = formData.get('fullName') as string;
    const phone = formData.get('phone') as string;

    const { error } = await supabase
      .from('profiles')
      .update({
        full_name: fullName,
        phone: phone,
        updated_at: new Date().toISOString()
      })
      .eq('id', user.id);

    if (error) {
      return fail(500, { message: error.message });
    }

    return { success: true };
  }
};
