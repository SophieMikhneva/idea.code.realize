import { useState, useEffect, useCallback } from "react";
import useSWR, { Key } from "swr";
import { useDebounce } from "use-debounce";

interface UseSearchProps<T> {
  endpoint: string;
  initialQuery?: string;
  fetcher: (url: string) => Promise<T>;
  debounceDelay?: number;
  minQueryLength?: number;
}

export function useSearch<T>({
  endpoint,
  initialQuery = "",
  fetcher,
  debounceDelay = 300,
  minQueryLength = 1,
}: UseSearchProps<T>) {
  const [query, setQuery] = useState(initialQuery);
  const [debouncedQuery] = useDebounce(query, debounceDelay);
  const [shouldFetch, setShouldFetch] = useState(false);

  useEffect(() => {
    if (debouncedQuery.trim().length >= minQueryLength) {
      setShouldFetch(true);
    } else {
      setShouldFetch(false);
    }
  }, [debouncedQuery, minQueryLength]);

  const handleManualSearch = useCallback(() => {
    if (query.trim().length >= minQueryLength) {
      setShouldFetch(true);
    }
  }, [query, minQueryLength]);

  const swrKey: Key =
    shouldFetch && debouncedQuery.trim()
      ? `${endpoint}?query=${encodeURIComponent(debouncedQuery)}`
      : null;

  const { data, error, isLoading, isValidating } = useSWR<T>(swrKey, fetcher, {
    revalidateOnFocus: false,
    shouldRetryOnError: false,
  });

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleManualSearch();
    }
  };

  return {
    query,
    setQuery,
    debouncedQuery,
    results: data,
    isLoading: isLoading || isValidating,
    isError: !!error,
    handleSearch: handleManualSearch,
    handleKeyDown,
    error,
  };
}
