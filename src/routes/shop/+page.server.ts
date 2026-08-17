import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, locals, setHeaders }) => {
  const supabase = locals.supabase;

  // Set Edge CDN caching headers for catalog browsing
  setHeaders({
    'cache-control': 'public, max-age=60, s-maxage=180, stale-while-revalidate=300'
  });

  // Read query params
  const search = url.searchParams.get('search') || '';
  const categorySlug = url.searchParams.get('category') || '';
  const brand = url.searchParams.get('brand') || '';
  const gender = url.searchParams.get('gender') || '';
  const minPrice = Number(url.searchParams.get('min_price')) || 200;
  const maxPrice = Number(url.searchParams.get('max_price')) || 20000;
  const sort = url.searchParams.get('sort') || 'popular';
  const page = Number(url.searchParams.get('page')) || 1;
  const perPage = 12;

  // Execute filter metadata fetches concurrently
  const [categoriesRes, brandsRes] = await Promise.all([
    supabase
      .from('categories')
      .select('id, name, slug')
      .order('display_order', { ascending: true }),
    supabase
      .from('products')
      .select('brand')
      .eq('status', 'active')
  ]);

  const categories = categoriesRes.data || [];
  const brands = Array.from(new Set(brandsRes.data?.map((p: any) => p.brand) || []));

  // Build main product query
  let query = supabase
    .from('products')
    .select('*, product_images(*)', { count: 'exact' })
    .eq('status', 'active');

  if (search) {
    query = query.or(`name.ilike.%${search}%,brand.ilike.%${search}%,description.ilike.%${search}%`);
  }

  if (categorySlug) {
    const selectedCategory = categories.find((c: any) => c.slug === categorySlug);
    if (selectedCategory) {
      query = query.eq('category_id', selectedCategory.id);
    } else {
      const { data: cat } = await supabase
        .from('categories')
        .select('id')
        .eq('slug', categorySlug)
        .single();

      if (cat) {
        query = query.eq('category_id', cat.id);
      }
    }
  }

  if (brand) {
    query = query.eq('brand', brand);
  }

  if (gender) {
    query = query.eq('gender', gender);
  }

  query = query.gte('price', minPrice);
  query = query.lte('price', maxPrice);

  // Sorting
  if (sort === 'newest') {
    query = query.order('created_at', { ascending: false });
  } else if (sort === 'price_asc') {
    query = query.order('price', { ascending: true });
  } else if (sort === 'price_desc') {
    query = query.order('price', { ascending: false });
  } else {
    query = query.order('rating', { ascending: false }).order('review_count', { ascending: false });
  }

  // Pagination
  const from = (page - 1) * perPage;
  const to = from + perPage - 1;
  query = query.range(from, to);

  const { data: products, count } = await query;

  return {
    products: products || [],
    totalCount: count || 0,
    categories,
    brands,
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
