import { useEffect, useState } from "react";
import { api } from "../api";
import { useCampaignId } from "../hooks/useCampaignId";

export function OrdersPage() {
  const { campaignId } = useCampaignId();
  const [rows, setRows] = useState<any[]>([]);

  useEffect(() => {
    if (!campaignId) return;
    api<any[]>(`/api/v1/campaigns/${campaignId}/orders`).then(setRows);
  }, [campaignId]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Ordres</h1>
      <p className="text-sm text-zinc-600">Exécution simulée — hypothèse : {rows[0]?.assumptions_label ?? "estimation"}.</p>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left">
            <th>Symbole</th>
            <th>Côté</th>
            <th>Qté</th>
            <th>Statut</th>
            <th>Date exéc.</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((o) => (
            <tr key={o.id} className="border-b">
              <td>{o.symbol}</td>
              <td>{o.side}</td>
              <td>{o.quantity}</td>
              <td>{o.status}</td>
              <td>{o.execution_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
