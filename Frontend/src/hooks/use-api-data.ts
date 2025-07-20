import { useState, useEffect, useCallback, useRef, DependencyList } from 'react';
import { RealApiService, Platform, AnalyticsSummary, GrowthTrend } from '@/lib/real-api-service';

export interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useApiData<T>(
  apiMethod: () => Promise<T>,
  dependencies: DependencyList = [],
  enablePolling: boolean = false,
  pollingInterval: number = 30000
): UseApiState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);
  const mountedRef = useRef(true);

  const fetchData = useCallback(async () => {
    if (!mountedRef.current) return;

    try {
      setError(null);
      if (data === null) setLoading(true); // Only show loading on initial fetch
      const result = await apiMethod();
      if (mountedRef.current) {
        setData(result);
      }
    } catch (err) {
      if (mountedRef.current) {
        const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
        setError(errorMessage);
        console.error('API Error:', err);
      }
    } finally {
      if (mountedRef.current) {
        setLoading(false);
      }
    }
  }, []); // Remove dependencies to prevent infinite re-creation

  // Initial fetch - only run once
  useEffect(() => {
    fetchData();
  }, []); // Empty dependency array for initial fetch only

  // Polling effect - separate from initial fetch
  useEffect(() => {
    if (enablePolling && !loading && !error && data !== null) {
      pollingRef.current = setInterval(() => {
        if (mountedRef.current) {
          fetchData();
        }
      }, pollingInterval);

      return () => {
        if (pollingRef.current) {
          clearInterval(pollingRef.current);
          pollingRef.current = null;
        }
      };
    }
  }, [enablePolling, pollingInterval, loading, error, data]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      mountedRef.current = false;
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
        pollingRef.current = null;
      }
    };
  }, []);

  return {
    data,
    loading,
    error,
    refetch: fetchData
  };
}

// Specific hooks for different data types
export function usePlatformData(enablePolling: boolean = true) {
  const refreshInterval = RealApiService.getRefreshInterval();
  return useApiData(
    () => RealApiService.getAllPlatforms(),
    [],
    enablePolling,
    refreshInterval
  );
}

export function useAnalyticsSummary(enablePolling: boolean = true) {
  const refreshInterval = RealApiService.getRefreshInterval();
  return useApiData(
    () => RealApiService.getAnalyticsSummary(),
    [],
    enablePolling,
    refreshInterval
  );
}

export function useGrowthTrends() {
  return useApiData(
    () => RealApiService.getGrowthTrends(),
    [],
    false // Growth trends don't need real-time updates
  );
}
