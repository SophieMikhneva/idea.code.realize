import { API_ROUTES } from "@/constants/route.constant";
import useSWR from "swr";

const fetcher = async (url: string): Promise<any[]> => {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Ошибка загрузки: ${response.statusText}`);
  }

  return response.json();
};

// TODO: Узнать структуру презентации и описать ее.

export const usePresentations = () => {
  const { data, error, isLoading } = useSWR<any[]>(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}${API_ROUTES.presentations}`,
    fetcher
  );

  return {
    presentations: data,
    isLoading,
    isError: !!error,
  };
};
