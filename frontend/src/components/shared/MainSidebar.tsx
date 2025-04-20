"use client";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useSearchHistory } from "@/stores/searchHistory.store";

import { Fragment, JSX } from "react";
import { Button } from "../ui/button";
import { useSearch } from "@/hooks/useSearch.hook";
import { API_ROUTES } from "@/constants/route.constant";

const MainSidebar = (): JSX.Element => {
  const { history, clearHistory } = useSearchHistory();
  const { setQuery } = useSearch<string[]>({
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
    <Sidebar>
      <SidebarHeader />
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Недавние</SidebarGroupLabel>
          <SidebarMenu>
            {history.length ? (
              <>
                {history.map((item) => (
                  <SidebarMenuItem
                    key={item.timestamp}
                    className="px-2"
                    onClick={() => setQuery(item.query)}
                  >
                    <SidebarMenuButton>{item.query}</SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
                <Button onClick={() => clearHistory()}>Очистить</Button>
              </>
            ) : (
              <p className="leading-7 px-2">Здесь появятся посление запросы</p>
            )}
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
};

export default MainSidebar;
