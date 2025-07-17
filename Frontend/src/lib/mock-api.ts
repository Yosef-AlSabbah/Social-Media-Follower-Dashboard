// Mock data service to replace real API calls during development
import { PlatformData, AnalyticsSummary, GrowthTrendData } from '@/lib/api-centralized';

// Define ChartDataPoint interface here since it's not in api-centralized
interface ChartDataPoint {
  day: string;
  value: number;
  date: string;
}

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Mock platform data (simplified interface to match what Dashboard expects)
interface MockPlatformData {
  id: string;
  name: string;
  followers: number;
  engagement: number;
  growth: number;
  color: string;
}

const mockPlatforms: MockPlatformData[] = [
  {
    id: 'facebook',
    name: 'فيسبوك',
    followers: 125000,
    engagement: 4.2,
    growth: 12.5,
    color: '#1877F2'
  },
  {
    id: 'instagram',
    name: 'إنستغرام',
    followers: 89000,
    engagement: 6.8,
    growth: 18.3,
    color: '#E4405F'
  },
  {
    id: 'twitter',
    name: 'تويتر',
    followers: 45000,
    engagement: 3.1,
    growth: 8.7,
    color: '#1DA1F2'
  },
  {
    id: 'youtube',
    name: 'يوتيوب',
    followers: 67000,
    engagement: 7.9,
    growth: 22.1,
    color: '#FF0000'
  },
  {
    id: 'tiktok',
    name: 'تيك توك',
    followers: 156000,
    engagement: 9.4,
    growth: 45.6,
    color: '#FF0050'
  },
  {
    id: 'linkedin',
    name: 'لينكد إن',
    followers: 23000,
    engagement: 2.8,
    growth: 15.2,
    color: '#0A66C2'
  },
  {
    id: 'snapchat',
    name: 'سناب شات',
    followers: 34000,
    engagement: 5.6,
    growth: 11.9,
    color: '#FFFC00'
  }
];

// Mock analytics summary
const mockAnalyticsSummary: AnalyticsSummary = {
  totalFollowers: 539000,
  topPlatform: 'تيك توك',
  dailyGrowth: 2340
};

// Generate mock chart data
const generateMockChartData = (days: number = 7): ChartDataPoint[] => {
  return Array.from({ length: days }, (_, i) => {
    const date = new Date(Date.now() - (days - 1 - i) * 24 * 60 * 60 * 1000);
    return {
      day: date.toLocaleDateString('ar-SA', { weekday: 'short' }),
      date: date.toISOString().split('T')[0],
      value: Math.floor(1000 + Math.random() * 5000)
    };
  });
};

// Mock growth trends
const mockGrowthTrends: GrowthTrendData[] = mockPlatforms.map(platform => ({
  date: new Date().toISOString().split('T')[0],
  value: platform.followers,
  platform: platform.id
}));

// Mock API service
export class MockApiService {
  static async getAllPlatforms(): Promise<MockPlatformData[]> {
    await delay(800 + Math.random() * 400); // Random delay 800-1200ms
    return mockPlatforms;
  }

  static async getAnalyticsSummary(): Promise<AnalyticsSummary> {
    await delay(600 + Math.random() * 300); // Random delay 600-900ms
    return mockAnalyticsSummary;
  }

  static async getGrowthTrends(): Promise<GrowthTrendData[]> {
    await delay(500 + Math.random() * 200); // Random delay 500-700ms
    return mockGrowthTrends;
  }

  static async getPlatformById(platformId: string): Promise<MockPlatformData> {
    await delay(300 + Math.random() * 200); // Random delay 300-500ms
    const platform = mockPlatforms.find(p => p.id === platformId);
    if (!platform) {
      throw new Error(`Platform ${platformId} not found`);
    }
    return platform;
  }

  // Generate mock chart data for a platform
  static generateChartDataForPlatform(platformId: string): ChartDataPoint[] {
    const platform = mockPlatforms.find(p => p.id === platformId);
    const baseFollowers = platform?.followers || 1000;
    
    return Array.from({ length: 7 }, (_, i) => {
      const date = new Date(Date.now() - (6 - i) * 24 * 60 * 60 * 1000);
      const variation = 0.8 + Math.random() * 0.4; // 80% to 120% of base
      
      return {
        day: date.toLocaleDateString('ar-SA', { weekday: 'short' }),
        date: date.toISOString().split('T')[0],
        value: Math.floor(baseFollowers * variation)
      };
    });
  }
}