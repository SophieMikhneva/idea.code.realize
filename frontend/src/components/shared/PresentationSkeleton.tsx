"use client";

import { Skeleton } from "@/components/ui/skeleton";

export function PresentationSkeleton({ count = 5 }: { count?: number }) {
  return (
    <ul className="space-y-2">
      {Array(count)
        .fill(0)
        .map((_, index) => (
          <li key={index}>
            <Skeleton className="h-8 w-full" />
          </li>
        ))}
    </ul>
  );
}
