import { useSearchHistory } from "@/stores/searchHistory.store";
import { useState, useEffect, useCallback } from "react";
import useSWR, { Key } from "swr";
import { useDebounce } from "use-debounce";

import { useSearchStore } from "@/stores/search.store";

interface UseSearchProps<T> {
  endpoint: string;
  fetcher: (url: string) => Promise<T>;
  debounceDelay?: number;
  minQueryLength?: number;
}

export function useSearch<T>({
  endpoint,
  fetcher,
  debounceDelay = 300,
  minQueryLength = 1,
}: UseSearchProps<T>) {
  const { searchQuery, setSearchQuery } = useSearchStore();
  const { addQuery } = useSearchHistory();
  // const [query, setQuery] = useState(initialQuery);
  const [debouncedQuery] = useDebounce(searchQuery, debounceDelay);
  const [shouldFetch, setShouldFetch] = useState(false);

  useEffect(() => {
    if (debouncedQuery.trim().length >= minQueryLength) {
      setShouldFetch(true);
    } else {
      setShouldFetch(false);
    }
  }, [debouncedQuery, minQueryLength]);

  const handleManualSearch = useCallback(() => {
    if (searchQuery.trim().length >= minQueryLength) {
      setShouldFetch(true);
      addQuery(searchQuery.trim());
    }
  }, [searchQuery, minQueryLength, addQuery]);

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
    query: searchQuery,
    setQuery: setSearchQuery,
    debouncedQuery,
    results: data,
    isLoading: isLoading || isValidating,
    isError: !!error,
    handleSearch: handleManualSearch,
    handleKeyDown,
    error,
  };
}
