"use client";

import { disciplines } from "@/constants/presentation.constant";
import { DocumentsList } from "@/components/shared/DocumentsList";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";

const DisciplinePage = () => {
  const params = useParams();
  const disciplineId = Number(params.disciplineId);
  const discipline = disciplines[disciplineId + 1];

  return (
    <div className="container mx-auto py-8 px-4">
      <header className="flex justify-between items-center">
        <h2 className="mb-6 text-2xl font-bold">{discipline.title}</h2>
        <Button>Создать</Button>
      </header>
      <DocumentsList discipline={discipline} disciplineId={disciplineId} />
    </div>
  );
};

export default DisciplinePage;
