import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals, setHeaders }) => {
  const supabase = locals.supabase;

  // Set high-performance Edge CDN caching headers for homepage delivery
  setHeaders({
    'cache-control': 'public, max-age=60, s-maxage=300, stale-while-revalidate=600'
  });

  // Execute all independent database queries concurrently in a single round-trip batch
  const [featuredRes, bestSellersRes, categoriesRes, heroSettingRes] = await Promise.all([
    supabase
      .from('products')
      .select('*, product_images(*)')
      .eq('status', 'active')
      .eq('is_featured', true)
      .order('display_order', { ascending: true })
      .limit(8),
    supabase
      .from('products')
      .select('*, product_images(*)')
      .eq('status', 'active')
      .eq('is_bestseller', true)
      .order('display_order', { ascending: true })
      .limit(8),
    supabase
      .from('categories')
      .select('*')
      .order('display_order', { ascending: true }),
    supabase
      .from('settings')
      .select('value')
      .eq('key', 'hero_slides')
      .single()
  ]);

  let heroProducts: any[] = [];
  const heroSetting = heroSettingRes.data;
  if (heroSetting?.value?.product_ids && Array.isArray(heroSetting.value.product_ids) && heroSetting.value.product_ids.length > 0) {
    const { data: slides } = await supabase
      .from('products')
      .select('*, product_images(*)')
      .in('id', heroSetting.value.product_ids)
      .eq('status', 'active');
    
    heroProducts = slides || [];
  }

  return {
    featuredProducts: featuredRes.data || [],
    bestSellers: bestSellersRes.data || [],
    categories: categoriesRes.data || [],
    heroProducts
  };
};
