import { Link, useLocation } from "react-router-dom";
import { ReactNode, useEffect, useState } from "react";
import { api } from "../api";

const links = [
  ["Vue d'ensemble", "/"],
  ["Arène", "/arene"],
  ["Campagnes", "/campagnes"],
  ["Portefeuille", "/portefeuille"],
  ["Décisions", "/decisions"],
  ["Ordres", "/ordres"],
  ["Backtests", "/backtests"],
  ["Données", "/donnees"],
  ["Rapports", "/rapports"],
  ["Paramètres", "/parametres"],
];

export function Layout({ children }: { children: ReactNode }) {
  const loc = useLocation();
  const [mode, setMode] = useState("DEMO");

  useEffect(() => {
    api<{ trading_mode: string }>("/api/v1/health")
      .then((h) => setMode(h.trading_mode))
      .catch(() => setMode("hors ligne"));
  }, []);

  return (
    <div className="min-h-screen text-zinc-900 dark:text-zinc-100">
      <header className="sticky top-0 z-50 border-b border-amber-700 bg-amber-600 text-white">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-2 px-4 py-2 text-sm font-semibold">
          <span>SIMULATION — ARGENT FICTIF</span>
          <span>Mode : {mode}</span>
        </div>
      </header>
      <nav className="border-b border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
        <ul className="mx-auto flex max-w-7xl flex-wrap gap-1 px-2 py-2 text-sm">
          {links.map(([label, href]) => (
            <li key={href}>
              <Link
                to={href}
                className={`rounded px-3 py-1.5 ${
                  loc.pathname === href
                    ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900"
                    : "hover:bg-zinc-100 dark:hover:bg-zinc-800"
                }`}
              >
                {label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>
    </div>
  );
}
