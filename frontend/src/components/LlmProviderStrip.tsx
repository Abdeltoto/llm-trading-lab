const providers = [
  { id: "demo", name: "Démo", status: "Actif", desc: "Zéro clé" },
  { id: "openai", name: "OpenAI", status: "Config", desc: "Adaptateur" },
  { id: "anthropic", name: "Anthropic", status: "Config", desc: "Adaptateur" },
  { id: "google", name: "Google", status: "Config", desc: "Gemini" },
  { id: "ollama", name: "Ollama", status: "Config", desc: "Local" },
] as const;

export function LlmProviderStrip({ compact = false }: { compact?: boolean }) {
  return (
    <section
      className={`rounded-xl border border-zinc-200/80 bg-gradient-to-b from-zinc-50 to-white p-4 dark:border-zinc-800 dark:from-zinc-900 dark:to-zinc-950 ${
        compact ? "" : "shadow-sm"
      }`}
      aria-label="Fournisseurs LLM"
    >
      <div className="mb-3 flex items-baseline justify-between gap-2">
        <h2 className="text-sm font-semibold tracking-wide text-zinc-700 dark:text-zinc-200">
          Fournisseurs LLM
        </h2>
        <span className="text-[11px] uppercase tracking-wider text-zinc-500">équité expérimentale</span>
      </div>
      <ul className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-5">
        {providers.map((p) => (
          <li
            key={p.id}
            className="group flex flex-col items-center rounded-lg border border-transparent px-2 py-3 text-center transition hover:border-amber-200/80 hover:bg-amber-50/50 dark:hover:border-amber-900/50 dark:hover:bg-amber-950/20"
          >
            <img
              src={`/icons/llm/${p.id}.svg`}
              alt=""
              width={36}
              height={36}
              className="mb-2 opacity-90 transition group-hover:scale-105"
            />
            <span className="text-xs font-medium">{p.name}</span>
            <span
              className={`mt-0.5 text-[10px] ${
                p.status === "Actif" ? "text-emerald-600" : "text-zinc-500"
              }`}
            >
              {p.status}
            </span>
            {!compact && <span className="mt-1 text-[10px] text-zinc-400">{p.desc}</span>}
          </li>
        ))}
      </ul>
    </section>
  );
}
