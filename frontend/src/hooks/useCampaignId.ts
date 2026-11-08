import { useEffect, useState } from "react";
import { api } from "../api";

const KEY = "llm_lab_campaign_id";

export function useCampaignId() {
  const [campaignId, setCampaignId] = useState<string | null>(
    localStorage.getItem(KEY)
  );
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const stored = localStorage.getItem(KEY);
      if (stored) {
        setCampaignId(stored);
        setLoading(false);
        return;
      }
      const list = await api<Array<{ id: string }>>("/api/v1/campaigns");
      if (list[0]) {
        localStorage.setItem(KEY, list[0].id);
        setCampaignId(list[0].id);
      }
      setLoading(false);
    }
    load().catch(() => setLoading(false));
  }, []);

  return { campaignId, setCampaignId, loading };
}
