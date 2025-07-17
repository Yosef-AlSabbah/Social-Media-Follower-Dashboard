import { useState, useEffect } from 'react';

// Hook to manage splash screen state
export function useSplashScreen(minDuration: number = 2000) {
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, minDuration);

    return () => clearTimeout(timer);
  }, [minDuration]);

  return showSplash;
}