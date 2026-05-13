import { stats } from "../data";

export function StatsBar() {
  return (
    <section className="stats-bar" aria-label="Repository stats">
      {stats.map((stat, index) => (
        <div className="stat-group" key={stat.label}>
          {index > 0 ? <span className="stat-divider" aria-hidden="true" /> : null}
          <div className="stat">
            <span className="stat-val">{stat.value}</span>
            <span className="stat-label">{stat.label}</span>
          </div>
        </div>
      ))}
    </section>
  );
}
