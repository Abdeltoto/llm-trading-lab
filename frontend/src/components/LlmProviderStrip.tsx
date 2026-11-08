const providers = [
  { id: "demo", name: "Démo", status: "Actif", desc: "Déterministe · zéro clé" },
  { id: "openai", name: "OpenAI", status: "Config", desc: "GPT · adaptateur" },
  { id: "anthropic", name: "Anthropic", status: "Config", desc: "Claude · adaptateur" },
  { id: "google", name: "Gemini", status: "Config", desc: "Google · adaptateur" },
  { id: "ollama", name: "Ollama", status: "Config", desc: "Modèles locaux" },
] as const;

export function LlmProviderStrip({ compact = false }: { compact?: boolean }) {
  return (
    <section
      className={`rounded-xl border border-zinc-200/80 bg-gradient-to-b from-zinc-50 to-white p-4 dark:border-zinc-800 dark:from-zinc-900 dark:to-zinc-950 ${
        compact ? "" : "shadow-sm"
      }`}
      aria-label="Fournisseurs LLM"
    >
      <div className="mb-4 flex items-baseline justify-between gap-2">
        <h2 className="text-sm font-semibold tracking-wide text-zinc-700 dark:text-zinc-200">
          Fournisseurs LLM
        </h2>
        <span className="text-[11px] uppercase tracking-wider text-zinc-500">équité expérimentale</span>
      </div>
      <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
        {providers.map((p) => (
          <li
            key={p.id}
            className="group flex flex-col items-center rounded-xl border border-zinc-100 bg-white px-2 py-4 text-center shadow-sm transition hover:border-amber-200/90 hover:shadow-md dark:border-zinc-800 dark:bg-zinc-900/80 dark:hover:border-amber-900/60"
          >
            <div className="mb-2 flex h-11 w-11 items-center justify-center rounded-lg bg-white ring-1 ring-zinc-100 dark:bg-zinc-950 dark:ring-zinc-800">
              <img
                src={`/icons/llm/${p.id}.svg`}
                alt=""
                width={28}
                height={28}
                className="h-7 w-7 object-contain transition group-hover:scale-105"
              />
            </div>
            <span className="text-xs font-semibold tracking-tight">{p.name}</span>
            <span
              className={`mt-1 text-[10px] font-medium ${
                p.status === "Actif" ? "text-emerald-600" : "text-zinc-500"
              }`}
            >
              {p.status}
            </span>
            {!compact && <span className="mt-1.5 text-[10px] leading-snug text-zinc-400">{p.desc}</span>}
          </li>
        ))}
      </ul>
    </section>
  );
}
