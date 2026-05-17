import { useState } from "react";
import { providers } from "../data";
import { ExpandableInstallCard } from "./ExpandableInstallCard";

export function EcosystemProviders() {
  const [expanded, setExpanded] = useState<string | null>(null);

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
                variant="provider"
                expanded={expanded === provider.name}
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
