import { About } from "./components/About";
import { BottomCta } from "./components/BottomCta";
import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { McpProviders } from "./components/McpProviders";
import { NeedCards } from "./components/NeedCards";
import { QuickStart } from "./components/QuickStart";
import { ScenarioGrid } from "./components/ScenarioGrid";
import { StatsBar } from "./components/StatsBar";

function App() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <StatsBar />
        <NeedCards />
        <section className="details-section" aria-label="Skill Starter Pack details">
          <div className="surface-grid">
            <ScenarioGrid />
            <QuickStart />
          </div>
          <McpProviders />
          <About />
          <BottomCta />
        </section>
      </main>
    </>
  );
}

export default App;
