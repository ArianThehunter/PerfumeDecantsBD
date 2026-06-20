"""
PerfumeDecantBD — Database Seeding Script
==========================================
Generates realistic seed data for testing identity, products, inventory, orders, analytics, and AI insights.
"""

import asyncio
from datetime import UTC, datetime, timedelta
import random
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import async_session_factory, Base, engine, init_db
from src.core.security import hash_password

# Import models
from src.modules.auth.models import Role, User, Address
from src.modules.products.models import Brand, Category, Collection, Note, FragranceFamily, Product, ProductVariant, ProductImage, ProductNote, PriceHistory
from src.modules.orders.models import Order, OrderItem, OrderTimeline
from src.modules.discounts.models import Coupon, CouponUsage, Campaign
from src.modules.inventory.models import Warehouse, InventoryMovement, Supplier
from src.modules.reviews.models import Review
from src.modules.notifications.models import Notification

async def seed_all():
    print("Initializing database tables...")
    await init_db()
    print("Starting database seeding...")
    async with async_session_factory() as db:
        # 1. Seed Roles
        roles_dict = {}
        for role_name in ["SuperAdmin", "Manager", "InventoryManager", "CustomerSupport", "Customer", "Viewer"]:
            stmt = select(Role).where(Role.name == role_name)
            res = await db.execute(stmt)
            role = res.scalar_one_or_none()
            if not role:
                role = Role(
                    name=role_name,
                    description=f"{role_name} access role",
                    permissions='["*"]' if role_name in ["SuperAdmin", "Manager"] else '[]'
                )
                db.add(role)
            roles_dict[role_name] = role
        
        await db.flush()

        # 2. Seed Users
        hashed_pwd = hash_password("password123")
        users = [
            # Admin User
            User(
                email="admin@perfumedecantbd.com",
                password_hash=hashed_pwd,
                first_name="Rafiq",
                last_name="Islam",
                phone="01711223344",
                is_active=True,
                is_verified=True,
                roles=[roles_dict["SuperAdmin"]]
            ),
            # Staff Users
            User(
                email="manager@perfumedecantbd.com",
                password_hash=hashed_pwd,
                first_name="Sajid",
                last_name="Rahman",
                phone="01711223345",
                is_active=True,
                is_verified=True,
                roles=[roles_dict["Manager"]]
            ),
            User(
                email="inventory@perfumedecantbd.com",
                password_hash=hashed_pwd,
                first_name="Mizan",
                last_name="Haque",
                phone="01711223346",
                is_active=True,
                is_verified=True,
                roles=[roles_dict["InventoryManager"]]
            ),
        ]

        # Add 10 mock customers
        first_names = ["Anik", "Tahsan", "Nisha", "Farhan", "Riyad", "Jamil", "Sultana", "Nabil", "Sadia", "Zayan"]
        last_names = ["Ahmed", "Khan", "Chowdhury", "Hassan", "Islam", "Rahman", "Begum", "Talukder", "Jahan", "Hossain"]
        
        customers = []
        for i in range(10):
            cust = User(
                email=f"customer{i+1}@gmail.com",
                password_hash=hashed_pwd,
                first_name=first_names[i],
                last_name=last_names[i],
                phone=f"0181234567{i}",
                is_active=True,
                is_verified=True,
                roles=[roles_dict["Customer"]],
                reward_points=random.randint(50, 500)
            )
            users.append(cust)
            customers.append(cust)

        # Persist users and resolve database instances
        persisted_users = []
        persisted_customers = []
        for u in users:
            stmt = select(User).where(User.email == u.email)
            res = await db.execute(stmt)
            db_user = res.scalar_one_or_none()
            if not db_user:
                db.add(u)
                db_user = u
            persisted_users.append(db_user)
            if u in customers:
                persisted_customers.append(db_user)
                
        await db.flush()
        customers = persisted_customers

        # Seed Addresses for customers
        for cust in customers:
            stmt_addr = select(Address).where(Address.user_id == cust.id)
            res_addr = await db.execute(stmt_addr)
            if not res_addr.scalar_one_or_none():
                address = Address(
                    user_id=cust.id,
                    label="Home",
                    first_name=cust.first_name,
                    last_name=cust.last_name,
                    address_line1=f"{random.randint(10, 150)} Road No. {random.randint(1, 15)}, Sector {random.randint(1, 14)}",
                    city="Dhaka",
                    postal_code=str(random.randint(1200, 1230)),
                    country="Bangladesh",
                    phone=cust.phone,
                    is_default=True
                )
                db.add(address)
        
        await db.flush()

        # 3. Seed Suppliers and Warehouse
        stmt_sup = select(Supplier).where(Supplier.name == "EuroParfums Distributor")
        res_sup = await db.execute(stmt_sup)
        supplier = res_sup.scalar_one_or_none()
        if not supplier:
            supplier = Supplier(
                name="EuroParfums Distributor",
                contact_name="Marcello V.",
                email="contact@europarfums.com",
                phone="+3312345678",
                address="Rue de Faubourg, Paris, France"
            )
            db.add(supplier)

        stmt_wh = select(Warehouse).where(Warehouse.name == "Dhaka Central Hub")
        res_wh = await db.execute(stmt_wh)
        warehouse = res_wh.scalar_one_or_none()
        if not warehouse:
            warehouse = Warehouse(
                name="Dhaka Central Hub",
                location="Tejgaon Industrial Area, Dhaka",
                is_active=True
            )
            db.add(warehouse)
        await db.flush()

        # 4. Seed Fragrance Families
        fam_dict = {}
        families = [
            ("Woody", "woody", "#6B4A31", "Earthy scents based on wood materials, like cedar, sandalwood, and patchouli."),
            ("Citrus", "citrus", "#E3A814", "Zesty and fresh scents based on fruits like bergamot, lemon, orange, and lime."),
            ("Ambery", "ambery", "#C96D28", "Warm, sweet, and exotic scents formerly known as oriental, incorporating vanilla, spices, and resins."),
            ("Floral", "floral", "#DF7A97", "Classic scents built around floral bouquets, roses, jasmine, and lilies."),
            ("Fresh", "fresh", "#3A96C4", "Clean, oceanic, and green scents inspired by marine breezes, freshly cut grass, and aquatic elements.")
        ]
        for name, slug, color, desc_text in families:
            stmt = select(FragranceFamily).where(FragranceFamily.name == name)
            res = await db.execute(stmt)
            fam = res.scalar_one_or_none()
            if not fam:
                fam = FragranceFamily(name=name, slug=slug, color=color, description=desc_text)
                db.add(fam)
            fam_dict[name] = fam

        await db.flush()

        # 5. Seed Notes
        notes_dict = {}
        notes = [
            ("Bergamot", "Citrus", "Fresh, zesty Italian citrus fruit", "🍋"),
            ("Pineapple", "Fruit", "Sweet, tropical, juicy fruit", "🍍"),
            ("Jasmine", "Floral", "Intense, sweet, rich white floral", "🌸"),
            ("Ambergris", "Animalic", "Salty, warm, marine scent element", "🌊"),
            ("Oakmoss", "Woody", "Forest floor, damp, mossy green note", "🌿"),
            ("Vanilla", "Sweet", "Creamy, cozy, sweet dessert note", "🍦"),
            ("Oud", "Woody", "Rich, dark, balsamic, smoky agarwood", "🪵"),
            ("Sandalwood", "Woody", "Soft, sweet, milky, warm wood note", "🪵"),
            ("Patchouli", "Woody", "Earthy, dark, herbal, slightly sweet leaf", "🍃"),
            ("Saffron", "Spicy", "Rich, leathery, bittersweet spice", "🌶️"),
            ("Cedarwood", "Woody", "Dry, clean, pencil-shavings style wood", "🌲"),
            ("Rose", "Floral", "Classic, romantic, rich pink flower", "🌹"),
            ("Musk", "Animalic", "Clean, powdery, skin-like base note", "🧼")
        ]
        for name, category, desc_text, icon in notes:
            stmt = select(Note).where(Note.name == name)
            res = await db.execute(stmt)
            note = res.scalar_one_or_none()
            if not note:
                note = Note(name=name, category=category, description=desc_text, icon=icon)
                db.add(note)
            notes_dict[name] = note

        await db.flush()

        # 6. Seed Brands
        brands_data = [
            ("Creed", "creed", "House of Creed, luxurious multi-generational fragrance dynasty.", "France"),
            ("Chanel", "chanel", "High-fashion Parisian brand known for classic elegance.", "France"),
            ("Dior", "dior", "House of Dior, creator of modern blockbusters and private lines.", "France"),
            ("Tom Ford", "tom-ford", "Bold, seductive, premium fragrances from American fashion icon.", "United States"),
            ("Maison Francis Kurkdjian", "mfk", "Master perfumer Kurkdjian's legendary niche fragrance house.", "France"),
            ("Roja Parfums", "roja-parfums", "Roja Dove's ultra-luxury British haute parfumerie.", "United Kingdom"),
            ("Byredo", "byredo", "Modern minimalist Stockholm-based scent stories.", "Sweden")
        ]
        brands_dict = {}
        for name, slug, desc_text, country in brands_data:
            stmt = select(Brand).where(Brand.name == name)
            res = await db.execute(stmt)
            brand = res.scalar_one_or_none()
            if not brand:
                brand = Brand(name=name, slug=slug, description=desc_text, country=country)
                db.add(brand)
            brands_dict[name] = brand

        await db.flush()

        # 7. Seed Categories
        cat_dict = {}
        categories_data = [
            ("Mens Fragrances", "mens", "Perfumes tailored for men"),
            ("Womens Fragrances", "womens", "Perfumes tailored for women"),
            ("Niche & Premium", "niche", "Exclusive luxury releases"),
            ("Designer Favorites", "designer", "Timeless crowd pleasers"),
        ]
        for name, slug, desc_text in categories_data:
            stmt = select(Category).where(Category.slug == slug)
            res = await db.execute(stmt)
            cat = res.scalar_one_or_none()
            if not cat:
                cat = Category(name=name, slug=slug, description=desc_text)
                db.add(cat)
            cat_dict[slug] = cat

        await db.flush()

        # 8. Seed Collections
        col_dict = {}
        collections_data = [
            ("Summer Freshies", "summer-freshies", "Zesty, aquatic scents built for warm days.", True),
            ("Date Night Gems", "date-night", "Seductive, mysterious scents to make a statement.", True),
            ("Office Safe", "office-safe", "Clean, polite, professional everyday fragrances.", False),
        ]
        for name, slug, desc_text, is_feat in collections_data:
            stmt = select(Collection).where(Collection.slug == slug)
            res = await db.execute(stmt)
            col = res.scalar_one_or_none()
            if not col:
                col = Collection(name=name, slug=slug, description=desc_text, is_featured=is_feat)
                db.add(col)
            col_dict[slug] = col

        await db.flush()

        # 9. Seed Coupons
        coupons = [
            Coupon(code="WELCOME10", discount_type="percentage", discount_value=10.0, min_order_amount=50.0, is_active=True),
            Coupon(code="FLASH20", discount_type="percentage", discount_value=20.0, max_discount_amount=40.0, is_active=True),
            Coupon(code="LUXE50", discount_type="fixed", discount_value=50.0, min_order_amount=300.0, is_active=True)
        ]
        for cp in coupons:
            stmt = select(Coupon).where(Coupon.code == cp.code)
            res = await db.execute(stmt)
            if not res.scalar_one_or_none():
                db.add(cp)

        await db.flush()

        # 10. Seed Products & Variants
        products_data = [
            {
                "name": "Aventus",
                "slug": "creed-aventus",
                "brand": "Creed",
                "family": "Woody",
                "gender": "Men",
                "concentration": "Aventus Cologne",
                "desc": "The exceptional Aventus was inspired by the dramatic life of a historic emperor, celebrating strength, power and success.",
                "short": "Legendary fruity, woody fragrance for men.",
                "price": 320.0,
                "cost": 150.0,
                "variants": [
                    ("2ml Decant", "AV-DEC-2", 2, 8.0, 4.0, 100),
                    ("5ml Decant", "AV-DEC-5", 5, 18.0, 9.0, 80),
                    ("10ml Decant", "AV-DEC-10", 10, 32.0, 16.0, 6), # Low stock item!
                    ("100ml Bottle", "AV-BOT-100", 100, 320.0, 150.0, 12),
                ],
                "notes": [("Bergamot", "top"), ("Pineapple", "top"), ("Jasmine", "middle"), ("Ambergris", "base"), ("Oakmoss", "base")],
                "categories": ["mens", "niche"],
                "collections": ["summer-freshies", "office-safe"],
                "is_featured": True,
                "is_best_seller": True,
            },
            {
                "name": "Bleu de Chanel",
                "slug": "bleu-de-chanel",
                "brand": "Chanel",
                "family": "Citrus",
                "gender": "Men",
                "concentration": "EDP",
                "desc": "An ode to masculine freedom expressed in a woody aromatic fragrance with a captivating trail. A timeless scent.",
                "short": "Classic fresh, clean masculine office masterpiece.",
                "price": 145.0,
                "cost": 65.0,
                "variants": [
                    ("2ml Decant", "BDC-DEC-2", 2, 5.0, 2.5, 120),
                    ("5ml Decant", "BDC-DEC-5", 5, 12.0, 6.0, 90),
                    ("10ml Decant", "BDC-DEC-10", 10, 22.0, 11.0, 4), # Low stock item!
                    ("100ml Bottle", "BDC-BOT-100", 100, 145.0, 65.0, 15),
                ],
                "notes": [("Bergamot", "top"), ("Jasmine", "middle"), ("Sandalwood", "base"), ("Cedarwood", "base"), ("Musk", "base")],
                "categories": ["mens", "designer"],
                "collections": ["office-safe", "date-night"],
                "is_featured": True,
                "is_best_seller": True,
            },
            {
                "name": "Baccarat Rouge 540",
                "slug": "br540",
                "brand": "Maison Francis Kurkdjian",
                "family": "Ambery",
                "gender": "Unisex",
                "concentration": "Extrait de Parfum",
                "desc": "Luminous and sophisticated, Baccarat Rouge 540 lays on the skin like an amber, floral and woody breeze. A highly poetic alchemy.",
                "short": "Luxurious sweet burnt-sugar ambergris perfume.",
                "price": 380.0,
                "cost": 180.0,
                "variants": [
                    ("2ml Decant", "BR540-DEC-2", 2, 10.0, 5.0, 80),
                    ("5ml Decant", "BR540-DEC-5", 5, 24.0, 12.0, 60),
                    ("10ml Decant", "BR540-DEC-10", 10, 45.0, 22.0, 30),
                    ("70ml Bottle", "BR540-BOT-70", 70, 380.0, 180.0, 8),
                ],
                "notes": [("Saffron", "top"), ("Jasmine", "middle"), ("Ambergris", "base"), ("Cedarwood", "base")],
                "categories": ["womens", "niche"],
                "collections": ["date-night"],
                "is_featured": True,
                "is_best_seller": False,
            },
            {
                "name": "Lost Cherry",
                "slug": "tf-lost-cherry",
                "brand": "Tom Ford",
                "family": "Ambery",
                "gender": "Unisex",
                "concentration": "Eau de Parfum",
                "desc": "Lost Cherry is a full-bodied journey into the once-forbidden; a contrasting scent that reveals a tempting dichotomy of playful, candy-like gleam on the outside and luscious flesh on the inside.",
                "short": "Warm sweet almond, black cherry, and liqueur.",
                "price": 395.0,
                "cost": 190.0,
                "variants": [
                    ("2ml Decant", "TFLC-DEC-2", 2, 12.0, 6.0, 0), # Out of stock item!
                    ("5ml Decant", "TFLC-DEC-5", 5, 28.0, 14.0, 50),
                    ("10ml Decant", "TFLC-DEC-10", 10, 50.0, 25.0, 20),
                    ("50ml Bottle", "TFLC-BOT-50", 50, 395.0, 190.0, 5),
                ],
                "notes": [("Vanilla", "base"), ("Rose", "middle"), ("Sandalwood", "base")],
                "categories": ["womens", "niche"],
                "collections": ["date-night"],
                "is_featured": False,
                "is_best_seller": False,
            },
            {
                "name": "Oud Wood",
                "slug": "tf-oud-wood",
                "brand": "Tom Ford",
                "family": "Woody",
                "gender": "Men",
                "concentration": "Eau de Parfum",
                "desc": "One of the most rare, precious, and expensive ingredients in a perfumer's arsenal, oud wood is often burned in incense-filled temples.",
                "short": "Smoky, dry blend of exotic agarwood, cardamom, and rosewood.",
                "price": 295.0,
                "cost": 130.0,
                "variants": [
                    ("2ml Decant", "TFOW-DEC-2", 2, 8.0, 4.0, 90),
                    ("5ml Decant", "TFOW-DEC-5", 5, 18.0, 9.0, 60),
                    ("10ml Decant", "TFOW-DEC-10", 10, 32.0, 16.0, 40),
                    ("100ml Bottle", "TFOW-BOT-100", 100, 295.0, 130.0, 10),
                ],
                "notes": [("Oud", "middle"), ("Sandalwood", "base"), ("Vanilla", "base"), ("Cedarwood", "middle")],
                "categories": ["mens", "niche"],
                "collections": ["office-safe", "date-night"],
                "is_featured": False,
                "is_best_seller": True,
            }
        ]

        products_dict = {}
        variants_list = []
        for prod_info in products_data:
            stmt = select(Product).where(Product.slug == prod_info["slug"])
            res = await db.execute(stmt)
            product = res.scalar_one_or_none()
            
            if not product:
                product = Product(
                    name=prod_info["name"],
                    slug=prod_info["slug"],
                    brand_id=brands_dict[prod_info["brand"]].id,
                    fragrance_family_id=fam_dict[prod_info["family"]].id,
                    gender=prod_info["gender"],
                    concentration=prod_info["concentration"],
                    description=prod_info["desc"],
                    short_description=prod_info["short"],
                    base_price=prod_info["price"],
                    cost_price=prod_info["cost"],
                    status="published",
                    is_featured=prod_info["is_featured"],
                    is_best_seller=prod_info["is_best_seller"],
                    avg_rating=4.5 + random.random() * 0.5,
                    review_count=random.randint(5, 20)
                )
                
                # Link categories
                for cat_slug in prod_info["categories"]:
                    product.categories.append(cat_dict[cat_slug])
                
                # Link collections
                for col_slug in prod_info["collections"]:
                    product.collections.append(col_dict[col_slug])
                
                db.add(product)
                await db.flush()

                # Add image placeholders
                image = ProductImage(
                    product_id=product.id,
                    url=f"/static/images/perfumes/{product.slug}.jpg",
                    alt_text=product.name,
                    is_primary=True
                )
                db.add(image)

                # Add notes relationships
                for note_name, pos in prod_info["notes"]:
                    note_rel = ProductNote(
                        product_id=product.id,
                        note_id=notes_dict[note_name].id,
                        position=pos
                    )
                    db.add(note_rel)

                # Add variants
                for vname, sku, size, price, cost, stock in prod_info["variants"]:
                    var = ProductVariant(
                        product_id=product.id,
                        name=vname,
                        sku=sku,
                        size_ml=size,
                        price=price,
                        cost_price=cost,
                        stock_quantity=stock,
                        safety_stock=5 if size < 100 else 2,
                        is_active=True
                    )
                    db.add(var)
                    variants_list.append(var)
                    
                    # Record initial purchase inventory movements
                    if stock > 0:
                        mov = InventoryMovement(
                            variant=var,
                            warehouse=warehouse,
                            movement_type="purchase",
                            quantity=stock,
                            notes="Initial seed stock purchase",
                            unit_cost=cost,
                            created_by="System Seed"
                        )
                        db.add(mov)
            else:
                stmt_vars = select(ProductVariant).where(ProductVariant.product_id == product.id)
                res_vars = await db.execute(stmt_vars)
                variants_list.extend(res_vars.scalars().all())
                
            products_dict[prod_info["name"]] = product

        await db.flush()

        # 11. Seed Orders History (Last 60 Days)
        # We need a rich dataset of transactions to populate analytics charts.
        # We'll generate ~50 orders spread over the last 60 days.
        stmt_orders = select(func.count(Order.id))
        orders_exist_count = (await db.execute(stmt_orders)).scalar() or 0
        
        if orders_exist_count == 0:
            print("Seeding order history...")
            now = datetime.now(UTC)
            for i in range(50):
                # Pick a random customer
                cust = random.choice(customers)
                
                # Order date spread over last 60 days
                order_days_ago = random.randint(1, 60)
                order_date = now - timedelta(days=order_days_ago, hours=random.randint(1, 23))
                
                # Generate order items
                num_items = random.randint(1, 3)
                order_items = []
                subtotal = 0.0
                
                selected_variants = random.sample(variants_list, num_items)
                for var in selected_variants:
                    qty = random.randint(1, 2)
                    price = float(var.price)
                    total_p = price * qty
                    subtotal += total_p
                    
                    order_items.append(OrderItem(
                        variant_id=var.id,
                        product_name=var.product.name,
                        variant_name=var.name,
                        sku=var.sku,
                        quantity=qty,
                        unit_price=price,
                        total_price=total_p,
                        product_image=f"/static/images/perfumes/{var.product.slug}.jpg"
                    ))
                    
                    # Record sales movement
                    mov = InventoryMovement(
                        variant_id=var.id,
                        warehouse_id=warehouse.id,
                        movement_type="sale",
                        quantity=-qty,
                        reference=f"ORD-{(1000 + i)}",
                        notes=f"Order sale ORD-{(1000 + i)}",
                        created_by="System Seed"
                    )
                    db.add(mov)
                    
                    # Deduct stock
                    var.stock_quantity = max(0, var.stock_quantity - qty)

                shipping = 10.0
                tax = round(subtotal * 0.05, 2)
                discount = 0.0
                
                # Randomly apply coupon
                coupon_code = None
                if random.random() < 0.3:
                    coupon_code = "WELCOME10"
                    discount = round(subtotal * 0.10, 2)
                
                total = subtotal + shipping + tax - discount

                order = Order(
                    order_number=f"ORD-{(1000 + i)}",
                    user_id=cust.id,
                    status=random.choice(["delivered", "delivered", "delivered", "shipped", "processing"]),
                    subtotal=subtotal,
                    shipping_cost=shipping,
                    tax_amount=tax,
                    discount_amount=discount,
                    total=total,
                    coupon_code=coupon_code,
                    payment_method=random.choice(["bkash", "cash_on_delivery", "card"]),
                    payment_status="paid" if random.random() < 0.9 else "pending",
                    created_at=order_date,
                    updated_at=order_date
                )
                
                # Add items
                order.items.extend(order_items)
                db.add(order)
                
                # Add timeline events
                timeline1 = OrderTimeline(
                    order=order,
                    status="pending",
                    title="Order Placed",
                    description="Your order has been received.",
                    created_at=order_date
                )
                timeline2 = OrderTimeline(
                    order=order,
                    status="confirmed",
                    title="Order Confirmed",
                    description="Merchant confirmed your order.",
                    created_at=order_date + timedelta(minutes=random.randint(10, 60))
                )
                db.add(timeline1)
                db.add(timeline2)
                
                # Update customer statistics
                cust.total_orders += 1
                cust.lifetime_value = float(cust.lifetime_value) + total
                
            await db.flush()

        # 12. Seed Reviews
        stmt_rev = select(func.count(Review.id))
        rev_count = (await db.execute(stmt_rev)).scalar() or 0
        if rev_count == 0:
            for name, prod in products_dict.items():
                # Write 2 reviews per product
                for j in range(2):
                    cust = random.choice(customers)
                    rev = Review(
                        product_id=prod.id,
                        user_id=cust.id,
                        rating=random.randint(4, 5),
                        title=random.choice(["Amazing smell!", "Long lasting", "Authentic decants", "Great service"]),
                        content=random.choice([
                            "This smells absolutely stunning and is highly projection-heavy. Will buy again!",
                            "The projection is solid. Lasts for 8+ hours on my clothes. Recommended brand.",
                            "Authentic juice. Shipping took 2 days. The packaging was top-notch.",
                        ]),
                        is_verified_purchase=True,
                        is_approved=True
                    )
                    db.add(rev)
            await db.flush()

        await db.commit()
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_all())
