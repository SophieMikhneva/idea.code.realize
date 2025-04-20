import { Discipline } from "@/types/presentations.type";
import Link from "next/link";

interface DocumentsListProps {
  discipline: Discipline;
  disciplineId: number;
}

export function DocumentsList({
  discipline,
  disciplineId,
}: DocumentsListProps) {
  return (
    <div className="space-y-6">
      {discipline.documents.presentations.length > 0 && (
        <section className="space-y-3">
          <h3 className="text-lg font-semibold">Презентации</h3>
          <ul className="space-y-2">
            {discipline.documents.presentations.map((presentation) => (
              <li
                key={presentation.id}
                className="rounded-md border p-3 hover:bg-muted/50"
              >
                <Link
                  href={`/disciplines/${disciplineId}/presentations/${presentation.id}`}
                  className="flex items-center justify-between"
                >
                  <div>
                    <h4 className="font-medium">{presentation.title}</h4>
                    <p className="text-sm text-muted-foreground">
                      {presentation.description}
                    </p>
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {presentation.fileType.split("/")[1]}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      {discipline.documents.abstract && (
        <section className="space-y-3">
          <h3 className="text-lg font-semibold">Реферат</h3>
          <div className="rounded-md border p-3 hover:bg-muted/50">
            <a
              href={discipline.documents.abstract}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-primary hover:underline"
            >
              Скачать реферат по {discipline.title}
            </a>
          </div>
        </section>
      )}

      {discipline.documents.cheatSheet && (
        <section className="space-y-3">
          <h3 className="text-lg font-semibold">Шпаргалка</h3>
          <div className="rounded-md border p-3 hover:bg-muted/50">
            <a
              href={discipline.documents.cheatSheet}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-primary hover:underline"
            >
              Скачать шпаргалку по {discipline.title}
            </a>
          </div>
        </section>
      )}
    </div>
  );
}
