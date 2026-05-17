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
        <svg className="brand-lockup" viewBox="0 0 255 44" role="img" aria-labelledby="brand-title">
          <title id="brand-title">Skill Starter Pack</title>
          <g className="brand-icon-code">
            <rect className="brand-shell" x="1.5" y="1.5" width="41" height="41" rx="10" />
            <rect x="8.8" y="8.8" width="12" height="12" rx="3" />
            <rect x="23.2" y="8.8" width="12" height="12" rx="3" className="terminal-tile" />
            <rect x="8.8" y="23.2" width="12" height="12" rx="3" />
            <rect x="23.2" y="23.2" width="12" height="12" rx="3" />
            <path d="M26.8 12.5l4.4 3.4-4.4 3.4" />
            <path d="M31.8 19.4h3.5" />
          </g>
          <text x="56" y="28">Skill Starter Pack</text>
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
