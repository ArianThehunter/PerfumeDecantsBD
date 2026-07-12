import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, locals }) => {
  const supabase = locals.supabase;

  // Read query params
  const search = url.searchParams.get('search') || '';
  const categorySlug = url.searchParams.get('category') || '';
  const brand = url.searchParams.get('brand') || '';
  const gender = url.searchParams.get('gender') || '';
  const minPrice = Number(url.searchParams.get('min_price')) || 0;
  const maxPrice = Number(url.searchParams.get('max_price')) || 10000;
  const sort = url.searchParams.get('sort') || 'popular';
  const page = Number(url.searchParams.get('page')) || 1;
  const perPage = 12;

  // 1. Fetch Categories for filters
  const { data: categories } = await supabase
    .from('categories')
    .select('id, name, slug')
    .order('display_order', { ascending: true });

  // 2. Fetch distinct brands for filter checklist
  // (Using a simple query since PG doesn't have native "DISTINCT ON" direct endpoint in Supabase easily without RPC, but we can do simple select)
  const { data: allProductsForBrands } = await supabase
    .from('products')
    .select('brand')
    .eq('status', 'active');
  const brands = Array.from(new Set(allProductsForBrands?.map(p => p.brand) || []));

  // 3. Build main query
  let query = supabase
    .from('products')
    .select('*, product_images(*)', { count: 'exact' })
    .eq('status', 'active');

  if (search) {
    query = query.or(`name.ilike.%${search}%,brand.ilike.%${search}%,description.ilike.%${search}%`);
  }

  if (categorySlug) {
    // Resolve category first
    const { data: cat } = await supabase
      .from('categories')
      .select('id')
      .eq('slug', categorySlug)
      .single();

    if (cat) {
      query = query.eq('category_id', cat.id);
    }
  }

  if (brand) {
    query = query.eq('brand', brand);
  }

  if (gender) {
    query = query.eq('gender', gender);
  }

  if (minPrice > 0) {
    query = query.gte('price', minPrice);
  }

  if (maxPrice < 10000) {
    query = query.lte('price', maxPrice);
  }

  // Sorting
  if (sort === 'newest') {
    query = query.order('created_at', { ascending: false });
  } else if (sort === 'price_asc') {
    query = query.order('price', { ascending: true });
  } else if (sort === 'price_desc') {
    query = query.order('price', { ascending: false });
  } else {
    // Default: popular / rating
    query = query.order('rating', { ascending: false }).order('review_count', { ascending: false });
  }

  // Pagination
  const from = (page - 1) * perPage;
  const to = from + perPage - 1;
  query = query.range(from, to);

  const { data: products, count, error } = await query;

  return {
    products: products || [],
    totalCount: count || 0,
    categories: categories || [],
    brands: brands || [],
    filters: {
      search,
      category: categorySlug,
      brand,
      gender,
      minPrice,
      maxPrice,
      sort,
      page,
      perPage
    }
  };
};
