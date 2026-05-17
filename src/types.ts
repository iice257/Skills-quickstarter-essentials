export type SelectionItem = {
  title: string;
  command: string;
};

export type MultiSelectControls = {
  active: boolean;
  selected: Record<string, SelectionItem>;
  toggle: (item: SelectionItem) => void;
};
