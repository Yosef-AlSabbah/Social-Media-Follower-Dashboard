/**
 * Real API Service matching the OpenAPI specification
 * This replaces the mock API with actual backend calls
 */

import { getApiConfig } from './environment';

// OpenAPI response types
export interface Platform {
  id: string;
  name: string;
  name_ar: string;
  followers: number; // Changed from string to number
  delta: number; // Changed from string to number
  color: string;
  is_active: boolean;
  last_updated: string;
}

export interface TopPlatform {
  id: string;
  name: string;
  name_ar: string;
  followers: number;
}

export interface AnalyticsSummary {
  total_followers: number;
  top_platform: TopPlatform;
  daily_growth: number;
  weekly_growth: number;
  monthly_growth: number;
}

export interface DailyDataPoint {
  day: string;
  value: number;
  date: string;
}

export interface GrowthTrend {
  platform_id: string;
  data: DailyDataPoint[];
}

export interface DailyMetric {
  date: string;
  new_followers: number;
}

// Backend API Response wrapper interface
interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

// Custom error class
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

export class RealApiService {
  private static config = getApiConfig();

  private static async fetchWithRetry<T>(
    url: string,
    options?: RequestInit,
    retries: number = 0
  ): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.config.timeout);

    try {
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

      // Handle wrapped response format
      if (!result.success) {
        throw new ApiError(result.message || 'API request failed');
      }

      return result.data;
    } catch (error) {
      clearTimeout(timeoutId);

      if (retries < this.config.retryAttempts - 1) {
        await new Promise((resolve) => setTimeout(resolve, Math.pow(2, retries) * 1000));
        return this.fetchWithRetry(url, options, retries + 1);
      }

      if (error instanceof ApiError) throw error;
      if (error instanceof Error && error.name === 'AbortError') {
        throw new ApiError(`Request timeout after ${this.config.timeout}ms`, 504);
      }
      throw new ApiError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  static async getAllPlatforms(): Promise<Platform[]> {
    const url = `${this.config.baseUrl}/metrics/platforms/`;
    return this.fetchWithRetry<Platform[]>(url);
  }

  static async getPlatformById(id: string): Promise<Platform> {
    const url = `${this.config.baseUrl}/metrics/platforms/${id}/`;
    return this.fetchWithRetry<Platform>(url);
  }

  static async getAnalyticsSummary(): Promise<AnalyticsSummary> {
    const url = `${this.config.baseUrl}/metrics/analytics/summary/`;
    return this.fetchWithRetry<AnalyticsSummary>(url);
  }

  static async getGrowthTrends(): Promise<GrowthTrend[]> {
    const url = `${this.config.baseUrl}/metrics/analytics/growth-trends/`;
    return this.fetchWithRetry<GrowthTrend[]>(url);
  }

  static async getDailyMetrics(): Promise<DailyMetric[]> {
    const url = `${this.config.baseUrl}/metrics/analytics/daily-metrics/`;
    return this.fetchWithRetry<DailyMetric[]>(url);
  }

  static async invalidateCache(): Promise<void> {
    const url = `${this.config.baseUrl}/metrics/analytics/invalidate-cache/`;
    await this.fetchWithRetry<void>(url, { method: 'POST' });
  }

  static async forceRefresh(): Promise<void> {
    const url = `${this.config.baseUrl}/metrics/analytics/force-refresh/`;
    await this.fetchWithRetry<void>(url, { method: 'POST' });
  }

  static getRefreshInterval(): number {
    return this.config.refreshInterval;
  }
}