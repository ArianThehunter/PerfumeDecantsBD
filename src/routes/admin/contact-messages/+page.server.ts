import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ url, locals }) => {
  const supabase = locals.supabase as any;
  const search = url.searchParams.get('search') || '';

  let query = supabase
    .from('contact_messages')
    .select('*')
    .order('created_at', { ascending: false });

  if (search) {
    query = query.or(`name.ilike.%${search}%,email.ilike.%${search}%,subject.ilike.%${search}%,message.ilike.%${search}%`);
  }

  const { data: messages, error } = await query;

  if (error) {
    console.error('Failed to load contact messages:', error);
    return {
      messages: [],
      error: 'An internal error occurred while loading contact messages.'
    };
  }

  return {
    messages: messages || [],
    search
  };
};

export const actions: Actions = {
  markRead: async ({ request, locals }) => {
    const supabase = locals.supabase as any;
    const formData = await request.formData();
    const id = formData.get('id') as string;

    if (!id) return fail(400, { message: 'Message ID is required' });

    const { error } = await supabase
      .from('contact_messages')
      .update({ is_read: true })
      .eq('id', id);

    if (error) {
      console.error('Failed to mark message as read:', error);
      return fail(500, { message: 'An internal error occurred while updating the message.' });
    }
    return { success: true };
  },

  markUnread: async ({ request, locals }) => {
    const supabase = locals.supabase as any;
    const formData = await request.formData();
    const id = formData.get('id') as string;

    if (!id) return fail(400, { message: 'Message ID is required' });

    const { error } = await supabase
      .from('contact_messages')
      .update({ is_read: false })
      .eq('id', id);

    if (error) {
      console.error('Failed to mark message as unread:', error);
      return fail(500, { message: 'An internal error occurred while updating the message.' });
    }
    return { success: true };
  },

  deleteMessage: async ({ request, locals }) => {
    const supabase = locals.supabase as any;
    const formData = await request.formData();
    const id = formData.get('id') as string;

    if (!id) return fail(400, { message: 'Message ID is required' });

    const { error } = await supabase
      .from('contact_messages')
      .delete()
      .eq('id', id);

    if (error) {
      console.error('Failed to delete message:', error);
      return fail(500, { message: 'An internal error occurred while deleting the message.' });
    }
    return { success: true };
  }
};
