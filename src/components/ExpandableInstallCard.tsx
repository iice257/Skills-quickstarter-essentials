import { ArrowRight } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import type { KeyboardEvent } from "react";
import { CopyButton } from "./CopyButton";

export type ExpandableInstallItem = {
  title: string;
  description: string;
  command: string;
  summary: string;
  includes: string[];
  icon: LucideIcon;
  action?: string;
  logoSrc?: string;
  logoAlt?: string;
};

type ExpandableInstallCardProps = {
  item: ExpandableInstallItem;
  index: number;
  expanded: boolean;
  onToggle: () => void;
  variant: "path" | "scenario" | "provider";
};

export function ExpandableInstallCard({
  item,
  index,
  expanded,
  onToggle,
  variant
}: ExpandableInstallCardProps) {
  const Icon = item.icon;

  function handleKeyDown(event: KeyboardEvent<HTMLElement>) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onToggle();
    }
  }

  return (
    <article
      className={`expand-card ${variant}-card ${expanded ? "expanded" : ""}`}
      role="button"
      tabIndex={0}
      aria-expanded={expanded}
      onClick={onToggle}
      onKeyDown={handleKeyDown}
    >
      <span className="card-accent" aria-hidden="true" />
      <div className="expand-card-top">
        <em>{String(index + 1).padStart(2, "0")}</em>
        <CopyButton className="mini-copy" value={item.command} label="Copy" successLabel="Copied" />
      </div>
      <span className="icon-chip">
        {item.logoSrc ? (
          <img src={item.logoSrc} alt={item.logoAlt ?? ""} aria-hidden={item.logoAlt ? undefined : true} />
        ) : (
          <Icon aria-hidden="true" />
        )}
      </span>
      <strong>{item.title}</strong>
      <p>{item.description}</p>

      {expanded ? (
        <div className="expanded-detail">
          <div>
            <span>What it does</span>
            <p>{item.summary}</p>
          </div>
          <div>
            <span>Includes</span>
            <ul>
              {item.includes.map((skill) => (
                <li key={skill}>{skill}</li>
              ))}
            </ul>
          </div>
          <div className="expanded-command">
            <code>{item.command}</code>
            <CopyButton value={item.command} label="Copy command" successLabel="Copied" />
          </div>
        </div>
      ) : (
        <span className="card-action">
          {item.action ?? "View details"}
          <ArrowRight aria-hidden="true" />
        </span>
      )}
    </article>
  );
}
