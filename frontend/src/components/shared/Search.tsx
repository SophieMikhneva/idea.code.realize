// components/SearchComponent.tsx
"use client";

import { useSearch } from "@/hooks/useSearch.hook";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { API_ROUTES } from "@/constants/route.constant";

export function Search() {
  const { query, setQuery, results, isLoading, handleSearch, handleKeyDown } =
    useSearch<string[]>({
      endpoint: `${process.env.NEXT_PUBLIC_BACKEND_URL}${API_ROUTES.search}`,
      debounceDelay: 1000,
      minQueryLength: 2,
      fetcher: async (url) => {
        const res = await fetch(url);
        if (!res.ok) throw new Error("Search failed");
        return res.json();
      },
    });

  return (
    <div className="flex w-full max-w-md items-center space-x-2">
      <Input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Искать в хранилище..."
      />
      <Button onClick={handleSearch} disabled={isLoading}>
        {isLoading ? "Думаю..." : "Искать"}
      </Button>

      {results && (
        <div className="mt-4">
          {results.map((item, index) => (
            <div key={index}>{item}</div>
          ))}
        </div>
      )}
    </div>
  );
}
