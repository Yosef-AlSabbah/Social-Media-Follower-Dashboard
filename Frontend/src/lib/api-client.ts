import { initializeApiConfig } from './environment';

// Initialize API client on app startup
export function initializeApp() {
  // Initialize API configuration
  initializeApiConfig();

  // Set up global error handling for API calls
  if (typeof window !== 'undefined') {
    window.addEventListener('unhandledrejection', (event) => {
      if (event.reason?.name === 'ApiError') {
        console.error('Unhandled API Error:', event.reason);
        // You can add toast notifications or other error handling here
      }
    });
  }
}

// Export API utilities for use throughout the app
export { ApiService, ApiError } from './api-service';
export { ApiConfig, ApiEndpoints } from './api-config';
export type {
  PlatformData,
  AnalyticsSummary,
  GrowthTrendData,
  ChartDataPoint,
  ApiResponse
} from './api-config';
