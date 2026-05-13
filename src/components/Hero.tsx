import { ArrowRight, Check, Play } from "lucide-react";
import { trustItems } from "../data";

export function Hero() {
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
            Curated skills, scenario bundles, provider packs, and MCP configs for Codex and other
            agentic IDEs. Install only what you need.
          </p>

          <div className="hero-actions">
            <a className="btn-primary" href="#scenarios">
              Explore Scenarios
              <ArrowRight aria-hidden="true" />
            </a>
            <a className="btn-secondary" href="#quick-start">
              Quick Start
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
                <span className="t-prompt">$</span>
                <span className="t-cmd"> Skill Installer install the skills listed at README.md</span>
              </p>
              <div className="t-output">
                <span className="t-info">? Choose a setup path</span>
                <span className="t-success">&gt; Scenarios / use-case bundles</span>
                <span>  Skills / installable files</span>
                <span>  MCPs / config references</span>
                <span>  Providers / OpenAI, Claude, Gemini, Cursor</span>
              </div>
              <p>
                <span className="t-prompt">$</span>
                <span className="t-cmd"> install categories/web-development-setup</span>
              </p>
              <div className="t-output">
                <span className="t-success">✓ Fetched scenario bundle</span>
                <span className="t-success">✓ Installed matching skill paths</span>
                <span className="t-success">✓ Ready after Codex restart</span>
              </div>
              <p>
                <span className="t-prompt">$</span>
                <span className="t-comment"> # Works with your provider of choice</span>
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
                <span className="t-prompt">$</span>
                <span className="t-cursor" aria-hidden="true" />
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
