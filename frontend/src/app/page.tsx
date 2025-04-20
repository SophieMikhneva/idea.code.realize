"use client";

import { disciplines } from "@/constants/presentation.constant";
import DisciplineCard from "@/components/shared/DisciplineCard";
import { JSX, useState } from "react";

export default function HomePage(): JSX.Element {
  const [activeDisciplineId, setActiveDisciplineId] = useState<number | null>(
    null
  );
  // const { presentations, isLoading, isError } = usePresentations();

  return (
    <div className="flex flex-col w-full px-4">
      <div>
        <h3 className="scroll-m-20 text-2xl font-semibold tracking-tight">
          Главная
        </h3>
        <p className="leading-7 text-[var(--muted-foreground)]">
          Здесь представлены все материалы
        </p>
      </div>
      <div className="grid grid-cols-3 gap-4 mt-4">
        {disciplines.map((discipline) => (
          <DisciplineCard
            key={discipline.id}
            discipline={discipline}
            isActive={activeDisciplineId === discipline.id}
            onClick={() =>
              setActiveDisciplineId(
                activeDisciplineId === discipline.id ? null : discipline.id
              )
            }
          />
        ))}
      </div>
    </div>
  );
}
