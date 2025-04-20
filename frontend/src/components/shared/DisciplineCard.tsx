import React from "react";
import { Discipline } from "@/types/presentations.type";
import Link from "next/link";
import { Star } from "lucide-react";

interface DisciplineCardProps {
  discipline: Discipline;
  isActive?: boolean;
  onClick?: () => void;
}

export default function DisciplineCard({
  discipline,
  isActive,
  onClick,
}: DisciplineCardProps) {
  return (
    <Link
      href={`/disciplines/${discipline.id}`}
      className={`bg-[var(--muted)] rounded-lg shadow-md p-4 transition-all duration-300 select-none
${isActive ? "border-2 border-primary" : ""}`}
      onClick={onClick}
    >
      <h4 className="text-2xl font-semibold mb-2">{discipline.title}</h4>
      <p className="text-sm text-gray-500">Лектор: {discipline.lecturer}</p>
      <div className="flex items-center mt-2 gap-2">
        <Star size={16} />
        {discipline.rating}
      </div>
    </Link>
  );
}
