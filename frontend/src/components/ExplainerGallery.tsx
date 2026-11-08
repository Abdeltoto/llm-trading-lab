const slides = [
  {
    src: "/marketing/pipeline-decision.jpg",
    title: "Chaîne de décision",
    caption: "Données point-in-time → contrat JSON → RiskEngine → exécution T+1 simulée.",
  },
  {
    src: "/marketing/arena-explainer.jpg",
    title: "Arène",
    caption: "Courbes et classement sur le même moteur, coût IA visible par concurrent.",
  },
  {
    src: "/marketing/architecture-layers.jpg",
    title: "Couches",
    caption: "Interface, intelligence, contrôle — sans accès direct du LLM au registre.",
  },
] as const;

export function ExplainerGallery() {
  return (
    <section className="space-y-4" aria-labelledby="explainer-heading">
      <div>
        <h2 id="explainer-heading" className="text-lg font-semibold">
          Comment ça fonctionne
        </h2>
        <p className="mt-1 max-w-2xl text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
          Trois vues du protocole expérimental. Illustrations générées pour la documentation — le comportement
          réel est défini par le code et les tests.
        </p>
      </div>
      <div className="grid gap-4 lg:grid-cols-3">
        {slides.map((s) => (
          <figure
            key={s.src}
            className="overflow-hidden rounded-xl border border-zinc-200 dark:border-zinc-800"
          >
            <img src={s.src} alt={s.title} className="h-40 w-full object-cover object-center" loading="lazy" />
            <figcaption className="space-y-1 border-t border-zinc-100 px-3 py-2.5 text-sm dark:border-zinc-800">
              <div className="font-medium">{s.title}</div>
              <p className="text-xs leading-relaxed text-zinc-500">{s.caption}</p>
            </figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
}
