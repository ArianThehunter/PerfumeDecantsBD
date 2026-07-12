-- Seed Categories
insert into public.categories (id, name, slug, description, image_url, display_order) values
('c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91', 'Eau de Parfum', 'eau-de-parfum', 'High concentration of perfume oils, lasting 6-8 hours.', 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=600&h=800&fit=crop', 1),
('c8e03e5c-7d9a-4f5d-be1f-2df25fba0b92', 'Eau de Toilette', 'eau-de-toilette', 'Lighter concentration ideal for daily use, lasting 4-6 hours.', 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=600&h=800&fit=crop', 2),
('c8e03e5c-7d9a-4f5d-be1f-3df25fba0b93', 'Cologne', 'cologne', 'Fresh and light fragrances, perfect for hot weather.', 'https://images.unsplash.com/photo-1594035910387-fea081ac45b0?w=600&h=800&fit=crop', 3),
('c8e03e5c-7d9a-4f5d-be1f-4df25fba0b94', 'Unisex', 'unisex', 'Fragrances designed to be shared and enjoyed by everyone.', 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=600&h=800&fit=crop', 4),
('c8e03e5c-7d9a-4f5d-be1f-5df25fba0b95', 'Gift Sets', 'gift-sets', 'Curated discovery sets and collections of decants.', 'https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=600&h=800&fit=crop', 5);

-- Seed Products
insert into public.products (id, name, slug, brand, category_id, short_description, description, top_notes, middle_notes, base_notes, price, discount_price, sizes, stock_quantity, rating, review_count, is_featured, is_bestseller, is_new_arrival, status, gender, display_order) values
-- 1. Creed Aventus
('a0000000-0000-0000-0000-000000000001', 'Creed Aventus', 'creed-aventus', 'Creed', 'c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91',
 'The exceptional Aventus was inspired by the dramatic life of a historic emperor.',
 'The exceptional Aventus was inspired by the dramatic life of a historic emperor, celebrating strength, power and success. Introduced in 2010, this scent has grown to become the most popular fragrance in the history of the brand.',
 array['Pineapple', 'Bergamot', 'Blackcurrant', 'Apple'],
 array['Birch', 'Patchouli', 'Moroccan Jasmine', 'Rose'],
 array['Musk', 'Oakmoss', 'Ambergris', 'Vanille'],
 2500, 2300,
 '[{"label": "5ml", "price": 1200, "ml": 5}, {"label": "10ml", "price": 2300, "ml": 10}, {"label": "30ml", "price": 6500, "ml": 30}]'::jsonb,
 15, 4.9, 128, true, true, false, 'active', 'men', 1),

-- 2. Bleu de Chanel
('a0000000-0000-0000-0000-000000000002', 'Bleu de Chanel EDP', 'bleu-de-chanel-edp', 'Chanel', 'c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91',
 'An ode to masculine freedom expressed in a woody aromatic fragrance with a captivating trail.',
 'An ode to masculine freedom expressed in a woody aromatic fragrance with a captivating trail. A timeless scent housed in a bottle of deep and mysterious blue.',
 array['Grapefruit', 'Lemon', 'Mint', 'Pink Pepper'],
 array['Ginger', 'Nutmeg', 'Jasmine', 'Iso E Super'],
 array['Incense', 'Vetiver', 'Cedar', 'Sandalwood', 'Patchouli', 'Labdanum', 'Amber'],
 1900, null,
 '[{"label": "5ml", "price": 1000, "ml": 5}, {"label": "10ml", "price": 1900, "ml": 10}, {"label": "30ml", "price": 5400, "ml": 30}]'::jsonb,
 22, 4.8, 310, true, true, false, 'active', 'men', 2),

-- 3. Dior Sauvage
('a0000000-0000-0000-0000-000000000003', 'Sauvage EDP', 'sauvage-edp', 'Dior', 'c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91',
 'A powerful freshness of Sauvage exudes new sensual and mysterious facets.',
 'A powerful freshness of Sauvage exudes new sensual and mysterious facets, renewing itself with the signature of an ingenious composition. Calabrian Bergamot, spirited and juicy, invites new spicy notes to add fullness and sensuality.',
 array['Calabrian Bergamot'],
 array['Sichuan Pepper', 'Lavender', 'Star Anise', 'Nutmeg'],
 array['Ambroxan', 'Vanilla'],
 1800, 1600,
 '[{"label": "5ml", "price": 850, "ml": 5}, {"label": "10ml", "price": 1600, "ml": 10}, {"label": "30ml", "price": 4500, "ml": 30}]'::jsonb,
 12, 4.7, 420, true, false, true, 'active', 'men', 3),

-- 4. Baccarat Rouge 540
('a0000000-0000-0000-0000-000000000004', 'Baccarat Rouge 540 EDP', 'baccarat-rouge-540', 'Maison Francis Kurkdjian', 'c8e03e5c-7d9a-4f5d-be1f-4df25fba0b94',
 'Luminous and sophisticated, Baccarat Rouge 540 lays on the skin like an amber, floral and woody breeze.',
 'Luminous and sophisticated, Baccarat Rouge 540 lays on the skin like an amber, floral and woody breeze. A poetic alchemy. A highly condensed and graphic olfactory signature.',
 array['Saffron', 'Jasmine'],
 array['Amberwood', 'Ambergris'],
 array['Fir Resin', 'Cedar'],
 3200, 2900,
 '[{"label": "5ml", "price": 1600, "ml": 5}, {"label": "10ml", "price": 2900, "ml": 10}, {"label": "30ml", "price": 8500, "ml": 30}]'::jsonb,
 8, 4.9, 95, true, true, false, 'active', 'unisex', 4),

-- 5. Tom Ford Tobacco Vanille
('a0000000-0000-0000-0000-000000000005', 'Tobacco Vanille EDP', 'tobacco-vanille', 'Tom Ford', 'c8e03e5c-7d9a-4f5d-be1f-4df25fba0b94',
 'Tom Ford reinvents a classic fragrance genre by adding creamy tonka bean, vanilla, cocoa, dry fruit accords.',
 'Tom Ford reinvents a classic fragrance genre by adding creamy tonka bean, vanilla, cocoa, dry fruit accords and sweet wood sap for a modern, opulent, and almost heady impression.',
 array['Tobacco Leaf', 'Spicy Notes'],
 array['Vanilla', 'Cocoa', 'Tonka Bean', 'Tobacco Blossom'],
 array['Dried Fruits', 'Woody Notes'],
 2800, null,
 '[{"label": "5ml", "price": 1500, "ml": 5}, {"label": "10ml", "price": 2800, "ml": 10}, {"label": "30ml", "price": 7900, "ml": 30}]'::jsonb,
 10, 4.8, 150, false, true, false, 'active', 'unisex', 5),

-- 6. Yves Saint Laurent Y EDP
('a0000000-0000-0000-0000-000000000006', 'Y EDP', 'y-edp', 'YSL', 'c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91',
 'The perfume of an accomplished and creative man.',
 'Y Eau de Parfum represents a man who has accomplished his dreams and is moving towards a new tomorrow. He is a man capable of facing the challenges presented to him, he takes nothing for granted.',
 array['Apple', 'Ginger', 'Bergamot'],
 array['Sage', 'Juniper Berries', 'Geranium'],
 array['Amberwood', 'Tonka Bean', 'Cedar', 'Vetiver', 'Olibanum'],
 1750, 1550,
 '[{"label": "5ml", "price": 800, "ml": 5}, {"label": "10ml", "price": 1550, "ml": 10}, {"label": "30ml", "price": 4350, "ml": 30}]'::jsonb,
 25, 4.8, 184, false, true, true, 'active', 'men', 6),

-- 7. Tom Ford Lost Cherry
('a0000000-0000-0000-0000-000000000007', 'Lost Cherry EDP', 'lost-cherry', 'Tom Ford', 'c8e03e5c-7d9a-4f5d-be1f-4df25fba0b94',
 'Lost Cherry is a full-bodied journey into the once-forbidden.',
 'Lost Cherry is a full-bodied journey into the once-forbidden; a contrasting scent that reveals a tempting dichotomy of playful, candy-like gleam on the outside and luscious flesh on the inside.',
 array['Bitter Almond', 'Black Cherry', 'Cherry Liqueur'],
 array['Sour Cherry', 'Plum', 'Turkish Rose', 'Jasmine Sambac'],
 array['Tonka Bean', 'Vanilla', 'Cinnamon', 'Peru Balsam', 'Benzoin', 'Sandalwood', 'Cloves', 'Cedar', 'Patchouli', 'Vetiver'],
 3100, 2800,
 '[{"label": "5ml", "price": 1500, "ml": 5}, {"label": "10ml", "price": 2800, "ml": 10}, {"label": "30ml", "price": 8100, "ml": 30}]'::jsonb,
 7, 4.6, 62, false, false, true, 'active', 'unisex', 7),

-- 8. Parfums de Marly Layton
('a0000000-0000-0000-0000-000000000008', 'Layton EDP', 'layton-pdm', 'Parfums de Marly', 'c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91',
 'An addictive and signature fragrance that combines mandarin, apple and lavender.',
 'An addictive and signature fragrance that combines mandarin, apple and lavender. The warm base contains vanilla, precious woods and coffee notes.',
 array['Apple', 'Lavender', 'Mandarin Orange', 'Bergamot'],
 array['Geranium', 'Violet', 'Jasmine'],
 array['Vanilla', 'Cardamom', 'Sandalwood', 'Pepper', 'Guaiac Wood', 'Patchouli'],
 2600, null,
 '[{"label": "5ml", "price": 1350, "ml": 5}, {"label": "10ml", "price": 2600, "ml": 10}, {"label": "30ml", "price": 7200, "ml": 30}]'::jsonb,
 14, 4.9, 78, true, true, false, 'active', 'men', 8),

-- 9. Giorgio Armani Acqua Di Gio Profondo
('a0000000-0000-0000-0000-000000000009', 'Acqua Di Gio Profondo EDP', 'acqua-di-gio-profondo', 'Armani', 'c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91',
 'Acqua Di Giò Profondo is a deep dive into the profoundness of the soul.',
 'Acqua Di Giò Profondo is the intense marine interpretation of Acqua Di Giò. More than a simple fragrance, Profondo is a captivating deep-dive into the profoundness of the soul, embracing the values of freedom, sensoriality and modern masculinity.',
 array['Marine Notes', 'Aquozone', 'Green Mandarin', 'Bergamot'],
 array['Rosemary', 'Lavender', 'Cypress', 'Mastic or Lentisque'],
 array['Mineral notes', 'Musk', 'Patchouli', 'Amber'],
 1700, 1500,
 '[{"label": "5ml", "price": 800, "ml": 5}, {"label": "10ml", "price": 1500, "ml": 10}, {"label": "30ml", "price": 4200, "ml": 30}]'::jsonb,
 20, 4.7, 140, false, false, false, 'active', 'men', 9),

-- 10. Chanel Coco Mademoiselle
('a0000000-0000-0000-0000-000000000010', 'Coco Mademoiselle EDP', 'coco-mademoiselle', 'Chanel', 'c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91',
 'The essence of a bold, free woman. A feminine character oriental with a strong personality.',
 'The essence of a bold, free woman. A feminine character oriental with a strong personality, yet surprisingly fresh. Sparkling orange notes trigger the senses, leading to a clear, sensual heart.',
 array['Orange', 'Mandarin Orange', 'Bergamot', 'Orange Blossom'],
 array['Turkish Rose', 'Jasmine', 'Mimosa', 'Ylang-Ylang'],
 array['Patchouli', 'White Musk', 'Vanilla', 'Vetiver', 'Tonka Bean', 'Opoponax'],
 2100, 1950,
 '[{"label": "5ml", "price": 1050, "ml": 5}, {"label": "10ml", "price": 1950, "ml": 10}, {"label": "30ml", "price": 5600, "ml": 30}]'::jsonb,
 18, 4.8, 203, true, true, false, 'active', 'women', 10),

-- 11. YSL Libre Intense
('a0000000-0000-0000-0000-000000000011', 'Libre Intense EDP', 'libre-intense', 'YSL', 'c8e03e5c-7d9a-4f5d-be1f-1df25fba0b91',
 'The perfume of a strong, bold and free woman experiencing her freedom at its most extreme.',
 'The perfume of a strong, bold and free woman experiencing her freedom at its most extreme. The tension between the burning sensuality of an orange blossom from Morocco and the aromatic freshness of lavender from France.',
 array['Lavender', 'Mandarin Orange', 'Bergamot'],
 array['Lavender', 'Tunisian Orange Blossom', 'Jasmine Sambac', 'Orchid'],
 array['Madagascar Vanilla', 'Tonka Bean', 'Ambergris', 'Vetiver'],
 2000, 1850,
 '[{"label": "5ml", "price": 950, "ml": 5}, {"label": "10ml", "price": 1850, "ml": 10}, {"label": "30ml", "price": 5200, "ml": 30}]'::jsonb,
 16, 4.7, 98, false, true, true, 'active', 'women', 11),

-- 12. Versace Eros EDT
('a0000000-0000-0000-0000-000000000012', 'Eros EDT', 'versace-eros-edt', 'Versace', 'c8e03e5c-7d9a-4f5d-be1f-2df25fba0b92',
 'Eros is the fragrance that interprets sublime masculinity through a luminous aura.',
 'Eros is the fragrance that interprets sublime masculinity through a luminous aura with an intense, vibrant, and glowing freshness obtained from the combination of mint leaves, Italian lemon zest, and green apple.',
 array['Mint', 'Green Apple', 'Lemon'],
 array['Tonka Bean', 'Ambroxan', 'Geranium'],
 array['Madagascar Vanilla', 'Virginian Cedar', 'Atlas Cedar', 'Vetiver', 'Oakmoss'],
 1400, null,
 '[{"label": "5ml", "price": 750, "ml": 5}, {"label": "10ml", "price": 1400, "ml": 10}, {"label": "30ml", "price": 3800, "ml": 30}]'::jsonb,
 30, 4.6, 255, false, false, false, 'active', 'men', 12);

-- Seed Product Images
insert into public.product_images (product_id, url, alt_text, is_primary, display_order) values
('a0000000-0000-0000-0000-000000000001', 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800&fit=crop', 'Creed Aventus Decant Bottle', true, 1),
('a0000000-0000-0000-0000-000000000002', 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=800&fit=crop', 'Bleu de Chanel Decant', true, 1),
('a0000000-0000-0000-0000-000000000003', 'https://images.unsplash.com/photo-1594035910387-fea081ac45b0?w=800&fit=crop', 'Sauvage EDP Decant', true, 1),
('a0000000-0000-0000-0000-000000000004', 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=800&fit=crop', 'Baccarat Rouge 540 Decant', true, 1),
('a0000000-0000-0000-0000-000000000005', 'https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=800&fit=crop', 'Tobacco Vanille Decant', true, 1),
('a0000000-0000-0000-0000-000000000006', 'https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?w=800&fit=crop', 'YSL Y EDP Decant', true, 1),
('a0000000-0000-0000-0000-000000000007', 'https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?w=800&fit=crop', 'Tom Ford Lost Cherry Decant', true, 1),
('a0000000-0000-0000-0000-000000000008', 'https://images.unsplash.com/photo-1547887538-047f814bfb64?w=800&fit=crop', 'Parfums de Marly Layton Decant', true, 1),
('a0000000-0000-0000-0000-000000000009', 'https://images.unsplash.com/photo-1594035910387-fea081ac45b0?w=800&fit=crop', 'Acqua Di Gio Profondo Decant', true, 1),
('a0000000-0000-0000-0000-000000000010', 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800&fit=crop', 'Coco Mademoiselle Decant', true, 1),
('a0000000-0000-0000-0000-000000000011', 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=800&fit=crop', 'YSL Libre Intense Decant', true, 1),
('a0000000-0000-0000-0000-000000000012', 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=800&fit=crop', 'Versace Eros Decant', true, 1);
