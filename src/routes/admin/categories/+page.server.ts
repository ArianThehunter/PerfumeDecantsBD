import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase;

  const { data: categories } = await supabase
    .from('categories')
    .select('*')
    .order('display_order', { ascending: true });

  return {
    categories: categories || []
  };
};

export const actions: Actions = {
  createCategory: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();

    const name = formData.get('name') as string;
    const slug = formData.get('slug') as string;
    const description = formData.get('description') as string;
    const imageUrl = formData.get('imageUrl') as string;
    const displayOrder = Number(formData.get('displayOrder')) || 0;

    if (!name || !slug) {
      return fail(400, { message: 'Name and slug are required' });
    }

    const { error } = await supabase
      .from('categories')
      .insert({
        name,
        slug,
        description: description || null,
        image_url: imageUrl || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=600',
        display_order: displayOrder
      });

    if (error) {
      return fail(500, { message: error.message });
    }

    return { success: true };
  },

  updateCategory: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();

    const id = formData.get('id') as string;
    const name = formData.get('name') as string;
    const slug = formData.get('slug') as string;
    const description = formData.get('description') as string;
    const imageUrl = formData.get('imageUrl') as string;
    const displayOrder = Number(formData.get('displayOrder')) || 0;

    if (!id || !name || !slug) {
      return fail(400, { message: 'Name, slug and ID are required' });
    }

    const { error } = await supabase
      .from('categories')
      .update({
        name,
        slug,
        description: description || null,
        image_url: imageUrl || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=600',
        display_order: displayOrder,
        updated_at: new Date().toISOString()
      })
      .eq('id', id);

    if (error) {
      return fail(500, { message: error.message });
    }

    return { success: true };
  },

  deleteCategory: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();
    const id = formData.get('id') as string;

    const { error } = await supabase
      .from('categories')
      .delete()
      .eq('id', id);

    if (error) {
      return fail(500, { message: error.message });
    }

    return { success: true };
  }
};
