"use client";

import { usePresentations } from "@/hooks/usePresentations.hook";

export default function Homepage() {
  const { presentations, isLoading, isError } = usePresentations();

  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (isError) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-col w-full">
      {/* <Header /> */}
      <main className="w-full p-4">
        <div className="p-4">
          <h3 className="scroll-m-20 text-2xl font-semibold tracking-tight">
            Главная
          </h3>
          <p className="leading-7 text-[var(--muted-foreground)]">
            Здесь представлены все материалы
          </p>
        </div>
        <ul>
          {presentations?.map((presentation) => (
            <li>{presentation}</li>
          ))}
        </ul>
      </main>
    </div>
  );
}
