# PerfumeDecantsBD

A luxurious e-commerce platform built for purchasing high-end perfume decants. Features a beautiful user interface with dark/light mode, guest checkout, and a complete admin dashboard for store management.

## Tech Stack
- **Frontend**: SvelteKit, Tailwind CSS
- **Backend & Database**: Supabase (PostgreSQL, Storage, Authentication)
- **Deployment**: Vercel

## Key Features
- **Guest Checkout**: Place orders without requiring an account.
- **Dynamic Carts**: Carts are saved locally and isolated per user.
- **Admin Dashboard**: Manage products, categories, orders, and site settings.
- **Storage**: Direct local image uploads to Supabase storage.
- **Dark/Light Mode**: Full synchronized UI theming.

## Local Development
1. Clone the repository
2. Run `npm install` to install dependencies
3. Copy `.env.example` to `.env` and fill in your Supabase details
4. Run `npm run dev` to start the local development server

## Database Setup
Run the SQL migration scripts located in `supabase/migrations/` in order on your Supabase SQL editor to set up the tables, policies, and storage buckets.

## Deployment
This project is configured with `@sveltejs/adapter-vercel`. Simply import the repository into Vercel and provide the `.env` variables for a seamless deployment.
