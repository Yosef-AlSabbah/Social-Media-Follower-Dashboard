import { ApiConfig, ApiEndpoints, PlatformData, AnalyticsSummary, GrowthTrendData, ApiResponse, DailyMetric, ApiErrorPayload, ApiErrorResponse } from './api-config';

class ApiError extends Error {
  constructor(message: string, public status?: number, public errors?: ApiErrorPayload) {
    super(message);
    this.name = 'ApiError';
  }
}

export class ApiService {
  private static async fetchWithError<T>(url: string, options?: RequestInit): Promise<T> {
    const maxRetries = ApiConfig.getRetryAttempts();
    const timeout = ApiConfig.getTimeout();

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        const response = await fetch(url, {
          headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
          },
          signal: controller.signal,
          ...options,
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          throw new ApiError(`HTTP error! status: ${response.status}`);
        }

        const result: ApiResponse<T> = await response.json();

        if (!result.success) {
          const errorResponse = result as ApiErrorResponse;
          throw new ApiError(errorResponse.message, response.status, errorResponse.errors);
        }

        return result.data;
      } catch (error) {
        // If this is the last attempt, throw the error
        if (attempt === maxRetries) {
          if (error instanceof ApiError) {
            throw error;
          }
          if (error instanceof Error && error.name === 'AbortError') {
            throw new ApiError(`Request timeout after ${timeout}ms`, 504);
          }
          throw new ApiError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }

        // Wait before retrying (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt - 1) * 1000));
      }
    }

    throw new ApiError('Maximum retry attempts exceeded');
  }

  // Platform data methods
  static async getAllPlatforms(): Promise<PlatformData[]> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.PLATFORMS);
    return this.fetchWithError<PlatformData[]>(url);
  }

  static async getPlatformById(platformId: string): Promise<PlatformData> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.PLATFORM_DETAIL, { id: platformId });
    return this.fetchWithError<PlatformData>(url);
  }

  // Analytics methods
  static async getAnalyticsSummary(): Promise<AnalyticsSummary> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.ANALYTICS_SUMMARY);
    return this.fetchWithError<AnalyticsSummary>(url);
  }

  static async getGrowthTrends(): Promise<GrowthTrendData[]> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.ANALYTICS_GROWTH_TRENDS);
    return this.fetchWithError<GrowthTrendData[]>(url);
  }

  static async getDailyMetrics(): Promise<DailyMetric[]> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.ANALYTICS_DAILY_METRICS);
    return this.fetchWithError<DailyMetric[]>(url);
  }

  // Cache management methods
  static async invalidateCache(): Promise<void> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.ANALYTICS_INVALIDATE_CACHE);
    return this.fetchWithError<void>(url, { method: 'POST' });
  }

  static async forceRefresh(): Promise<void> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.ANALYTICS_FORCE_REFRESH);
    return this.fetchWithError<void>(url, { method: 'POST' });
  }

  // Utility method for polling data
  static createPollingSubscription<T>(
    apiMethod: () => Promise<T>,
    callback: (data: T) => void,
    errorCallback: (error: Error) => void,
    intervalMs: number = 30000
  ): { start: () => void; stop: () => void } {
    let intervalId: NodeJS.Timeout | null = null;
    let isActive = false;

    const pollData = async () => {
      if (!isActive) return;

      try {
        const data = await apiMethod();
        callback(data);
      } catch (error) {
        errorCallback(error instanceof Error ? error : new Error('Unknown polling error'));
      }
    };

    return {
      start: () => {
        if (!isActive) {
          isActive = true;
          pollData(); // Initial fetch
          intervalId = setInterval(pollData, intervalMs);
        }
      },
      stop: () => {
        isActive = false;
        if (intervalId) {
          clearInterval(intervalId);
          intervalId = null;
        }
      }
    };
  }
}

export { ApiError };
