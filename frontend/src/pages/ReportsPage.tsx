import { useCampaignId } from "../hooks/useCampaignId";

export function ReportsPage() {
  const { campaignId } = useCampaignId();

  if (!campaignId) return <p>Sélectionnez une campagne.</p>;

  const jsonUrl = `/api/v1/campaigns/${campaignId}/report?format=json`;
  const htmlUrl = `/api/v1/campaigns/${campaignId}/report?format=html`;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Rapports</h1>
      <p className="text-sm">Exports avec métadonnées de reproduction (version, moteur, mode).</p>
      <div className="flex gap-3">
        <a className="rounded border px-4 py-2 text-sm" href={jsonUrl} download>
          Télécharger JSON
        </a>
        <a className="rounded border px-4 py-2 text-sm" href={htmlUrl} target="_blank" rel="noreferrer">
          Ouvrir HTML imprimable
        </a>
      </div>
    </div>
  );
}
