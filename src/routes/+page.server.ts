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

  // Load hero slides setting
  const { data: heroSetting } = await supabase
    .from('settings')
    .select('value')
    .eq('key', 'hero_slides')
    .single();

  let heroProducts: any[] = [];
  if (heroSetting?.value?.product_ids && Array.isArray(heroSetting.value.product_ids) && heroSetting.value.product_ids.length > 0) {
    const { data: slides } = await supabase
      .from('products')
      .select('*, product_images(*)')
      .in('id', heroSetting.value.product_ids)
      .eq('status', 'active');
    
    // Sort based on the selected order if possible, or just use DB return order
    heroProducts = slides || [];
  }

  return {
    featuredProducts: featured || [],
    bestSellers: bestSellers || [],
    categories: categories || [],
    heroProducts
  };
};
