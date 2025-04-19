"use client";

import { JSX } from "react";
import ModeToggle from "./ModeToggle";
import UserProfileMenu from "./UserProfileMenu";
import Link from "next/link";
import { ROUTES } from "@/constants/route.constant";
import { Search } from "./Search";

const Header = (): JSX.Element => {
  return (
    <header className="flex border-b-1 border-[var(--border)] items-center justify-between gap-4 p-4 bg-[var(--background)] sticky top-0">
      <Link
        href={ROUTES.home}
        className="scroll-m-20 text-xl font-semibold tracking-tight"
      >
        Хранилище
      </Link>
      <Search />
      <div className="flex items-center justify-center gap-2">
        <ModeToggle />
        <UserProfileMenu user={{ name: "GiRRaFFee" }} />
      </div>
    </header>
  );
};

export default Header;
