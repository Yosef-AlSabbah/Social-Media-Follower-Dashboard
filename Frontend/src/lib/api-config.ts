import { getApiConfig } from './environment';

// API Configuration with centralized URL management
export enum ApiEndpoints {
  // Platform endpoints - matching OpenAPI spec
  PLATFORMS = '/metrics/platforms/',
  PLATFORM_DETAIL = '/metrics/platforms/{id}/',

  // Analytics endpoints - matching OpenAPI spec
  ANALYTICS_SUMMARY = '/metrics/analytics/summary/',
  ANALYTICS_GROWTH_TRENDS = '/metrics/analytics/growth-trends/',
  ANALYTICS_DAILY_METRICS = '/metrics/analytics/daily-metrics/',
  ANALYTICS_INVALIDATE_CACHE = '/metrics/analytics/invalidate-cache/',
  ANALYTICS_FORCE_REFRESH = '/metrics/analytics/force-refresh/',
}

export class ApiConfig {
  private static config = getApiConfig();

  static getFullUrl(endpoint: ApiEndpoints, params?: Record<string, string>): string {
    let url = `${this.config.baseUrl}${endpoint}`;

    // Replace path parameters
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url = url.replace(`{${key}}`, value);
      });
    }
    
    return url;
  }

  static getTimeout(): number {
    return this.config.timeout;
  }

  static getRetryAttempts(): number {
    return this.config.retryAttempts;
  }

  static getBaseUrl(): string {
    return this.config.baseUrl;
  }

  static refreshConfig(): void {
    this.config = getApiConfig();
  }
}

// API Response Types - Updated to match OpenAPI specification
export interface Pagination {
  count: number;
  next: string | null;
  previous: string | null;
  total_pages: number;
  current_page: number;
  page_size: number;
}

export interface Meta {
  pagination: Pagination;
}

export interface ApiErrorPayload {
  [key: string]: string[];
}

export interface ApiSuccessResponse<T> {
  success: true;
  message: string;
  data: T;
  meta?: Meta;
}

export interface ApiErrorResponse {
  success: false;
  message: string;
  data: Record<string, unknown> | null;
  errors?: ApiErrorPayload;
}

export type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse;

// Platform interface matching OpenAPI schema
export interface PlatformData {
  id: string;
  name: string;
  name_ar: string;
  followers: number;
  delta: number;
  color: string;
  is_active: boolean;
  last_updated: string;
}

// Analytics Summary interface matching OpenAPI schema
export interface AnalyticsSummary {
  total_followers: number;
  top_platform: {
    id: string;
    name: string;
    name_ar: string;
    followers: number;
  };
  daily_growth: number;
  weekly_growth: number;
  monthly_growth: number;
}

// Daily Data Point interface matching OpenAPI schema
export interface DailyDataPoint {
  day: string;
  value: number;
  date: string;
}

// Growth Trend interface matching OpenAPI schema
export interface GrowthTrendData {
  platform_id: string;
  data: DailyDataPoint[];
}

// Daily Metric interface matching OpenAPI schema
export interface DailyMetric {
  date: string;
  new_followers: number;
}
