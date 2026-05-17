import { useState } from "react";
import { favorites } from "../data";
import { useGridColumns } from "../hooks/useGridColumns";
import type { MultiSelectControls } from "../types";
import { ExpandableInstallCard } from "./ExpandableInstallCard";

type FavoritesSectionProps = {
  multiSelect: MultiSelectControls;
};

export function FavoritesSection({ multiSelect }: FavoritesSectionProps) {
  const [expanded, setExpanded] = useState<number | null>(0);
  const columns = useGridColumns({ desktop: 3, tablet: 2, mobile: 1 });

  return (
    <section id="favorites" className="favorites-section" aria-labelledby="favorites-title">
      <div className="section-header">
        <div>
          <span className="section-eyebrow">Favourites</span>
          <h2 id="favorites-title">
            The current
            <br />
            shortlist.
          </h2>
        </div>
        <p>
          Six high-value skills kept separate from categories and originals, matching the repo's
          <code> favourites/</code> folder.
        </p>
      </div>

      <div className="favorites-grid">
        {favorites.map((favorite, index) => {
          const hiddenSameRow =
            expanded !== null &&
            index !== expanded &&
            Math.floor(index / columns) === Math.floor(expanded / columns);

          return (
            <ExpandableInstallCard
              key={favorite.name}
              item={{
                title: favorite.name,
                description: favorite.description,
                command: favorite.command,
                summary: favorite.summary,
                includes: favorite.includes,
                icon: favorite.icon,
                action: null
              }}
              index={index}
              hiddenSameRow={hiddenSameRow}
              expanded={expanded === index}
              multiSelect={multiSelect}
              onToggle={() => setExpanded((current) => (current === index ? null : index))}
              variant="provider"
            />
          );
        })}
      </div>
    </section>
  );
}
