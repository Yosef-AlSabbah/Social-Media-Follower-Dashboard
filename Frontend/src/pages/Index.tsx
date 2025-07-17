import { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { ThemeProvider } from '@/components/ThemeProvider'
import { Dashboard } from '@/components/Dashboard'
import { Footer } from '@/components/Footer'
import { SplashScreen } from '@/components/SplashScreen'
import { useSplashScreen } from '@/hooks/use-splash-screen'

const Index = () => {
  const showSplash = useSplashScreen(3000); // Show splash for 3 seconds

  return (
    <ThemeProvider defaultTheme="dark">
      <AnimatePresence mode="wait">
        {showSplash ? (
          <SplashScreen key="splash" />
        ) : (
          <div key="main">
            <Dashboard />
            <Footer />
          </div>
        )}
      </AnimatePresence>
    </ThemeProvider>
  );
};

export default Index;
