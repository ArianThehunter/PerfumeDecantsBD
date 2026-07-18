import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase as any;

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

  // 5. Completed Revenue calculation (ONLY completed orders)
  const { data: completedOrdersData } = await supabase
    .from('orders')
    .select('total')
    .eq('status', 'completed');
  const revenue = completedOrdersData?.reduce((sum: number, item: any) => sum + Number(item.total), 0) || 0;

  // 6. Daily Completed Revenue (completed orders today)
  const todayStart = new Date();
  todayStart.setHours(0, 0, 0, 0);
  const { data: dailyOrders } = await supabase
    .from('orders')
    .select('total')
    .eq('status', 'completed')
    .gte('created_at', todayStart.toISOString());
  const dailyRevenue = dailyOrders?.reduce((sum: number, item: any) => sum + Number(item.total), 0) || 0;

  // 7. Monthly Completed Revenue (completed orders this month)
  const firstDayOfMonth = new Date();
  firstDayOfMonth.setDate(1);
  firstDayOfMonth.setHours(0, 0, 0, 0);
  const { data: monthlyOrders } = await supabase
    .from('orders')
    .select('total')
    .eq('status', 'completed')
    .gte('created_at', firstDayOfMonth.toISOString());
  const monthlyRevenue = monthlyOrders?.reduce((sum: number, item: any) => sum + Number(item.total), 0) || 0;

  // 8. Weekly aggregation for sales trend (completed orders in the last 30 days)
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  thirtyDaysAgo.setHours(0, 0, 0, 0);
  const { data: trendOrders } = await supabase
    .from('orders')
    .select('total, created_at')
    .eq('status', 'completed')
    .gte('created_at', thirtyDaysAgo.toISOString());

  const weeklySales = [
    { day: 'W1', amount: 0 },
    { day: 'W2', amount: 0 },
    { day: 'W3', amount: 0 },
    { day: 'W4', amount: 0 }
  ];

  if (trendOrders) {
    const nowMs = new Date().getTime();
    const oneDayMs = 24 * 60 * 60 * 1000;
    trendOrders.forEach((ord: any) => {
      const orderTime = new Date(ord.created_at).getTime();
      const daysAgo = (nowMs - orderTime) / oneDayMs;
      if (daysAgo <= 7) {
        weeklySales[3].amount += Number(ord.total);
      } else if (daysAgo <= 14) {
        weeklySales[2].amount += Number(ord.total);
      } else if (daysAgo <= 21) {
        weeklySales[1].amount += Number(ord.total);
      } else if (daysAgo <= 30) {
        weeklySales[0].amount += Number(ord.total);
      }
    });
  }

  // 9. Recent Orders
  const { data: recentOrders } = await supabase
    .from('orders')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(5);

  // 10. Low Stock Products (Dynamic Configurable Threshold)
  const { data: inventorySettings } = await supabase
    .from('settings')
    .select('value')
    .eq('key', 'inventory_settings')
    .single();

  const threshold = inventorySettings?.value?.low_stock_threshold !== undefined
    ? Number(inventorySettings.value.low_stock_threshold)
    : 5;

  const { data: lowStockProducts } = await supabase
    .from('products')
    .select('*')
    .lte('stock_quantity', threshold)
    .order('stock_quantity', { ascending: true })
    .limit(5);

  // 11. Recent Cancelled Orders for Notifications
  const { data: cancelledOrders } = await supabase
    .from('orders')
    .select('id, order_number, cancelled_at')
    .eq('status', 'cancelled')
    .order('cancelled_at', { ascending: false, nullsFirst: false })
    .limit(3);

  return {
    stats: {
      totalProducts: totalProducts || 0,
      totalOrders: totalOrders || 0,
      pendingOrders: pendingOrders || 0,
      completedOrders: completedOrders || 0,
      revenue,
      dailyRevenue,
      monthlyRevenue
    },
    weeklySales,
    recentOrders: recentOrders || [],
    lowStockProducts: lowStockProducts || [],
    cancelledOrders: cancelledOrders || []
  };
};
