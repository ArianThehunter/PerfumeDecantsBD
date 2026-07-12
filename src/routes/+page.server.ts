import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase;

  // Load featured products
  const { data: featured } = await supabase
    .from('products')
    .select('*, product_images(*)')
    .eq('status', 'active')
    .eq('is_featured', true)
    .order('display_order', { ascending: true })
    .limit(8);

  // Load best sellers
  const { data: bestSellers } = await supabase
    .from('products')
    .select('*, product_images(*)')
    .eq('status', 'active')
    .eq('is_bestseller', true)
    .order('display_order', { ascending: true })
    .limit(8);

  // Load categories
  const { data: categories } = await supabase
    .from('categories')
    .select('*')
    .order('display_order', { ascending: true });

  return {
    featuredProducts: featured || [],
    bestSellers: bestSellers || [],
    categories: categories || []
  };
};
