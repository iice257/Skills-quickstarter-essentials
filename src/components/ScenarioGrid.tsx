import { ArrowRight } from "lucide-react";
import { useState } from "react";
import { scenarios } from "../data";
import { useGridColumns } from "../hooks/useGridColumns";
import type { MultiSelectControls } from "../types";
import { ExpandableInstallCard } from "./ExpandableInstallCard";

type ScenarioGridProps = {
  multiSelect: MultiSelectControls;
};

export function ScenarioGrid({ multiSelect }: ScenarioGridProps) {
  const [expanded, setExpanded] = useState<string | null>(null);
  const columns = useGridColumns({ desktop: 3, tablet: 2, mobile: 1 });
  const expandedIndex = scenarios.findIndex((scenario) => scenario.name === expanded);

  return (
    <section id="scenarios" className="panel scenario-panel">
      <div className="panel-heading">
        <div>
          <span>Scenario bundles</span>
          <h2>Popular scenario bundles</h2>
        </div>
        <a href="https://github.com/iice257/Skills-quickstarter/tree/main/categories" target="_blank" rel="noreferrer">
          View all scenarios
          <ArrowRight aria-hidden="true" />
        </a>
      </div>

      <div className="scenario-grid">
        {scenarios.map((scenario, index) => {
          const hiddenSameRow =
            expandedIndex >= 0 &&
            index !== expandedIndex &&
            Math.floor(index / columns) === Math.floor(expandedIndex / columns);

          return (
            <ExpandableInstallCard
              key={scenario.name}
              item={{
                title: scenario.name,
                description: scenario.description,
                command: scenario.command,
                summary: scenario.summary,
                includes: scenario.includes,
                icon: scenario.icon,
                action: "Expand"
              }}
              index={index}
              hiddenSameRow={hiddenSameRow}
              variant="scenario"
              expanded={expanded === scenario.name}
              multiSelect={multiSelect}
              onToggle={() =>
                setExpanded((current) => (current === scenario.name ? null : scenario.name))
              }
            />
          );
        })}
      </div>
    </section>
  );
}
