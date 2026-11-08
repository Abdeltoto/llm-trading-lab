import { useEffect, useState } from "react";
import { api } from "../api";
import { useCampaignId } from "../hooks/useCampaignId";

export function DecisionsPage() {
  const { campaignId } = useCampaignId();
  const [rows, setRows] = useState<any[]>([]);

  useEffect(() => {
    if (!campaignId) return;
    api<any[]>(`/api/v1/campaigns/${campaignId}/decisions`).then(setRows);
  }, [campaignId]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Décisions</h1>
      <table className="w-full text-xs md:text-sm">
        <thead>
          <tr className="border-b text-left">
            <th className="py-2">Instant</th>
            <th>OK</th>
            <th>Hash données</th>
            <th>Résumé</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((d) => (
            <tr key={d.id} className="border-b align-top">
              <td className="py-2">{d.as_of}</td>
              <td>{d.validation_ok ? "oui" : "non"}</td>
              <td className="font-mono">{d.data_snapshot_hash}</td>
              <td>{d.contract?.rationale_summary}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
