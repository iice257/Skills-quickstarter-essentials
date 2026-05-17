import { useState } from "react";
import { About } from "./components/About";
import { BottomCta } from "./components/BottomCta";
import { EcosystemProviders } from "./components/EcosystemProviders";
import { FavoritesSection } from "./components/FavoritesSection";
import { Footer } from "./components/Footer";
import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { NeedCards } from "./components/NeedCards";
import { QuickStart } from "./components/QuickStart";
import { ScenarioGrid } from "./components/ScenarioGrid";
import { StatsBar } from "./components/StatsBar";
import type { SectionKey } from "./data";

const sectionKeys: SectionKey[] = ["home", "categories", "scenarios", "providers", "favorites", "about"];

function getInitialSection(): SectionKey {
  const hash = window.location.hash.replace("#", "");
  return sectionKeys.includes(hash as SectionKey) ? (hash as SectionKey) : "home";
}

function HeroStage({ onNavigate }: { onNavigate: (section: SectionKey) => void }) {
  return (
    <section className="hero-stage" aria-label="Skill Starter Pack introduction">
      <Hero onNavigate={onNavigate} />
      <StatsBar />
    </section>
  );
}

function DetailsStack() {
  return (
    <section className="details-section" aria-label="Skill Starter Pack details">
      <div className="surface-grid">
        <ScenarioGrid />
        <QuickStart />
      </div>
      <EcosystemProviders />
      <About />
      <FavoritesSection />
      <BottomCta />
    </section>
  );
}

function FocusedSection({ section }: { section: Exclude<SectionKey, "home"> }) {
  return (
    <main className="focused-page">
      {section === "categories" ? <NeedCards /> : null}
      {section === "scenarios" ? (
        <section className="details-section focused-details" aria-label="Popular scenarios">
          <div className="surface-grid single-panel">
            <ScenarioGrid />
          </div>
        </section>
      ) : null}
      {section === "providers" ? (
        <section className="details-section focused-details" aria-label="Provider packs">
          <EcosystemProviders />
        </section>
      ) : null}
      {section === "favorites" ? (
        <section className="details-section focused-details" aria-label="Favourite skills">
          <FavoritesSection />
        </section>
      ) : null}
      {section === "about" ? (
        <section className="details-section focused-details" aria-label="About Skill Starter Pack">
          <About />
          <BottomCta />
        </section>
      ) : null}
    </main>
  );
}

function HomePage({ onNavigate }: { onNavigate: (section: SectionKey) => void }) {
  return (
    <main>
      <HeroStage onNavigate={onNavigate} />
      <NeedCards />
      <DetailsStack />
    </main>
  );
}

function App() {
  const [activeSection, setActiveSection] = useState<SectionKey>(getInitialSection);
  const [viewKey, setViewKey] = useState(0);

  function handleNavigate(section: SectionKey) {
    setActiveSection(section);
    setViewKey((current) => current + 1);
    const nextUrl =
      section === "home"
        ? `${window.location.pathname}${window.location.search}`
        : `${window.location.pathname}${window.location.search}#${section}`;
    window.history.pushState(null, "", nextUrl);
    window.scrollTo({ top: 0, behavior: "auto" });
  }

  return (
    <>
      <Header activeSection={activeSection} onNavigate={handleNavigate} />
      <div key={`${activeSection}-${viewKey}`} className="page-view">
        {activeSection === "home" ? (
          <HomePage onNavigate={handleNavigate} />
        ) : (
          <FocusedSection section={activeSection} />
        )}
      </div>
      <Footer />
    </>
  );
}

export default App;
