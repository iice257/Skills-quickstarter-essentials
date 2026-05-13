import { Github, Grid2X2, Menu, X } from "lucide-react";
import { useState } from "react";
import { navItems, repoUrl } from "../data";

export function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className="site-header">
      <a className="brand" href="#home" aria-label="Skill Starter Pack home">
        <span className="brand-mark">
          <Grid2X2 aria-hidden="true" />
        </span>
        <span>Skill Starter Pack</span>
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
          <a key={item.href} href={item.href} onClick={() => setOpen(false)}>
            {item.label}
          </a>
        ))}
      </nav>

      <a className="github-button" href={repoUrl} target="_blank" rel="noreferrer">
        <Github aria-hidden="true" />
        <span>Star on GitHub</span>
      </a>
    </header>
  );
}
