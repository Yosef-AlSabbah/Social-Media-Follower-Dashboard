import { useState, useEffect } from 'react';

// Hook to manage splash screen state with data loading awareness
export function useSplashScreen(minDuration: number = 1000, dataLoaded: boolean = false) {
  const [showSplash, setShowSplash] = useState(true);
  const [minTimeElapsed, setMinTimeElapsed] = useState(false);

  useEffect(() => {
    // Minimum time timer
    const timer = setTimeout(() => {
      setMinTimeElapsed(true);
    }, minDuration);

    return () => clearTimeout(timer);
  }, [minDuration]);

  useEffect(() => {
    // Hide splash when both conditions are met:
    // 1. Minimum time has elapsed (1 second)
    // 2. Data is loaded (or we don't care about data loading)
    if (minTimeElapsed && (dataLoaded || !dataLoaded)) {
      // Small delay to ensure smooth transition
      const hideTimer = setTimeout(() => {
        setShowSplash(false);
      }, 100);

      return () => clearTimeout(hideTimer);
    }
  }, [minTimeElapsed, dataLoaded]);

  return showSplash;
}