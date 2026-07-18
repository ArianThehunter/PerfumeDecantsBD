import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { logger } from '$lib/services/logger';

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

    // 1. Fetch images to identify storage files before deleting DB rows
    const { data: images } = await supabase
      .from('product_images')
      .select('url')
      .eq('product_id', id);

    const storageFiles: string[] = [];
    if (images) {
      images.forEach((img: any) => {
        const parts = img.url.split('/storage/v1/object/public/products/');
        if (parts.length > 1) {
          storageFiles.push(decodeURIComponent(parts[1]));
        }
      });
    }

    // 2. Delete product row (Cascades and deletes matching product_images rows in database)
    const { error } = await supabase
      .from('products')
      .delete()
      .eq('id', id);

    if (error) {
      console.error('Failed to delete product:', error);
      return fail(500, { message: 'An internal database error occurred. Could not delete product.' });
    }

    // 3. Clean up the storage files asynchronously
    if (storageFiles.length > 0) {
      const { error: storageErr } = await supabase.storage
        .from('products')
        .remove(storageFiles);
      if (storageErr) {
        console.error('Failed to clean up product images from storage:', storageErr);
      }
    }

    // Log product deletion success
    logger.info('Product deleted', { productId: id });

    return { success: true };
  }
};
