import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase;

  // 1. Total Products
  const { count: totalProducts } = await supabase
    .from('products')
    .select('*', { count: 'exact', head: true });

  // 2. Total Orders
  const { count: totalOrders } = await supabase
    .from('orders')
    .select('*', { count: 'exact', head: true });

  // 3. Pending Orders
  const { count: pendingOrders } = await supabase
    .from('orders')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'pending');

  // 4. Completed Orders
  const { count: completedOrders } = await supabase
    .from('orders')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'completed');

  // 5. Total Revenue (sum of orders that are not cancelled)
  const { data: revenueData } = await supabase
    .from('orders')
    .select('total')
    .neq('status', 'cancelled');
  const revenue = revenueData?.reduce((sum, item) => sum + Number(item.total), 0) || 0;

  // 6. Recent Orders
  const { data: recentOrders } = await supabase
    .from('orders')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(5);

  // 7. Low Stock Products
  const { data: lowStockProducts } = await supabase
    .from('products')
    .select('*')
    .lte('stock_quantity', 5)
    .order('stock_quantity', { ascending: true })
    .limit(5);

  return {
    stats: {
      totalProducts: totalProducts || 0,
      totalOrders: totalOrders || 0,
      pendingOrders: pendingOrders || 0,
      completedOrders: completedOrders || 0,
      revenue
    },
    recentOrders: recentOrders || [],
    lowStockProducts: lowStockProducts || []
  };
};
