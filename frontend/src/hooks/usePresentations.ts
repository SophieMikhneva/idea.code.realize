import useSWR from "swr";

interface Presentation {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  // Добавь нужные поля
}

const fetcher = async (url: string): Promise<Presentation[]> => {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Ошибка загрузки: ${response.statusText}`);
  }

  return response.json();
};

export const usePresentations = () => {
  const { data, error, isLoading, mutate } = useSWR<Presentation[]>(
    "/api/presentations",
    fetcher
  );

  return {
    presentations: data,
    isLoading,
    isError: !!error,
    mutate,
  };
};
