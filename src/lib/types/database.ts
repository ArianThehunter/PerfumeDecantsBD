// Database types for Supabase
// These types should ideally be generated using: supabase gen types typescript
// For now, we define them manually to match our schema

export type Json = string | number | boolean | null | { [key: string]: Json | undefined } | Json[];

export type OrderStatus = 'pending' | 'confirmed' | 'processing' | 'completed' | 'cancelled';
export type PaymentMethod = 'cod' | 'bank_transfer';
export type ProductStatus = 'active' | 'draft';
export type UserRole = 'user' | 'admin';
export type Gender = 'men' | 'women' | 'unisex';

export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          full_name: string | null;
          phone: string | null;
          avatar_url: string | null;
          role: UserRole;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          full_name?: string | null;
          phone?: string | null;
          avatar_url?: string | null;
          role?: UserRole;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          full_name?: string | null;
          phone?: string | null;
          avatar_url?: string | null;
          role?: UserRole;
          updated_at?: string;
        };
      };
      categories: {
        Row: {
          id: string;
          name: string;
          slug: string;
          description: string | null;
          image_url: string | null;
          display_order: number;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          name: string;
          slug: string;
          description?: string | null;
          image_url?: string | null;
          display_order?: number;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          name?: string;
          slug?: string;
          description?: string | null;
          image_url?: string | null;
          display_order?: number;
          updated_at?: string;
        };
      };
      products: {
        Row: {
          id: string;
          name: string;
          slug: string;
          brand: string;
          category_id: string | null;
          short_description: string | null;
          description: string | null;
          top_notes: string[] | null;
          middle_notes: string[] | null;
          base_notes: string[] | null;
          price: number;
          discount_price: number | null;
          sizes: Json | null;
          stock_quantity: number;
          rating: number;
          review_count: number;
          is_featured: boolean;
          is_bestseller: boolean;
          is_new_arrival: boolean;
          status: ProductStatus;
          gender: Gender;
          display_order: number;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          name: string;
          slug: string;
          brand: string;
          category_id?: string | null;
          short_description?: string | null;
          description?: string | null;
          top_notes?: string[] | null;
          middle_notes?: string[] | null;
          base_notes?: string[] | null;
          price: number;
          discount_price?: number | null;
          sizes?: Json | null;
          stock_quantity?: number;
          rating?: number;
          review_count?: number;
          is_featured?: boolean;
          is_bestseller?: boolean;
          is_new_arrival?: boolean;
          status?: ProductStatus;
          gender?: Gender;
          display_order?: number;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          name?: string;
          slug?: string;
          brand?: string;
          category_id?: string | null;
          short_description?: string | null;
          description?: string | null;
          top_notes?: string[] | null;
          middle_notes?: string[] | null;
          base_notes?: string[] | null;
          price?: number;
          discount_price?: number | null;
          sizes?: Json | null;
          stock_quantity?: number;
          rating?: number;
          review_count?: number;
          is_featured?: boolean;
          is_bestseller?: boolean;
          is_new_arrival?: boolean;
          status?: ProductStatus;
          gender?: Gender;
          display_order?: number;
          updated_at?: string;
        };
      };
      product_images: {
        Row: {
          id: string;
          product_id: string;
          url: string;
          alt_text: string | null;
          is_primary: boolean;
          display_order: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          product_id: string;
          url: string;
          alt_text?: string | null;
          is_primary?: boolean;
          display_order?: number;
          created_at?: string;
        };
        Update: {
          product_id?: string;
          url?: string;
          alt_text?: string | null;
          is_primary?: boolean;
          display_order?: number;
        };
      };
      addresses: {
        Row: {
          id: string;
          user_id: string;
          label: string;
          full_name: string;
          phone: string;
          address_line_1: string;
          address_line_2: string | null;
          city: string;
          postal_code: string;
          is_default: boolean;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          label: string;
          full_name: string;
          phone: string;
          address_line_1: string;
          address_line_2?: string | null;
          city: string;
          postal_code: string;
          is_default?: boolean;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          label?: string;
          full_name?: string;
          phone?: string;
          address_line_1?: string;
          address_line_2?: string | null;
          city?: string;
          postal_code?: string;
          is_default?: boolean;
          updated_at?: string;
        };
      };
      orders: {
        Row: {
          id: string;
          user_id: string | null;
          order_number: string;
          status: OrderStatus;
          subtotal: number;
          shipping_cost: number;
          total: number;
          payment_method: PaymentMethod;
          shipping_address: Json;
          notes: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id?: string | null;
          order_number?: string;
          status?: OrderStatus;
          subtotal: number;
          shipping_cost?: number;
          total: number;
          payment_method: PaymentMethod;
          shipping_address: Json;
          notes?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          status?: OrderStatus;
          shipping_cost?: number;
          notes?: string | null;
          updated_at?: string;
        };
      };
      settings: {
        Row: {
          key: string;
          value: Json;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          key: string;
          value: Json;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          key?: string;
          value?: Json;
          updated_at?: string;
        };
      };
      order_items: {
        Row: {
          id: string;
          order_id: string;
          product_id: string;
          product_name: string;
          product_image: string | null;
          size: string | null;
          quantity: number;
          unit_price: number;
          total_price: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          order_id: string;
          product_id: string;
          product_name: string;
          product_image?: string | null;
          size?: string | null;
          quantity: number;
          unit_price: number;
          total_price: number;
          created_at?: string;
        };
        Update: {
          quantity?: number;
          unit_price?: number;
          total_price?: number;
        };
      };
    };
    Views: {
      [_ in never]: never;
    };
    Functions: {
      [_ in never]: never;
    };
    Enums: {
      order_status: OrderStatus;
      payment_method: PaymentMethod;
      product_status: ProductStatus;
      user_role: UserRole;
      gender: Gender;
    };
    CompositeTypes: {
      [_ in never]: never;
    };
  };
}

// Convenience type aliases
export type Profile = Database['public']['Tables']['profiles']['Row'];
export type Category = Database['public']['Tables']['categories']['Row'];
export type Product = Database['public']['Tables']['products']['Row'];
export type ProductImage = Database['public']['Tables']['product_images']['Row'];
export type Address = Database['public']['Tables']['addresses']['Row'];
export type Order = Database['public']['Tables']['orders']['Row'];
export type OrderItem = Database['public']['Tables']['order_items']['Row'];

// Extended types with relations
export type ProductWithImages = Product & {
  product_images: ProductImage[];
  categories?: Category | null;
};

export type OrderWithItems = Order & {
  order_items: (OrderItem & {
    products?: Product | null;
  })[];
  profiles?: Profile | null;
};

// Cart types
export interface CartItem {
  product_id: string;
  product_name: string;
  product_image: string;
  product_slug: string;
  brand: string;
  size: string | null;
  quantity: number;
  unit_price: number;
  max_stock: number;
}

// Size option type
export interface SizeOption {
  label: string;
  ml: number;
  price: number;
}

// Filter types
export interface ProductFilters {
  search?: string;
  category?: string;
  brand?: string;
  gender?: Gender;
  min_price?: number;
  max_price?: number;
  sort?: 'popular' | 'newest' | 'price_asc' | 'price_desc';
  page?: number;
  per_page?: number;
}
