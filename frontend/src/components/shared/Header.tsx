import { JSX } from "react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import ModeToggle from "./ModeToggle";
import UserProfileMenu from "./UserProfileMenu";

const Header = (): JSX.Element => {
  return (
    <header className="flex border-b-1 border-b-gray-400 items-center justify-between gap-4 p-4">
      <h2 className="scroll-m-20 text-2xl font-semibold tracking-tight">
        Главная
      </h2>
      <div className="flex w-full max-w-sm items-center space-x-2">
        <Input type="email" placeholder="Искать в хранилище" />
        <Button type="submit">Искать</Button>
      </div>
      <section className="flex items-center justify-center gap-2">
        <ModeToggle />
        <UserProfileMenu user={{ name: "GiRRaFFee" }} />
      </section>
    </header>
  );
};

export default Header;
