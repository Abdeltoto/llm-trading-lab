import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { useCampaignId } from "../hooks/useCampaignId";
import { ExplainerGallery } from "../components/ExplainerGallery";
import { LlmProviderStrip } from "../components/LlmProviderStrip";

export function OverviewPage() {
  const { campaignId, loading: cidLoading } = useCampaignId();
  const [arena, setArena] = useState<any>(null);
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    api("/api/v1/health").then(setHealth);
  }, []);

  useEffect(() => {
    if (!campaignId) return;
    api(`/api/v1/campaigns/${campaignId}/arena`).then(setArena);
  }, [campaignId]);

  if (cidLoading) return <p className="text-sm text-zinc-500">Chargement de la campagne…</p>;

  const leader = arena?.competitors?.[0];
  const mode = health?.trading_mode ?? "—";

  return (
    <div className="space-y-10">
      <header className="space-y-3 border-b border-zinc-200 pb-8 dark:border-zinc-800">
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-amber-700 dark:text-amber-400">
          Laboratoire · v{health?.version ?? "0.1"}
        </p>
        <h1 className="text-3xl font-semibold tracking-tight md:text-4xl">Vue d&apos;ensemble</h1>
        <p className="max-w-2xl text-base leading-relaxed text-zinc-600 dark:text-zinc-400">
          Comparez des modèles sous protocole identique — données, risque, instant de décision et budget IA.
          Aucun ordre réel. Mode actuel : <span className="font-mono text-zinc-800 dark:text-zinc-200">{mode}</span>
          .
        </p>
      </header>

      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard title="Campagne" value={campaignId?.slice(0, 8) ?? "—"} hint="identifiant court" />
        <MetricCard title="Concurrents" value={arena?.competitors?.length ?? 0} hint="portefeuilles isolés" />
        <MetricCard
          title="Moteur"
          value={arena?.engine ?? health?.execution_engine ?? "—"}
          hint="exécution simulée"
        />
      </div>

      <LlmProviderStrip />

      <ExplainerGallery />

      <section className="grid gap-6 md:grid-cols-2">
        <div className="rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
          <h2 className="text-sm font-semibold">Prochaine action</h2>
          <p className="mt-2 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
            Lancez un pas de simulation, puis ouvrez l&apos;arène pour comparer rendement et coût IA.
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            <Link
              to="/campagnes"
              className="rounded-md bg-zinc-900 px-3 py-2 text-xs font-medium text-white dark:bg-zinc-100 dark:text-zinc-900"
            >
              Campagnes
            </Link>
            <Link to="/arene" className="rounded-md border px-3 py-2 text-xs font-medium">
              Arène
            </Link>
            <Link to="/rapports" className="rounded-md border px-3 py-2 text-xs font-medium">
              Rapports
            </Link>
          </div>
        </div>
        <div className="rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
          <h2 className="text-sm font-semibold">État système</h2>
          <dl className="mt-3 space-y-2 text-sm">
            <Row label="API" value={health?.status ?? "—"} />
            <Row label="Worker" value="heartbeat (voir logs)" />
            {leader && (
              <Row
                label="Exemple concurrent"
                value={`${leader.name} · ${leader.cash.toLocaleString("fr-FR", {
                  style: "currency",
                  currency: "USD",
                })} cash`}
              />
            )}
          </dl>
        </div>
      </section>
    </div>
  );
}

function MetricCard({ title, value, hint }: { title: string; value: string | number; hint: string }) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white/80 p-4 backdrop-blur dark:border-zinc-800 dark:bg-zinc-900/80">
      <div className="text-[11px] font-medium uppercase tracking-wider text-zinc-500">{title}</div>
      <div className="mt-2 text-2xl font-semibold tabular-nums tracking-tight">{value}</div>
      <div className="mt-1 text-xs text-zinc-400">{hint}</div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between gap-4 border-b border-zinc-100 pb-2 last:border-0 dark:border-zinc-800">
      <dt className="text-zinc-500">{label}</dt>
      <dd className="text-right font-medium text-zinc-800 dark:text-zinc-200">{value}</dd>
    </div>
  );
}
