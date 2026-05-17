import { useState } from "react";
import { favorites } from "../data";
import { ExpandableInstallCard } from "./ExpandableInstallCard";

export function FavoritesSection() {
  const [expanded, setExpanded] = useState<number | null>(0);

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
        {favorites.map((favorite, index) => (
          <ExpandableInstallCard
            key={favorite.name}
            item={{
              title: favorite.name,
              description: favorite.description,
              command: favorite.command,
              summary: favorite.summary,
              includes: favorite.includes,
              icon: favorite.icon,
              action: "View favourite"
            }}
            index={index}
            expanded={expanded === index}
            onToggle={() => setExpanded((current) => (current === index ? null : index))}
            variant="provider"
          />
        ))}
      </div>
    </section>
  );
}
