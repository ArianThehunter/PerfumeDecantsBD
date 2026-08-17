// Production-ready sliding window rate limiter
// Protects endpoints from DDoS, brute-force credential stuffing, and spam attacks

interface RateLimitRecord {
  count: number;
  resetAt: number;
}

class InMemoryRateLimiter {
  private store = new Map<string, RateLimitRecord>();
  private cleanupInterval: ReturnType<typeof setInterval> | null = null;

  constructor() {
    // Periodically clean up expired entries every 5 minutes
    if (typeof setInterval !== 'undefined') {
      this.cleanupInterval = setInterval(() => {
        const now = Date.now();
        for (const [key, record] of this.store.entries()) {
          if (now > record.resetAt) {
            this.store.delete(key);
          }
        }
      }, 5 * 60 * 1000);

      // Unref timer so it doesn't prevent Node process exit
      const timer = this.cleanupInterval as any;
      if (timer && typeof timer.unref === 'function') {
        timer.unref();
      }
    }
  }

  /**
   * Checks if a request is within the rate limit.
   * @param key Unique identifier (e.g. `ip:checkout` or `email:login`)
   * @param limit Maximum allowed requests within the window
   * @param windowMs Time window in milliseconds
   * @returns `{ allowed: boolean, remaining: number, resetInSeconds: number }`
   */
  check(key: string, limit: number, windowMs: number): { allowed: boolean; remaining: number; resetInSeconds: number } {
    const now = Date.now();
    const record = this.store.get(key);

    if (!record || now > record.resetAt) {
      this.store.set(key, { count: 1, resetAt: now + windowMs });
      return { allowed: true, remaining: limit - 1, resetInSeconds: Math.ceil(windowMs / 1000) };
    }

    if (record.count >= limit) {
      const resetInSeconds = Math.max(1, Math.ceil((record.resetAt - now) / 1000));
      return { allowed: false, remaining: 0, resetInSeconds };
    }

    record.count += 1;
    const remaining = limit - record.count;
    const resetInSeconds = Math.max(1, Math.ceil((record.resetAt - now) / 1000));
    return { allowed: true, remaining, resetInSeconds };
  }

  /**
   * Resets rate limit for a specific key (e.g. on successful login)
   */
  reset(key: string): void {
    this.store.delete(key);
  }
}

export const rateLimiter = new InMemoryRateLimiter();
