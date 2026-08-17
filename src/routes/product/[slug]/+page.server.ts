import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals, setHeaders }) => {
  const supabase = locals.supabase;

  // Set Edge CDN caching headers for product detail pages
  setHeaders({
    'cache-control': 'public, max-age=60, s-maxage=300, stale-while-revalidate=600'
  });

  // Fetch product detail with images and category
  const { data: product, error: err } = await supabase
    .from('products')
    .select('*, product_images(*), categories(*)')
    .eq('slug', params.slug)
    .eq('status', 'active')
    .single();

  if (err || !product) {
    throw error(404, {
      message: 'Product not found',
      code: 'NOT_FOUND'
    });
  }

  // Fetch related products (same category or same brand)
  const { data: relatedProducts } = await supabase
    .from('products')
    .select('*, product_images(*)')
    .eq('status', 'active')
    .neq('id', product.id)
    .or(`category_id.eq.${product.category_id},brand.eq.${product.brand}`)
    .limit(4);

  return {
    product,
    relatedProducts: relatedProducts || []
  };
};
