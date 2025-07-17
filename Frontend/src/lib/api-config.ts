/**
 * BACKEND API REQUIREMENTS
 *
 * This file defines the structure that the backend API must implement.
 * The frontend is configured to communicate with these specific endpoints
 * and expects responses in the format defined by the interfaces below.
 *
 * Required Backend Implementation:
 * 1. RESTful API with endpoints matching ApiEndpoints enum
 * 2. Response format following ApiSuccessResponse/ApiErrorResponse interfaces
 * 3. Data models matching the interfaces (PlatformData, AnalyticsSummary, etc.)
 * 4. Error handling with appropriate status codes and descriptive messages
 *
 * NOTE: All data fields use snake_case naming convention to match Python backend style
 */

import { getApiConfig } from './environment';

// API Configuration with centralized URL management
export enum ApiEndpoints {
  // Platform endpoints
  PLATFORMS = '/platforms',             // GET: Returns all platform data
  PLATFORM_STATS = '/platforms/{id}',   // GET: Returns data for a specific platform

  // Analytics endpoints
  SUMMARY = '/analytics/summary',       // GET: Returns summary statistics across all platforms
  GROWTH_TRENDS = '/analytics/growth-trends', // GET: Returns growth trends for charting
  DAILY_METRICS = '/analytics/daily-metrics', // GET: Returns daily metrics data
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

/**
 * API RESPONSE FORMAT REQUIREMENTS
 *
 * Backend must return responses in these formats:
 *
 * Success response:
 * {
 *   "success": true,
 *   "message": "Success message",
 *   "data": {}, // Actual data matching the appropriate interface
 *   "meta": {} // Optional pagination data
 * }
 *
 * Error response:
 * {
 *   "success": false,
 *   "message": "Error message",
 *   "data": null,
 *   "errors": {} // Detailed error information
 * }
 */

/**
 * REQUIRED DATA MODELS
 *
 * Backend must implement these data models and return them in the formats defined below.
 * All properties use snake_case naming to match Python backend conventions.
 */

/**
 * PlatformData: Information about each social media platform
 * Required fields:
 * - id: Unique identifier for the platform
 * - name: Display name of the platform
 * - name_ar: Arabic display name
 * - followers: Current follower count
 * - delta: Change in followers (positive or negative)
 * - color: Brand color for UI display
 * - is_active: Whether the platform is currently active
 * - last_updated: ISO timestamp of last data update
 */
export interface PlatformData {
  id: string;
  name: string;
  name_ar: string; // Changed from nameAr
  followers: number;
  delta: number;
  color: string;
  is_active: boolean; // Changed from isActive
  last_updated: string; // Changed from lastUpdated
}

/**
 * AnalyticsSummary: Overview statistics for the dashboard
 * Required fields:
 * - total_followers: Sum of followers across all platforms
 * - top_platform: Details about the best performing platform
 * - daily_growth: New followers in last 24 hours
 * - weekly_growth: New followers in last 7 days
 * - monthly_growth: New followers in last 30 days
 */
export interface AnalyticsSummary {
  total_followers: number; // Changed from totalFollowers
  top_platform: { // Changed from topPlatform
    id: string;
    name: string;
    name_ar: string; // Changed from nameAr
    followers: number;
  };
  daily_growth: number; // Changed from dailyGrowth
  weekly_growth: number; // Changed from weeklyGrowth
  monthly_growth: number; // Changed from monthlyGrowth
}

/**
 * ChartDataPoint: Individual data point for charts
 * Required fields:
 * - day: Display label for day
 * - value: Numeric value for the data point
 * - date: ISO format date
 */
export interface ChartDataPoint {
  // These field names are already short and clear, keeping them as is
  day: string;
  value: number;
  date: string;
}

/**
 * GrowthTrendData: Time-series data for charting growth trends
 * Required fields:
 * - platform_id: Which platform this data belongs to
 * - data: Array of data points for the chart
 */
export interface GrowthTrendData {
  platform_id: string; // Changed from platformId
  data: ChartDataPoint[];
}

/**
 * DailyMetric: Daily performance metrics
 * Required fields:
 * - date: ISO format date
 * - new_followers: New followers gained that day
 */
export interface DailyMetric {
  date: string;
  new_followers: number;
}
