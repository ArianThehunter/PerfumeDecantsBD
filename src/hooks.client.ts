import type { HandleClientError } from '@sveltejs/kit';

export const handleError: HandleClientError = async ({ error, event, status, message }) => {
  const errorId = crypto.randomUUID();

  // Log client error to console in a structured format
  console.error(JSON.stringify({
    timestamp: new Date().toISOString(),
    level: 'ERROR',
    event: 'Client uncaught exception',
    errorId,
    status,
    url: event.url.toString(),
    error: error instanceof Error ? { name: error.name, message: error.message, stack: error.stack } : error
  }));

  return {
    message: status === 404 ? 'Page not found' : 'An unexpected error occurred',
    errorId
  };
};
