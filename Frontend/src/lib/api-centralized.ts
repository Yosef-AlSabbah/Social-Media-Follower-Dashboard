/**
 * Centralized API Service
 * 
 * This file contains all API calls for the application.
 * Each function includes clear documentation about expected backend data format.
 * All API logic is isolated here for easy maintenance and extension.
 *
 * NOTE: All backend data properties use snake_case naming to match Python backend conventions.
 */

import { ApiConfig, ApiEndpoints } from './api-config';

// Types for API responses - these define what we expect from the backend
export interface PlatformData {
  id: string;
  name: string;
  followers: number;
  engagement: number;
  growth: number;
  icon: string;
  color: string;
}

export interface AnalyticsSummary {
  total_followers: number; // Changed from totalFollowers
  top_platform: string;    // Changed from topPlatform
  daily_growth: number;    // Changed from dailyGrowth
}

export interface GrowthTrendData {
  date: string;
  value: number;
  platform?: string;
}

export interface DailyMetric {
  date: string;
  value: number;
  change: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface ApiErrorResponse {
  success: false;
  message: string;
  errors?: Record<string, string[]>;
}

// Custom error class for API-specific errors
export class ApiError extends Error {
  constructor(
    message: string, 
    public status?: number, 
    public errors?: Record<string, string[]>
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Core API class with centralized request handling
 */
export class CentralizedApiService {
  private static readonly MAX_RETRIES = 3;
  private static readonly TIMEOUT = 10000;

  /**
   * Generic fetch wrapper with error handling, retries, and timeout
   */
  private static async request<T>(
    url: string, 
    options?: RequestInit
  ): Promise<T> {
    for (let attempt = 1; attempt <= this.MAX_RETRIES; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.TIMEOUT);

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
          throw new ApiError(`HTTP ${response.status}: ${response.statusText}`, response.status);
        }

        const result: ApiResponse<T> = await response.json();

        if (!result.success) {
          const errorResponse = result as ApiErrorResponse;
          throw new ApiError(errorResponse.message, response.status, errorResponse.errors);
        }

        return result.data;
      } catch (error) {
        if (attempt === this.MAX_RETRIES) {
          if (error instanceof ApiError) throw error;
          if (error instanceof Error && error.name === 'AbortError') {
            throw new ApiError(`Request timeout after ${this.TIMEOUT}ms`, 504);
          }
          throw new ApiError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }

        // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt - 1) * 1000));
      }
    }

    throw new ApiError('Maximum retry attempts exceeded');
  }

  /**
   * Platform Management APIs
   */

  /**
   * Get all social media platforms with their current stats
   * Backend should return: Array of platforms with follower counts, engagement rates, etc.
   * Expected format: { id, name, followers, engagement, growth, icon, color }[]
   */
  static async getAllPlatforms(): Promise<PlatformData[]> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.PLATFORMS);
    return this.request<PlatformData[]>(url);
  }

  /**
   * Get detailed stats for a specific platform
   * Backend should return: Single platform object with detailed metrics
   * Expected format: { id, name, followers, engagement, growth, icon, color, additionalMetrics? }
   */
  static async getPlatformById(platform_id: string): Promise<PlatformData> { // Changed from platformId
    const url = ApiConfig.getFullUrl(ApiEndpoints.PLATFORM_STATS, { id: platform_id });
    return this.request<PlatformData>(url);
  }

  /**
   * Analytics Summary APIs
   */

  /**
   * Get high-level analytics summary for dashboard
   * Backend should return: Aggregated metrics across all platforms
   * Expected format: { total_followers: number, top_platform: string, daily_growth: number }
   */
  static async getAnalyticsSummary(): Promise<AnalyticsSummary> {
    const url = ApiConfig.getFullUrl(ApiEndpoints.SUMMARY);
    return this.request<AnalyticsSummary>(url);
  }

  /**
   * Growth and Trend APIs
   */

  /**
   * Get growth trend data for charts
   * Backend should return: Time-series data showing growth over time
   * Expected format: { date: string (ISO), value: number, platform?: string }[]
   */
  static async getGrowthTrends(
    time_range?: '7d' | '30d' | '90d' | '1y', // Changed from timeRange
    platform_id?: string                      // Changed from platformId
  ): Promise<GrowthTrendData[]> {
    const params = new URLSearchParams();
    if (time_range) params.append('range', time_range);
    if (platform_id) params.append('platform', platform_id);

    const url = `${ApiConfig.getFullUrl(ApiEndpoints.GROWTH_TRENDS)}?${params.toString()}`;
    return this.request<GrowthTrendData[]>(url);
  }

  /**
   * Get daily metrics for detailed analysis
   * Backend should return: Daily breakdown of key metrics
   * Expected format: { date: string (ISO), value: number, change: number }[]
   */
  static async getDailyMetrics(days: number = 30): Promise<DailyMetric[]> {
    const url = `${ApiConfig.getFullUrl(ApiEndpoints.DAILY_METRICS)}?days=${days}`;
    return this.request<DailyMetric[]>(url);
  }

  /**
   * Real-time Data APIs
   */

  /**
   * Create a polling subscription for real-time updates
   * Useful for dashboard components that need live data
   */
  static createPollingService<T>(
    apiCall: () => Promise<T>,
    onUpdate: (data: T) => void,
    onError: (error: ApiError) => void,
    intervalMs: number = 30000
  ): { start: () => void; stop: () => void; isActive: () => boolean } {
    let intervalId: NodeJS.Timeout | null = null;
    let isPolling = false;

    const poll = async () => {
      if (!isPolling) return;

      try {
        const data = await apiCall();
        onUpdate(data);
      } catch (error) {
        const apiError = error instanceof ApiError ? error : new ApiError('Polling failed');
        onError(apiError);
      }
    };

    return {
      start: () => {
        if (!isPolling) {
          isPolling = true;
          poll(); // Initial fetch
          intervalId = setInterval(poll, intervalMs);
        }
      },
      stop: () => {
        isPolling = false;
        if (intervalId) {
          clearInterval(intervalId);
          intervalId = null;
        }
      },
      isActive: () => isPolling
    };
  }

  /**
   * Batch API Operations
   */

  /**
   * Fetch multiple API endpoints simultaneously
   * Useful for dashboard initialization
   */
  static async batchFetch<T extends Record<string, any>>(
    requests: Record<keyof T, () => Promise<T[keyof T]>>
  ): Promise<T> {
    const entries = Object.entries(requests) as [keyof T, () => Promise<T[keyof T]>][];
    const promises = entries.map(async ([key, apiCall]) => {
      try {
        const data = await apiCall();
        return [key, { data, error: null }];
      } catch (error) {
        const apiError = error instanceof ApiError ? error : new ApiError('Batch request failed');
        return [key, { data: null, error: apiError }];
      }
    });

    const results = await Promise.all(promises);
    return Object.fromEntries(results) as T;
  }

  /**
   * Health Check APIs
   */

  /**
   * Check API health and connectivity
   * Backend should return: Simple status indicator
   * Expected format: { status: 'healthy' | 'degraded' | 'down', timestamp: string }
   */
  static async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const url = `${ApiConfig.getBaseUrl()}/health`;
    return this.request<{ status: string; timestamp: string }>(url);
  }
}

// Export singleton instance for consistency
export const ApiClient = CentralizedApiService;