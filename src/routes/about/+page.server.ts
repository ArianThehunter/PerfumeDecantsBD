import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ parent }) => {
  const layoutData = await parent();
  return {
    aboutSettings: layoutData.settings?.about_page || {}
  };
};
