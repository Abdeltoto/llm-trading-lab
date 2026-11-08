import { useState } from "react";
import { api } from "../api";
import { useCampaignId } from "../hooks/useCampaignId";

export function BacktestsPage() {
  const { campaignId } = useCampaignId();
  const [result, setResult] = useState<any>(null);

  async function launch() {
    if (!campaignId) return;
    const r = await api(`/api/v1/campaigns/${campaignId}/backtest?days=10`, { method: "POST" });
    setResult(r);
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Backtests</h1>
      <p className="text-sm text-amber-800 dark:text-amber-200">
        Exploratoire : risque de contamination par connaissances historiques des LLM — privilégier le suivi prospectif.
      </p>
      <button type="button" onClick={launch} className="rounded bg-zinc-900 px-4 py-2 text-sm text-white">
        Lancer backtest démo (10 jours)
      </button>
      {result && <pre className="rounded bg-zinc-100 p-3 text-xs dark:bg-zinc-900">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
