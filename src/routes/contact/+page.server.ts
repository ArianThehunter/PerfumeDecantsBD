import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { logger } from '$lib/services/logger';

export const load: PageServerLoad = async ({ parent }) => {
  const layoutData = await parent();
  return {
    contactSettings: layoutData.settings?.contact_page || {}
  };
};

export const actions: Actions = {
  submitMessage: async ({ request, locals }) => {
    const supabase = locals.supabase as any;
    const formData = await request.formData();

    const name = formData.get('name') as string;
    const email = formData.get('email') as string;
    const subject = formData.get('subject') as string;
    const message = formData.get('message') as string;

    if (!name || !email || !subject || !message) {
      return fail(400, { message: 'All fields are required' });
    }

    const { error } = await supabase
      .from('contact_messages')
      .insert({
        name,
        email,
        subject,
        message,
        is_read: false,
        created_at: new Date().toISOString()
      });

    if (error) {
      console.error('Failed to submit contact message:', error);
      return fail(500, { message: 'An internal error occurred. Could not submit your message at this time.' });
    }

    // Log contact message submission success
    logger.info('Contact form submitted', { name, email, subject });

    return { success: true };
  }
};
