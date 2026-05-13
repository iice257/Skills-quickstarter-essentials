import { ArrowRight } from "lucide-react";
import { needCards } from "../data";

export function NeedCards() {
  return (
    <section id="skills" className="paths-section">
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
          const Icon = card.icon;
          const external = card.href.startsWith("http");

          return (
            <a
              key={card.title}
              className="path-card"
              href={card.href}
              target={external ? "_blank" : undefined}
              rel={external ? "noreferrer" : undefined}
            >
              <span className="card-accent" aria-hidden="true" />
              <span className="card-num">{String(index + 1).padStart(2, "0")}</span>
              <span className="icon-chip">
                <Icon aria-hidden="true" />
              </span>
              <strong>{card.title}</strong>
              <p>{card.text}</p>
              <span className="card-action">
                {card.action}
                <ArrowRight aria-hidden="true" />
              </span>
            </a>
          );
        })}
      </div>
    </section>
  );
}
