import { ArrowRight } from "lucide-react";
import { scenarios } from "../data";

export function ScenarioGrid() {
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
          const Icon = scenario.icon;

          return (
            <a
              key={scenario.name}
              className="scenario-card"
              href={scenario.href}
              target="_blank"
              rel="noreferrer"
            >
              <em>{String(index + 1).padStart(2, "0")}</em>
              <span>
                <Icon aria-hidden="true" />
              </span>
              <strong>{scenario.name}</strong>
              <p>{scenario.description}</p>
            </a>
          );
        })}
      </div>
    </section>
  );
}
