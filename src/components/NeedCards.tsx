import { useState } from "react";
import { needCards } from "../data";
import { useGridColumns } from "../hooks/useGridColumns";
import type { MultiSelectControls } from "../types";
import { ExpandableInstallCard } from "./ExpandableInstallCard";

type NeedCardsProps = {
  multiSelect: MultiSelectControls;
};

export function NeedCards({ multiSelect }: NeedCardsProps) {
  const [expanded, setExpanded] = useState<string | null>(null);
  const columns = useGridColumns({ desktop: 5, tablet: 2, mobile: 1 });
  const expandedIndex = needCards.findIndex((card) => card.title === expanded);

  return (
    <section id="categories" className="paths-section">
      <div className="section-header">
        <div>
          <span className="section-eyebrow">Choose a path</span>
          <h2>
            What do you
            <br />
            need today?
          </h2>
        </div>
        <p>Pick the install or config area that matches the setup you want. Mix and match freely.</p>
      </div>
      <div className="need-grid">
        {needCards.map((card, index) => {
          const hiddenSameRow =
            expandedIndex >= 0 &&
            index !== expandedIndex &&
            Math.floor(index / columns) === Math.floor(expandedIndex / columns);

          return (
            <ExpandableInstallCard
              key={card.title}
              item={{
                title: card.title,
                description: card.text,
                command: card.command,
                summary: card.summary,
                includes: card.includes,
                icon: card.icon,
                action: card.action
              }}
              index={index}
              hiddenSameRow={hiddenSameRow}
              variant="path"
              expanded={expanded === card.title}
              multiSelect={multiSelect}
              onToggle={() => setExpanded((current) => (current === card.title ? null : card.title))}
            />
          );
        })}
      </div>
    </section>
  );
}
