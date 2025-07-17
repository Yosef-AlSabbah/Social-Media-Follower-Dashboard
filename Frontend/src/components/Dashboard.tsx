import { Facebook, Twitter, Instagram, Play, Youtube, Camera, Linkedin, LucideIcon } from 'lucide-react';
import { Header } from './Header'
import { PlatformCard } from './PlatformCard'
import { AnalyticsSummary } from './AnalyticsSummary'
import { SimpleChart } from './SimpleChart'
import { LoadingOverlay } from './LoadingOverlay'
import { usePlatformData, useAnalyticsSummary, useGrowthTrends } from '@/hooks/use-api-data'
import { MockApiService } from '@/lib/mock-api'

// Icon mapping for platforms
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

  // Map platforms with their icons
  const platformsWithIcons = platforms?.map(platform => ({
    ...platform,
    icon: platformIcons[platform.id] || Facebook
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
          totalFollowers={analyticsData?.totalFollowers || 0}
          topPlatform={analyticsData?.topPlatform || 'غير محدد'}
          dailyGrowth={analyticsData?.dailyGrowth || 0}
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
                  platform={platform.name}
                  followers={platform.followers}
                  delta={platform.growth}
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
                // Use mock chart data for each platform
                const chartData = MockApiService.generateChartDataForPlatform(platform.id);
                
                const variants = ['accent', 'secondary', 'primary'] as const;
                const variant = variants[index % 3];
                return (
                  <SimpleChart
                    key={platform.id}
                    data={chartData}
                    variant={variant}
                    title={`نمو المتابعين - ${platform.name}`}
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