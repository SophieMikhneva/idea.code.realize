import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

interface SearchHistoryItem {
  query: string;
  timestamp: number;
}

interface SearchHistoryState {
  history: SearchHistoryItem[];
  addQuery: (query: string) => void;
  clearHistory: () => void;
  removeQuery: (query: string) => void;
}

export const useSearchHistory = create<SearchHistoryState>()(
  persist(
    (set) => ({
      history: [],
      addQuery: (query) =>
        set((state) => {
          const newHistory = [
            { query, timestamp: Date.now() },
            ...state.history.filter((item) => item.query !== query),
          ].slice(0, 10);

          return { history: newHistory };
        }),
      clearHistory: () => set({ history: [] }),
      removeQuery: (query) =>
        set((state) => ({
          history: state.history.filter((item) => item.query !== query),
        })),
    }),
    {
      name: "search-history-storage",
      storage: createJSONStorage(() => localStorage),
      onRehydrateStorage: () => (state) => {
        if (state) {
          const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;
          state.history = state.history.filter(
            (item) => item.timestamp > oneDayAgo
          );
        }
      },
    }
  )
);
