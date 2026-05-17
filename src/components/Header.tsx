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
        href="#home"
        aria-label="Skill Starter Pack home"
        onClick={(event) => {
          event.preventDefault();
          navigate("home");
        }}
      >
        <img src="/skill-starter-logo.svg" alt="Skill Starter Pack" className="brand-logo" />
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
