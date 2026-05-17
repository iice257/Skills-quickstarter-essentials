import { Github } from "lucide-react";
import { githubProfileUrl, repoUrl, xProfileUrl } from "../data";

export function Footer() {
  return (
    <footer className="site-footer">
      <div>
        <strong>CURATED, FOCUSED, AGENT READY</strong>
        <span>(c) ice 2026</span>
      </div>
      <nav aria-label="Footer links">
        <a href={repoUrl} target="_blank" rel="noreferrer">
          Repository
        </a>
        <a href={githubProfileUrl} target="_blank" rel="noreferrer">
          <Github aria-hidden="true" />
          GitHub
        </a>
        <a href={xProfileUrl} target="_blank" rel="noreferrer">
          X
        </a>
      </nav>
    </footer>
  );
}
