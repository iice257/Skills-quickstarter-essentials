import { useEffect, useMemo, useState } from "react";
import { About } from "./components/About";
import { BottomCta } from "./components/BottomCta";
import { EcosystemProviders } from "./components/EcosystemProviders";
import { FavoritesSection } from "./components/FavoritesSection";
import { Footer } from "./components/Footer";
import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { MultiSelectFab } from "./components/MultiSelectFab";
import { NeedCards } from "./components/NeedCards";
import { QuickStart } from "./components/QuickStart";
import { ScenarioGrid } from "./components/ScenarioGrid";
import { StatsBar } from "./components/StatsBar";
import type { SectionKey } from "./data";
import type { SelectionItem } from "./types";

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

type SharedPageProps = {
  multiSelect: {
    active: boolean;
    selected: Record<string, SelectionItem>;
    toggle: (item: SelectionItem) => void;
  };
};

function DetailsStack({ multiSelect }: SharedPageProps) {
  return (
    <section className="details-section" aria-label="Skill Starter Pack details">
      <div className="surface-grid">
        <ScenarioGrid multiSelect={multiSelect} />
        <QuickStart />
      </div>
      <EcosystemProviders multiSelect={multiSelect} />
      <About />
      <FavoritesSection multiSelect={multiSelect} />
      <BottomCta />
    </section>
  );
}

function HomePage({
  multiSelect,
  onNavigate
}: SharedPageProps & { onNavigate: (section: SectionKey) => void }) {
  return (
    <main>
      <HeroStage onNavigate={onNavigate} />
      <NeedCards multiSelect={multiSelect} />
      <DetailsStack multiSelect={multiSelect} />
    </main>
  );
}

function App() {
  const [activeSection, setActiveSection] = useState<SectionKey>(getInitialSection);
  const [multiSelectActive, setMultiSelectActive] = useState(false);
  const [selected, setSelected] = useState<Record<string, SelectionItem>>({});

  const multiSelect = useMemo(
    () => ({
      active: multiSelectActive,
      selected,
      toggle(item: SelectionItem) {
        setSelected((current) => {
          const next = { ...current };
          if (next[item.command]) {
            delete next[item.command];
          } else {
            next[item.command] = item;
          }
          return next;
        });
      }
    }),
    [multiSelectActive, selected]
  );

  useEffect(() => {
    if (!window.location.hash) return;

    const section = getInitialSection();
    window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);
    window.setTimeout(() => {
      const target =
        section === "home" ? document.querySelector(".hero-stage") : document.getElementById(section);
      target?.scrollIntoView({ behavior: "auto", block: "start" });
    }, 0);
  }, []);

  useEffect(() => {
    if (!multiSelectActive) return;

    function handleEscape(event: KeyboardEvent) {
      if (event.key !== "Escape") return;
      setSelected({});
      setMultiSelectActive(false);
    }

    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [multiSelectActive]);

  function handleNavigate(section: SectionKey) {
    setActiveSection(section);
    window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);

    const target =
      section === "home" ? document.querySelector(".hero-stage") : document.getElementById(section);

    if (!target) return;

    target.scrollIntoView({ behavior: "smooth", block: "start" });
    target.classList.remove("section-fade-in");
    window.setTimeout(() => target.classList.add("section-fade-in"), 20);
    window.setTimeout(() => target.classList.remove("section-fade-in"), 780);
  }

  return (
    <>
      <Header activeSection={activeSection} onNavigate={handleNavigate} />
      <HomePage multiSelect={multiSelect} onNavigate={handleNavigate} />
      <MultiSelectFab
        active={multiSelectActive}
        selectedItems={Object.values(selected)}
        onEnable={() => setMultiSelectActive(true)}
        onCancel={() => {
          setSelected({});
          setMultiSelectActive(false);
        }}
        onCopied={() => {
          setSelected({});
          setMultiSelectActive(false);
        }}
      />
      <Footer />
    </>
  );
}

export default App;
