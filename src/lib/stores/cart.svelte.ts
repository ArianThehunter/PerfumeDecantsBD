import { browser } from '$app/environment';
import type { CartItem } from '$lib/types/database';

const CART_STORAGE_KEY = 'perfume-decants-cart';

// Reactive cart state using Svelte 5 runes
let items = $state<CartItem[]>([]);
let isOpen = $state(false);

let currentKey = CART_STORAGE_KEY + '-guest';

// Load from localStorage on init
if (browser) {
  try {
    const stored = localStorage.getItem(currentKey);
    if (stored) {
      items = JSON.parse(stored);
    }
  } catch {
    items = [];
  }
}

function initForUser(userId: string | null) {
  if (!browser) return;
  const key = userId ? `${CART_STORAGE_KEY}-${userId}` : `${CART_STORAGE_KEY}-guest`;
  currentKey = key;
  try {
    const stored = localStorage.getItem(key);
    if (stored) {
      items = JSON.parse(stored);
    } else {
      items = [];
    }
  } catch {
    items = [];
  }
}

// Persist to localStorage whenever items change
function persist() {
  if (browser && currentKey) {
    localStorage.setItem(currentKey, JSON.stringify(items));
  }
}

// Computed values
function getItemCount(): number {
  return items.reduce((sum, item) => sum + item.quantity, 0);
}

function getSubtotal(): number {
  return items.reduce((sum, item) => sum + item.unit_price * item.quantity, 0);
}

function getShippingCost(): number {
  const subtotal = getSubtotal();
  if (subtotal === 0) return 0;
  if (subtotal >= 5000) return 0; // Free shipping over 5000 BDT
  return 120; // Flat rate shipping
}

function getTotal(): number {
  return getSubtotal() + getShippingCost();
}

// Actions
function addItem(newItem: CartItem) {
  const existingIndex = items.findIndex(
    (item) => item.product_id === newItem.product_id && item.size === newItem.size
  );

  if (existingIndex >= 0) {
    const existing = items[existingIndex];
    const newQty = Math.min(existing.quantity + newItem.quantity, existing.max_stock);
    items[existingIndex] = { ...existing, quantity: newQty };
  } else {
    items = [...items, newItem];
  }
  persist();
}

function removeItem(productId: string, size: string | null) {
  items = items.filter((item) => !(item.product_id === productId && item.size === size));
  persist();
}

function updateQuantity(productId: string, size: string | null, quantity: number) {
  const index = items.findIndex(
    (item) => item.product_id === productId && item.size === size
  );

  if (index >= 0) {
    if (quantity <= 0) {
      removeItem(productId, size);
    } else {
      const maxQty = Math.min(quantity, items[index].max_stock);
      items[index] = { ...items[index], quantity: maxQty };
      persist();
    }
  }
}

function clearCart() {
  items = [];
  persist();
}

function openCart() {
  isOpen = true;
}

function closeCart() {
  isOpen = false;
}

function toggleCart() {
  isOpen = !isOpen;
}

function isInCart(productId: string, size: string | null): boolean {
  return items.some((item) => item.product_id === productId && item.size === size);
}

// Export the cart store as a module
export const cart = {
  get items() { return items; },
  get isOpen() { return isOpen; },
  get itemCount() { return getItemCount(); },
  get subtotal() { return getSubtotal(); },
  get shippingCost() { return getShippingCost(); },
  get total() { return getTotal(); },
  initForUser,
  addItem,
  removeItem,
  updateQuantity,
  clearCart,
  openCart,
  closeCart,
  toggleCart,
  isInCart
};
