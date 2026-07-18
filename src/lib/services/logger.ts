// Production-ready structured logging service
// Ready for forwarding to external audit log aggregates (Vercel Logs, Datadog, etc.)

export type LogLevel = 'INFO' | 'WARN' | 'ERROR';

export interface AuditLog {
  timestamp: string;
  level: LogLevel;
  event: string;
  userId?: string | null;
  email?: string | null;
  ip?: string;
  details?: Record<string, any>;
}

export const logger = {
  log(level: LogLevel, event: string, details?: any, userId?: string | null, email?: string | null) {
    const logEntry: AuditLog = {
      timestamp: new Date().toISOString(),
      level,
      event,
      userId,
      email,
      details: details instanceof Error ? { message: details.message, stack: details.stack } : details
    };

    const formattedLog = JSON.stringify(logEntry);

    if (level === 'ERROR') {
      console.error(formattedLog);
    } else if (level === 'WARN') {
      console.warn(formattedLog);
    } else {
      console.log(formattedLog);
    }
  },

  info(event: string, details?: any, userId?: string | null, email?: string | null) {
    this.log('INFO', event, details, userId, email);
  },

  warn(event: string, details?: any, userId?: string | null, email?: string | null) {
    this.log('WARN', event, details, userId, email);
  },

  error(event: string, err?: any, details?: any, userId?: string | null, email?: string | null) {
    this.log('ERROR', event, {
      error: err instanceof Error ? { name: err.name, message: err.message, stack: err.stack } : err,
      ...details
    }, userId, email);
  }
};
