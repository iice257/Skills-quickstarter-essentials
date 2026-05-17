import { Github, Menu, X } from "lucide-react";
import { useState } from "react";
import { commands, navItems, repoUrl } from "../data";
import type { SectionKey } from "../data";
import { CopyButton } from "./CopyButton";

type HeaderProps = {
  activeSection: SectionKey;
  onNavigate: (section: SectionKey) => void;
};

export function Header({ activeSection, onNavigate }: HeaderProps) {
  const [open, setOpen] = useState(false);

  function navigate(section: SectionKey) {
    setOpen(false);
    onNavigate(section);
  }

  return (
    <header className="site-header">
      <a
        className="brand"
        href="/"
        aria-label="Skill Starter Pack home"
        onClick={(event) => {
          event.preventDefault();
          navigate("home");
        }}
      >
        <svg className="brand-lockup" viewBox="0 0 240 40" role="img" aria-labelledby="brand-title">
          <title id="brand-title">Skill Starter Pack</title>
          <g className="brand-icon-code">
            <rect x="1.5" y="1.5" width="37" height="37" rx="8.5" />
            <rect x="8" y="8" width="10.5" height="10.5" rx="2.5" />
            <rect x="21.5" y="8" width="10.5" height="10.5" rx="2.5" className="terminal-tile" />
            <rect x="8" y="21.5" width="10.5" height="10.5" rx="2.5" />
            <rect x="21.5" y="21.5" width="10.5" height="10.5" rx="2.5" />
            <path d="M24.3 11.2l4 3.1-4 3.1" />
            <path d="M28.7 17.6h3.2" />
          </g>
          <text x="50" y="25.5">Skill Starter Pack</text>
        </svg>
      </a>

      <button
        className="menu-toggle"
        type="button"
        aria-expanded={open}
        aria-controls="primary-navigation"
        onClick={() => setOpen((value) => !value)}
      >
        {open ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
        <span className="sr-only">Toggle navigation</span>
      </button>

      <nav id="primary-navigation" className={open ? "nav-links open" : "nav-links"}>
        {navItems.map((item) => (
          <a
            key={item.href}
            href={item.href}
            aria-current={activeSection === item.section ? "page" : undefined}
            onClick={(event) => {
              event.preventDefault();
              navigate(item.section);
            }}
          >
            {item.label}
          </a>
        ))}
      </nav>

      <div className="nav-actions">
        <CopyButton
          className="nav-copy-button"
          value={commands[0].command}
          label="Quick Start"
          successLabel="Copied"
        />
        <a className="github-button" href={repoUrl} target="_blank" rel="noreferrer">
          <Github aria-hidden="true" />
          <span>Star on GitHub</span>
        </a>
      </div>
    </header>
  );
}
