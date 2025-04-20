import { ReactNode } from "react";

interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyExtractor?: (item: T, index: number) => string | number;
  listClassName?: string;
  itemClassName?: string;
}

const List = <T,>({
  items,
  renderItem,
  keyExtractor,
  listClassName,
  itemClassName,
}: ListProps<T>) => {
  return (
    <ul className={listClassName}>
      {items.map((item, index) => (
        <li
          key={keyExtractor ? keyExtractor(item, index) : index}
          className={itemClassName}
        >
          {renderItem(item, index)}
        </li>
      ))}
    </ul>
  );
};

export default List;
