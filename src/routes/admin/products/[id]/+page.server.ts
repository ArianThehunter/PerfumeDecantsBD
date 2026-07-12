import { fail, redirect } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
  const supabase = locals.supabase;

  // Load product
  const { data: product, error } = await supabase
    .from('products')
    .select('*, product_images(*)')
    .eq('id', params.id)
    .single();

  if (error || !product) {
    throw fail(404, { message: 'Product not found' });
  }

  // Load categories
  const { data: categories } = await supabase
    .from('categories')
    .select('*')
    .order('display_order', { ascending: true });

  return {
    product,
    categories: categories || []
  };
};

export const actions: Actions = {
  updateProduct: async ({ request, params, locals }) => {
    const supabase = locals.supabase;
    const formData = await request.formData();

    const name = formData.get('name') as string;
    const brand = formData.get('brand') as string;
    const slug = formData.get('slug') as string;
    const categoryId = formData.get('categoryId') as string;
    const shortDesc = formData.get('shortDesc') as string;
    const description = formData.get('description') as string;
    const price = Number(formData.get('price')) || 0;
    const discountPriceVal = formData.get('discountPrice');
    const discountPrice = discountPriceVal ? Number(discountPriceVal) : null;
    const stockQuantity = Number(formData.get('stockQuantity')) || 0;
    const gender = formData.get('gender') as string;
    const status = formData.get('status') as string;
    
    // Flags
    const isFeatured = formData.get('isFeatured') === 'on';
    const isBestseller = formData.get('isBestseller') === 'on';
    const isNewArrival = formData.get('isNewArrival') === 'on';

    // Parse notes
    const topNotesRaw = formData.get('topNotes') as string;
    const middleNotesRaw = formData.get('middleNotes') as string;
    const baseNotesRaw = formData.get('baseNotes') as string;

    const topNotes = topNotesRaw ? topNotesRaw.split(',').map((n) => n.trim()) : [];
    const middleNotes = middleNotesRaw ? middleNotesRaw.split(',').map((n) => n.trim()) : [];
    const baseNotes = baseNotesRaw ? baseNotesRaw.split(',').map((n) => n.trim()) : [];

    // Sizes
    const sizesJson = formData.get('sizesJson') as string;
    let sizes = null;
    if (sizesJson) {
      try {
        sizes = JSON.parse(sizesJson);
      } catch (e) {
        return fail(400, { message: 'Invalid sizes format' });
      }
    }

    // Image URL
    const imageUrl = formData.get('imageUrl') as string;
    const imageFile = formData.get('imageFile') as File;

    if (!name || !brand || !slug) {
      return fail(400, { message: 'Name, brand and slug are required' });
    }

    // Update Product
    const { error: prodError } = await supabase
      .from('products')
      .update({
        name,
        brand,
        slug,
        category_id: categoryId || null,
        short_description: shortDesc || null,
        description: description || null,
        price,
        discount_price: discountPrice,
        stock_quantity: stockQuantity,
        gender: gender as any,
        status: status as any,
        is_featured: isFeatured,
        is_bestseller: isBestseller,
        is_new_arrival: isNewArrival,
        top_notes: topNotes,
        middle_notes: middleNotes,
        base_notes: baseNotes,
        sizes: sizes as any,
        updated_at: new Date().toISOString()
      })
      .eq('id', params.id);

    if (prodError) {
      return fail(500, { message: prodError.message });
    }

    let finalImageUrl = imageUrl || '';

    // Handle local image file upload if provided
    if (imageFile && imageFile.size > 0) {
      const fileExt = imageFile.name.split('.').pop();
      const fileName = `${params.id}/${Date.now()}.${fileExt}`;
      const { data: uploadData, error: uploadError } = await supabase.storage
        .from('products')
        .upload(fileName, imageFile, {
          cacheControl: '3600',
          upsert: true
        });

      if (!uploadError && uploadData) {
        const { data: publicUrlData } = supabase.storage
          .from('products')
          .getPublicUrl(uploadData.path);
        
        if (publicUrlData) {
          finalImageUrl = publicUrlData.publicUrl;
        }
      } else {
        console.error('Storage upload error:', uploadError);
      }
    }

    // Update main image if provided/uploaded
    if (finalImageUrl) {
      // Check if primary image exists
      const { data: existingImg } = await supabase
        .from('product_images')
        .select('id')
        .eq('product_id', params.id)
        .eq('is_primary', true)
        .single();

      if (existingImg) {
        await supabase
          .from('product_images')
          .update({ url: finalImageUrl })
          .eq('id', existingImg.id);
      } else {
        await supabase.from('product_images').insert({
          product_id: params.id,
          url: finalImageUrl,
          alt_text: `${name} image`,
          is_primary: true,
          display_order: 1
        });
      }
    }

    throw redirect(303, '/admin/products');
  }
};
