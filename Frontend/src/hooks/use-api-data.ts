import { useState, useEffect, useCallback, DependencyList } from 'react';
import { MockApiService } from '@/lib/mock-api';
import { AnalyticsSummary, GrowthTrendData } from '@/lib/api-centralized';

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

  const fetchData = useCallback(async () => {
    try {
      setError(null);
      if (data === null) setLoading(true); // Only show loading on initial fetch
      const result = await apiMethod();
      setData(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  }, [apiMethod, ...dependencies]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    if (enablePolling && !loading && !error) {
      const interval = setInterval(() => {
        if (!loading) {
          fetchData();
        }
      }, pollingInterval);

      return () => clearInterval(interval);
    }
  }, [enablePolling, pollingInterval, loading, error, fetchData]);

  return {
    data,
    loading,
    error,
    refetch: fetchData
  };
}

// Specific hooks for different data types
export function usePlatformData(enablePolling: boolean = true) {
  return useApiData(
    () => MockApiService.getAllPlatforms(),
    [],
    enablePolling,
    30000
  );
}

export function useAnalyticsSummary(enablePolling: boolean = true) {
  return useApiData(
    () => MockApiService.getAnalyticsSummary(),
    [],
    enablePolling,
    60000 // Analytics summary updates less frequently
  );
}

export function useGrowthTrends() {
  return useApiData(
    () => MockApiService.getGrowthTrends(),
    [],
    false // Growth trends don't need real-time updates
  );
}
