import { useState, useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { ThemeProvider } from '@/components/ThemeProvider'
import { Dashboard } from '@/components/Dashboard'
import { Footer } from '@/components/Footer'
import { SplashScreen } from '@/components/SplashScreen'
import { useSplashScreen } from '@/hooks/use-splash-screen'
import { usePlatformData, useAnalyticsSummary, useGrowthTrends } from '@/hooks/use-api-data'

const Index = () => {
  // Get data loading status
  const { data: platforms, loading: platformsLoading } = usePlatformData(true);
  const { data: analyticsData, loading: analyticsLoading } = useAnalyticsSummary(true);
  const { data: growthTrends, loading: trendsLoading } = useGrowthTrends();

  // Check if essential data is loaded
  const dataLoaded = !platformsLoading && !analyticsLoading && !trendsLoading &&
                     platforms && analyticsData && growthTrends;

  // Show splash for 2 seconds minimum, hide when data is ready
  const showSplash = useSplashScreen(2000, dataLoaded);

  // State for showing loading overlay after splash
  const [showLoadingOverlay, setShowLoadingOverlay] = useState(false);

  // When splash ends, show loading overlay for additional 2 seconds
  useEffect(() => {
    if (!showSplash) {
      setShowLoadingOverlay(true);

      const overlayTimer = setTimeout(() => {
        setShowLoadingOverlay(false);
      }, 2000); // Exactly 2 seconds

      return () => clearTimeout(overlayTimer);
    }
  }, [showSplash]);

  return (
    <ThemeProvider defaultTheme="dark">
      <AnimatePresence mode="wait">
        {showSplash ? (
          <SplashScreen key="splash" />
        ) : (
          <div key="main">
            <Dashboard />
            <Footer />
            {/* Smooth loading overlay that allows scrolling */}
            <AnimatePresence>
              {showLoadingOverlay && (
                <motion.div
                  key="loading-overlay"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  className="fixed inset-0 z-40 flex items-center justify-center bg-background/60 backdrop-blur-sm pointer-events-none"
                >
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.8, opacity: 0 }}
                    transition={{ duration: 0.3, ease: "easeOut" }}
                    className="text-center space-y-4 bg-card/80 p-6 rounded-2xl border border-border/50 shadow-lg"
                  >
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent mx-auto"></div>
                    <p className="text-lg text-foreground arabic-text">جاري تحديث البيانات...</p>
                  </motion.div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </AnimatePresence>
    </ThemeProvider>
  );
};

export default Index;
