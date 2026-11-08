import { useEffect, useState } from "react";
import { api } from "../api";
import { useCampaignId } from "../hooks/useCampaignId";

export function PortfolioPage() {
  const { campaignId } = useCampaignId();
  const [arena, setArena] = useState<any>(null);

  useEffect(() => {
    if (!campaignId) return;
    api(`/api/v1/campaigns/${campaignId}/arena`).then(setArena);
  }, [campaignId]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Portefeuille</h1>
      <p className="text-sm text-zinc-600">Cash et courbes d'équité par concurrent (données simulées).</p>
      {arena?.competitors?.map((c: any) => (
        <div key={c.id} className="rounded border p-4 dark:border-zinc-800">
          <h2 className="font-semibold">{c.name}</h2>
          <p>Cash : {c.cash.toLocaleString("fr-FR", { style: "currency", currency: "USD" })}</p>
          <p className="text-xs text-zinc-500">Poids cibles/réels : voir onglet Décisions et ordres générés.</p>
        </div>
      ))}
    </div>
  );
}
