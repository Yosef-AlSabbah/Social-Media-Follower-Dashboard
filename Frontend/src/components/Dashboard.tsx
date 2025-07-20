import { Facebook, Twitter, Instagram, Play, Youtube, Camera, Linkedin, LucideIcon } from 'lucide-react';
import { Header } from './Header'
import { PlatformCard } from './PlatformCard'
import { AnalyticsSummary } from './AnalyticsSummary'
import { SimpleChart } from './SimpleChart'
import { LoadingOverlay } from './LoadingOverlay'
import { usePlatformData, useAnalyticsSummary, useGrowthTrends } from '@/hooks/use-api-data'
import { MockApiService } from '@/lib/mock-api'

// Icon mapping for platforms - using lowercase platform names
const platformIcons: Record<string, LucideIcon> = {
  facebook: Facebook,
  twitter: Twitter,
  instagram: Instagram,
  tiktok: Play,
  youtube: Youtube,
  snapchat: Camera,
  linkedin: Linkedin,
};

export function Dashboard() {
  const {
    data: platforms,
    loading: platformsLoading,
    error: platformsError
  } = usePlatformData(true) // Enable polling for real-time updates

  const {
    data: analyticsData,
    loading: analyticsLoading,
    error: analyticsError
  } = useAnalyticsSummary(true)

  const {
    data: growthTrends,
    loading: trendsLoading,
    error: trendsError
  } = useGrowthTrends()

  // Map platforms with their icons - using platform name instead of id
  const platformsWithIcons = platforms?.map(platform => ({
    ...platform,
    icon: platformIcons[platform.name.toLowerCase()] || Facebook
  })) || []

  // Check if any data is currently being loaded/updated
  const isUpdating = platformsLoading || analyticsLoading || trendsLoading

  // Error handling
  if (platformsError || analyticsError || trendsError) {
    return (
      <div className="min-h-screen bg-background p-6">
        <div className="max-w-7xl mx-auto">
          <Header />
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-destructive mb-4">خطأ في تحميل البيانات</h2>
              <p className="text-muted-foreground">
                {platformsError || analyticsError || trendsError}
              </p>
              <button
                onClick={() => window.location.reload()}
                className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
              >
                إعادة المحاولة
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <>
      <LoadingOverlay isVisible={isUpdating} />
      <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto">
        <Header />
        
        <AnalyticsSummary
          totalFollowers={analyticsData?.total_followers || 0}
          topPlatform={analyticsData?.top_platform?.name_ar || 'غير محدد'}
          dailyGrowth={analyticsData?.daily_growth || 0}
          isLoading={analyticsLoading}
        />

        <div className="mb-10">
          <h2 className="text-3xl font-bold mb-8 text-foreground bg-gradient-to-r from-foreground to-accent bg-clip-text">
            منصات التواصل الاجتماعي
          </h2>
          <div className="responsive-grid">
            {platformsLoading ? (
              Array.from({ length: 7 }).map((_, index) => (
                <PlatformCard
                  key={index}
                  platform=""
                  followers={0}
                  delta={0}
                  icon={Facebook}
                  color="#000000"
                  platformId=""
                  isLoading={true}
                />
              ))
            ) : (
              platformsWithIcons.map((platform) => (
                <PlatformCard
                  key={platform.id}
                  platform={platform.name_ar}
                  followers={platform.followers}
                  delta={platform.delta}
                  icon={platform.icon}
                  color={platform.color}
                  platformId={platform.id}
                />
              ))
            )}
          </div>
        </div>

        <div className="mb-10">
          <h2 className="text-3xl font-bold mb-8 text-foreground bg-gradient-to-r from-foreground to-secondary bg-clip-text">
            اتجاهات النمو لجميع المنصات
          </h2>
          <div className="responsive-chart-grid">
            {trendsLoading || !platformsWithIcons.length ? (
              Array.from({ length: 7 }).map((_, index) => (
                <div key={index} className="chart-container animate-pulse">
                  <div className="h-6 bg-muted rounded-lg mb-6 w-3/4"></div>
                  <div className="h-72 bg-muted/50 rounded-lg"></div>
                </div>
              ))
            ) : (
              platformsWithIcons.map((platform, index) => {
                // Find real growth trend data for this platform
                const platformTrendData = growthTrends?.find(trend => trend.platform_id === platform.id);
                let chartData = platformTrendData?.data || [];

                // Fallback to mock data if no real data is available
                if (!chartData || chartData.length === 0) {
                  console.warn(`⚠️ No growth data found for ${platform.name}, using mock data`);
                  chartData = MockApiService.generateChartDataForPlatform(platform.id);
                }

                // Enhanced debug logging for all platforms to see what's happening
                console.log(`📊 Platform Debug - ${platform.name}:`, {
                  platformId: platform.id,
                  platformName: platform.name,
                  platformNameLower: platform.name.toLowerCase(),
                  foundTrendData: !!platformTrendData,
                  chartDataLength: chartData.length,
                  chartData: chartData,
                  allGrowthTrendsIds: growthTrends?.map(t => t.platform_id) || [],
                  usingMockData: !platformTrendData?.data?.length
                });

                const variants = ['accent', 'secondary', 'primary'] as const;
                const variant = variants[index % 3];
                return (
                  <SimpleChart
                    key={platform.id}
                    data={chartData}
                    variant={variant}
                    title={`نمو المتابعين - ${platform.name_ar}`}
                  />
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
    </>
  )
}