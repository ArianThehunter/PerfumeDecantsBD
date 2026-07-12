import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const supabase = locals.supabase;

  const { data: settingsData } = await supabase
    .from('settings')
    .select('*');

  const settings: Record<string, any> = {};
  if (settingsData) {
    settingsData.forEach((row) => {
      settings[row.key] = row.value;
    });
  }

  return {
    settings
  };
};

export const actions: Actions = {
  updateFooter: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();

    const payload = {
      newsletter_title: formData.get('newsletter_title') as string,
      newsletter_desc: formData.get('newsletter_desc') as string,
      brand_desc: formData.get('brand_desc') as string,
      facebook_url: formData.get('facebook_url') as string,
      instagram_url: formData.get('instagram_url') as string,
      telegram_url: formData.get('telegram_url') as string,
      address: formData.get('address') as string,
      phone: formData.get('phone') as string,
      email: formData.get('email') as string,
      copyright: formData.get('copyright') as string
    };

    const { error } = await supabase
      .from('settings')
      .update({
        value: payload,
        updated_at: new Date().toISOString()
      })
      .eq('key', 'footer');

    if (error) return fail(500, { message: error.message });
    return { success: true };
  },

  updateAbout: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();

    const payload = {
      title: formData.get('title') as string,
      subtitle: formData.get('subtitle') as string,
      story_title: formData.get('story_title') as string,
      story_content_1: formData.get('story_content_1') as string,
      story_content_2: formData.get('story_content_2') as string,
      mission: formData.get('mission') as string,
      vision: formData.get('vision') as string,
      image_url: formData.get('image_url') as string
    };

    const { error } = await supabase
      .from('settings')
      .update({
        value: payload,
        updated_at: new Date().toISOString()
      })
      .eq('key', 'about_page');

    if (error) return fail(500, { message: error.message });
    return { success: true };
  },

  updateContact: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();

    const payload = {
      title: formData.get('title') as string,
      subtitle: formData.get('subtitle') as string,
      form_title: formData.get('form_title') as string,
      form_subtitle: formData.get('form_subtitle') as string,
      address: formData.get('address') as string,
      phone: formData.get('phone') as string,
      email: formData.get('email') as string,
      hours: formData.get('hours') as string
    };

    const { error } = await supabase
      .from('settings')
      .update({
        value: payload,
        updated_at: new Date().toISOString()
      })
      .eq('key', 'contact_page');

    if (error) return fail(500, { message: error.message });
    return { success: true };
  },

  updateShop: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();

    const payload = {
      title: formData.get('title') as string,
      subtitle: formData.get('subtitle') as string
    };

    const { error } = await supabase
      .from('settings')
      .update({
        value: payload,
        updated_at: new Date().toISOString()
      })
      .eq('key', 'shop_page');

    if (error) return fail(500, { message: error.message });
    return { success: true };
  }
};
