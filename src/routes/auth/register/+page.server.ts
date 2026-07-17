import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
  register: async ({ request, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();
    
    const fullName = formData.get('fullName') as string;
    const email = formData.get('email') as string;
    const phone = formData.get('phone') as string;
    const password = formData.get('password') as string;
    const confirmPassword = formData.get('confirmPassword') as string;

    // Required fields cannot be empty
    if (!fullName || !email || !phone || !password || !confirmPassword) {
      return fail(400, { message: 'All fields are required.' });
    }

    if (email.trim().toLowerCase() === 'admin@perfumedecantsbd.com') {
      return fail(400, { message: 'Registration is restricted for this email address.' });
    }

    if (password !== confirmPassword) {
      return fail(400, { message: 'Passwords do not match.' });
    }

    // Phone validation:
    // Must contain exactly 11 digits
    // Must begin with 01
    // Only numeric characters are allowed
    // Spaces, dashes and letters are not allowed
    const phoneRegex = /^01\d{9}$/;
    if (!phoneRegex.test(phone)) {
      return fail(400, { message: 'Phone number must start with 01, contain exactly 11 digits, and only contain numeric characters.' });
    }

    // Register user
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
          phone: phone
        }
      }
    });

    if (error) {
      return fail(400, { message: error.message || 'Failed to register.' });
    }

    return { success: true };
  }
};
