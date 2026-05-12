import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
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
            <motion.a
              key={scenario.name}
              className="scenario-card"
              href={scenario.href}
              target="_blank"
              rel="noreferrer"
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.025, duration: 0.35 }}
            >
              <span>
                <Icon aria-hidden="true" />
              </span>
              <strong>{scenario.name}</strong>
              <p>{scenario.description}</p>
            </motion.a>
          );
        })}
      </div>
    </section>
  );
}
