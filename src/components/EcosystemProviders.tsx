import { useState } from "react";
import { providers } from "../data";
import { useGridColumns } from "../hooks/useGridColumns";
import type { MultiSelectControls } from "../types";
import { ExpandableInstallCard } from "./ExpandableInstallCard";

type EcosystemProvidersProps = {
  multiSelect: MultiSelectControls;
};

export function EcosystemProviders({ multiSelect }: EcosystemProvidersProps) {
  const [expanded, setExpanded] = useState<string | null>(null);
  const columns = useGridColumns({ desktop: 4, tablet: 2, mobile: 1 });
  const expandedIndex = providers.findIndex((provider) => provider.name === expanded);

  return (
    <section className="ecosystem-section">
      <section id="providers" className="panel providers-panel">
        <div className="panel-heading compact">
          <div>
            <span>Providers</span>
            <h2>Provider packs</h2>
            <p>Provider packs stay separate from favourites and originals.</p>
          </div>
        </div>
        <div className="provider-grid">
          {providers.map((provider, index) => {
            const hiddenSameRow =
              expandedIndex >= 0 &&
              index !== expandedIndex &&
              Math.floor(index / columns) === Math.floor(expandedIndex / columns);

            return (
              <ExpandableInstallCard
                key={provider.name}
                item={{
                  title: provider.name,
                  description: provider.description,
                  command: provider.command,
                  summary: provider.summary,
                  includes: provider.includes,
                  icon: provider.icon,
                  logoSrc: provider.logoSrc,
                  logoAlt: `${provider.name} logo`,
                  action: "Expand pack"
                }}
                index={index}
                hiddenSameRow={hiddenSameRow}
                variant="provider"
                expanded={expanded === provider.name}
                multiSelect={multiSelect}
                onToggle={() =>
                  setExpanded((current) => (current === provider.name ? null : provider.name))
                }
              />
            );
          })}
        </div>
      </section>
    </section>
  );
}
