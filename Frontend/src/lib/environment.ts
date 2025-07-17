// Environment-specific API configuration
export const API_ENVIRONMENTS = {
  development: {
    baseUrl: 'http://localhost:3001/api/v1',
    timeout: 10000,
    retryAttempts: 3
  },
  staging: {
    baseUrl: 'https://staging-api.social-dashboard.com/v1',
    timeout: 15000,
    retryAttempts: 3
  },
  production: {
    baseUrl: 'https://api.social-dashboard.com/v1',
    timeout: 20000,
    retryAttempts: 5
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
