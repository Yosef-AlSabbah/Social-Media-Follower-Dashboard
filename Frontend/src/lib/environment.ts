// Environment-specific API configuration
export const API_ENVIRONMENTS = {
  development: {
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
    timeout: parseInt(import.meta.env.VITE_API_TIMEOUT) || 30000,
    retryAttempts: parseInt(import.meta.env.VITE_API_RETRY_ATTEMPTS) || 3,
    refreshInterval: parseInt(import.meta.env.VITE_REFRESH_INTERVAL) || 1800000 // 30 minutes default
  },
  staging: {
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'https://staging-api.social-dashboard.com/api/v1',
    timeout: parseInt(import.meta.env.VITE_API_TIMEOUT) || 30000,
    retryAttempts: parseInt(import.meta.env.VITE_API_RETRY_ATTEMPTS) || 3,
    refreshInterval: parseInt(import.meta.env.VITE_REFRESH_INTERVAL) || 1800000
  },
  production: {
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'https://api.social-dashboard.com/api/v1',
    timeout: parseInt(import.meta.env.VITE_API_TIMEOUT) || 30000,
    retryAttempts: parseInt(import.meta.env.VITE_API_RETRY_ATTEMPTS) || 5,
    refreshInterval: parseInt(import.meta.env.VITE_REFRESH_INTERVAL) || 1800000
  }
} as const;

export type Environment = keyof typeof API_ENVIRONMENTS;

// Get current environment from environment variables or default to development
export function getCurrentEnvironment(): Environment {
  const env = import.meta.env.VITE_APP_ENV as Environment;
  return env && env in API_ENVIRONMENTS ? env : 'development';
}

// Get API configuration for current environment
export function getApiConfig() {
  const currentEnv = getCurrentEnvironment();
  return API_ENVIRONMENTS[currentEnv];
}

// Initialize API configuration on app startup
export function initializeApiConfig() {
  const config = getApiConfig();

  // You can add the base URL to your ApiConfig class here
  // This allows dynamic environment switching
  if (typeof window !== 'undefined') {
    console.log(`🌐 API Environment: ${getCurrentEnvironment()}`);
    console.log(`🔗 API Base URL: ${config.baseUrl}`);
  }

  return config;
}
