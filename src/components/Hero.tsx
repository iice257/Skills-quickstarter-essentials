import { ArrowRight, Check, Copy, Play } from "lucide-react";
import { useState } from "react";
import { commands, trustItems } from "../data";
import type { SectionKey } from "../data";

type HeroProps = {
  onNavigate?: (section: SectionKey) => void;
};

export function Hero({ onNavigate }: HeroProps) {
  const [copied, setCopied] = useState(false);
  const mainCommand = commands[0].command;

  function fallbackCopy() {
    const textArea = document.createElement("textarea");
    textArea.value = mainCommand;
    textArea.setAttribute("readonly", "");
    textArea.style.position = "fixed";
    textArea.style.left = "-9999px";
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);
  }

  async function copyQuickStart() {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(mainCommand);
      } else {
        fallbackCopy();
      }
    } catch {
      fallbackCopy();
    }

    setCopied(true);
    window.setTimeout(() => setCopied(false), 2600);
  }

  return (
    <section id="home" className="hero-shell">
      <div className="hero-inner">
        <div className="hero-copy fade-up">
          <span className="eyebrow">AI agent / harness essentials</span>
          <h1>
            Everything
            <br />
            your <mark>AI agent</mark>
            <br />
            needs.
            <br />
            <span>All in one place.</span>
          </h1>
          <p>
            Curated skills, scenario bundles, provider packs, and category paths for Codex and other
            agentic IDEs. Install only what you need.
          </p>

          <div className="hero-actions">
            <a
              className="btn-primary"
              href="/scenarios"
              onClick={(event) => {
                if (!onNavigate) return;
                event.preventDefault();
                onNavigate("scenarios");
              }}
            >
              Explore Scenarios
              <ArrowRight aria-hidden="true" />
            </a>
            <button
              className="btn-secondary hero-copy-command"
              type="button"
              onClick={copyQuickStart}
              aria-live="polite"
            >
              Quick Start
              <Copy aria-hidden="true" />
              {copied ? (
                <span className="copy-tooltip">Command copied. Paste to agent to get started.</span>
              ) : null}
            </button>
            <a
              className="btn-secondary"
              href="/categories"
              onClick={(event) => {
                if (!onNavigate) return;
                event.preventDefault();
                onNavigate("categories");
              }}
            >
              Categories
              <Play aria-hidden="true" />
            </a>
          </div>

          <div className="trust-row" aria-label="Trust signals">
            {trustItems.map((item) => (
              <span key={item}>
                <i>
                  <Check aria-hidden="true" />
                </i>
                {item}
              </span>
            ))}
          </div>
        </div>

        <div className="hero-visual fade-up">
          <div className="terminal-frame">
            <div className="frame-dots" aria-hidden="true">
              <span />
              <span />
              <span />
            </div>
            <span className="frame-title">terminal - skill-starter-pack</span>
            <div className="terminal-body">
              <p>
                <span className="t-cmd">$skill-starter install README.md</span>
              </p>
              <div className="t-output">
                <span className="t-info">? Choose a setup path</span>
                <span className="t-success">&gt; Scenarios / use-case bundles</span>
                <span>  Categories / install paths</span>
                <span>  Favourites / capped shortlist</span>
                <span>  Providers / OpenAI, Claude, Gemini, Cursor</span>
              </div>
              <p>
                <span className="t-cmd">$skill-starter install categories/web-development-setup</span>
              </p>
              <div className="t-output">
                <span className="t-success">ok Fetched scenario bundle</span>
                <span className="t-success">ok Installed matching skill paths</span>
                <span className="t-success">ok Ready after Codex restart</span>
              </div>
              <p>
                <span className="t-comment"># Works with your provider of choice</span>
              </p>
              <div className="provider-chips">
                {["OpenAI", "Claude", "Gemini", "Cursor"].map((provider) => (
                  <span className="chip" key={provider}>
                    <i />
                    {provider}
                  </span>
                ))}
              </div>
              <p>
                <span className="t-cmd">$skill-starter </span>
                <span className="t-cursor" aria-hidden="true" />
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

