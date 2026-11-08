import { useEffect, useState } from "react";
import { api } from "../api";
import { useCampaignId } from "../hooks/useCampaignId";

export function CampaignsPage() {
  const { campaignId, setCampaignId } = useCampaignId();
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  const reload = () => api<any[]>("/api/v1/campaigns").then(setCampaigns);

  useEffect(() => {
    reload();
  }, []);

  async function createDemo() {
    setBusy(true);
    setMsg("");
    try {
      const c = await api<{ id: string }>("/api/v1/campaigns", {
        method: "POST",
        body: JSON.stringify({ name: "Nouvelle campagne démo", mode: "DEMO" }),
      });
      localStorage.setItem("llm_lab_campaign_id", c.id);
      setCampaignId(c.id);
      await reload();
      setMsg("Campagne créée. Aucun appel LLM payant en mode DEMO.");
    } catch (e: any) {
      setMsg(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function runStep() {
    if (!campaignId) return;
    setBusy(true);
    try {
      await api(`/api/v1/campaigns/${campaignId}/run-step`, { method: "POST", body: "{}" });
      setMsg("Pas de simulation exécuté.");
    } catch (e: any) {
      setMsg(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Campagnes</h1>
      <p className="text-sm text-zinc-600">
        Modèle par défaut : 100 000 USD fictifs / concurrent, 8 semaines prospectives (cible), budget IA 50 USD.
      </p>
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          disabled={busy}
          onClick={createDemo}
          className="rounded bg-zinc-900 px-4 py-2 text-sm text-white disabled:opacity-50"
        >
          Créer campagne DEMO
        </button>
        <button
          type="button"
          disabled={busy || !campaignId}
          onClick={runStep}
          className="rounded border px-4 py-2 text-sm disabled:opacity-50"
        >
          Exécuter un pas (décision + exécution simulée)
        </button>
      </div>
      {msg && <p className="text-sm text-amber-700">{msg}</p>}
      <ul className="divide-y rounded border dark:border-zinc-800">
        {campaigns.map((c) => (
          <li key={c.id} className="flex items-center justify-between px-3 py-2 text-sm">
            <span>
              {c.name} — {c.mode} — {c.execution_engine}
            </span>
            <button
              type="button"
              className="text-blue-600 underline"
              onClick={() => {
                localStorage.setItem("llm_lab_campaign_id", c.id);
                setCampaignId(c.id);
              }}
            >
              {c.id === campaignId ? "Active" : "Sélectionner"}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
