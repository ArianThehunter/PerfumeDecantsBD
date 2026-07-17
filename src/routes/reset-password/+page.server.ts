import { error, redirect, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  const session = locals.session;
  
  if (!session) {
    return { valid: false };
  }

  try {
    // Decode access token to check AMR (Authentication Method References) for "recovery"
    const base64Url = session.access_token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = atob(base64);
    const payload = JSON.parse(jsonPayload);
    
    const isRecovery = payload.amr && payload.amr.some((item: any) => {
      if (typeof item === 'string') return item === 'recovery';
      return item && item.method === 'recovery';
    });

    if (!isRecovery) {
      return { valid: false };
    }

    return { valid: true };
  } catch (err) {
    return { valid: false };
  }
};

export const actions: Actions = {
  resetPassword: async ({ request, locals }) => {
    const supabase = locals.supabase as any;
    const session = locals.session;

    if (!session) {
      return fail(401, { message: 'Session has expired or is invalid.' });
    }

    const formData = await request.formData();
    const password = formData.get('password') as string;
    const confirmPassword = formData.get('confirmPassword') as string;

    if (!password || !confirmPassword) {
      return fail(400, { message: 'Passwords cannot be empty.' });
    }

    if (password !== confirmPassword) {
      return fail(400, { message: 'Passwords do not match.' });
    }

    // Server-side password strength validation
    const minLength = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasDigit = /[0-9]/.test(password);
    const hasSpecial = /[^A-Za-z0-9]/.test(password);

    if (!minLength || !hasUpper || !hasLower || !hasDigit || !hasSpecial) {
      return fail(400, { message: 'Password does not meet the security requirements.' });
    }

    // Call Supabase updateUser to update password
    const { error: updateErr } = await supabase.auth.updateUser({ password });

    if (updateErr) {
      return fail(400, { message: updateErr.message || 'Failed to update password.' });
    }

    // Sign out to clear the recovery session cookies
    await supabase.auth.signOut();

    return { success: true };
  }
};
