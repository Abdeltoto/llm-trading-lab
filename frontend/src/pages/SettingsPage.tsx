import { useEffect, useState } from "react";
import { api } from "../api";

export function SettingsPage() {
  const [health, setHealth] = useState<any>(null);
  const [dark, setDark] = useState(document.documentElement.classList.contains("dark"));

  useEffect(() => {
    api("/api/v1/health").then(setHealth);
  }, []);

  function toggleTheme() {
    document.documentElement.classList.toggle("dark");
    setDark(document.documentElement.classList.contains("dark"));
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Paramètres</h1>
      <button type="button" className="rounded border px-3 py-2 text-sm" onClick={toggleTheme}>
        Thème {dark ? "clair" : "sombre"}
      </button>
      <pre className="rounded bg-zinc-100 p-3 text-xs dark:bg-zinc-900">{JSON.stringify(health, null, 2)}</pre>
      <p className="text-sm text-zinc-600">
        Clés LLM et Alpaca Paper : fichier <code>.env</code> côté serveur uniquement. Aucun passage en réel.
      </p>
    </div>
  );
}
