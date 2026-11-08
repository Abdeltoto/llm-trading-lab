import { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";
import { api } from "../api";
import { useCampaignId } from "../hooks/useCampaignId";
import { LlmProviderStrip } from "../components/LlmProviderStrip";

export function ArenaPage() {
  const { campaignId } = useCampaignId();
  const [arena, setArena] = useState<any>(null);
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!campaignId) return;
    api(`/api/v1/campaigns/${campaignId}/arena`).then(setArena);
  }, [campaignId]);

  useEffect(() => {
    if (!chartRef.current || !arena?.competitors?.length) return;
    const chart = createChart(chartRef.current, { height: 360, layout: { textColor: "#71717a" } });
    const colors = ["#2563eb", "#16a34a", "#dc2626"];
    arena.competitors.forEach((c: any, i: number) => {
      const series = chart.addLineSeries({ color: colors[i % colors.length], title: c.name });
      series.setData(
        c.equity_curve.map((p: any) => ({ time: p.t.slice(0, 10), value: p.equity }))
      );
    });
    chart.timeScale().fitContent();
    return () => chart.remove();
  }, [arena]);

  const ranked = [...(arena?.competitors ?? [])].sort(
    (a, b) => (b.equity_curve.at(-1)?.equity ?? 0) - (a.equity_curve.at(-1)?.equity ?? 0)
  );

  return (
    <div className="space-y-8">
      <header className="space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">Arène LLM</h1>
        <p className="max-w-2xl text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
          Courbes et classement sur le même moteur (<span className="font-mono">{arena?.engine ?? "—"}</span>).
          Coût d&apos;inférence affiché à part du PnL fictif.
        </p>
      </header>
      <LlmProviderStrip compact />
      <div ref={chartRef} className="rounded border border-zinc-200 dark:border-zinc-800" />
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left">
            <th className="py-2">Rang</th>
            <th>Nom</th>
            <th>Modèle</th>
            <th>Équité finale (fictif)</th>
            <th>Coût IA</th>
          </tr>
        </thead>
        <tbody>
          {ranked.map((c: any, idx: number) => (
            <tr key={c.id} className="border-b border-zinc-100 dark:border-zinc-800">
              <td className="py-2">{idx + 1}</td>
              <td>{c.name}</td>
              <td>
                {c.provider}/{c.model_id}
              </td>
              <td>{c.equity_curve.at(-1)?.equity?.toLocaleString("fr-FR") ?? "—"}</td>
              <td>${c.ai_cost_usd.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
