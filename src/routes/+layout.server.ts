import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  const session = locals.session;
  const user = locals.user;
  const supabase = locals.supabase;

  // Load general settings
  const { data: settingsData } = await supabase
    .from('settings')
    .select('*');

  const settings: Record<string, any> = {};
  if (settingsData) {
    settingsData.forEach((row: any) => {
      settings[row.key] = row.value;
    });
  }

  return {
    session,
    user,
    settings
  };
};
