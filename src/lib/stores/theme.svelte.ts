import { browser } from '$app/environment';

const THEME_STORAGE_KEY = 'perfume-decants-theme';

type Theme = 'light' | 'dark';

let current = $state<Theme>('light');

if (browser) {
  const stored = localStorage.getItem(THEME_STORAGE_KEY) as Theme | null;
  let initialTheme: Theme = 'light';
  if (stored) {
    initialTheme = stored;
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    initialTheme = 'dark';
  }
  current = initialTheme;
  applyTheme(initialTheme);
}

function applyTheme(theme: Theme) {
  if (browser) {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }
}

function toggle() {
  current = current === 'light' ? 'dark' : 'light';
  applyTheme(current);
}

function set(theme: Theme) {
  current = theme;
  applyTheme(current);
}

export const theme = {
  get current() { return current; },
  get isDark() { return current === 'dark'; },
  toggle,
  set
};
