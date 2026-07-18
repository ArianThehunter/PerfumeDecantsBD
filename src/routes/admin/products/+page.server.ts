import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase;

  const { data: products } = await supabase
    .from('products')
    .select('*, product_images(*)')
    .order('created_at', { ascending: false });

  return {
    products: products || []
  };
};

export const actions: Actions = {
  deleteProduct: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();
    const id = formData.get('id') as string;

    if (!id) {
      return fail(400, { message: 'Product ID is required' });
    }

    const { error } = await supabase
      .from('products')
      .delete()
      .eq('id', id);

    if (error) {
      console.error('Failed to delete product:', error);
      return fail(500, { message: 'An internal database error occurred. Could not delete product.' });
    }

    return { success: true };
  }
};
