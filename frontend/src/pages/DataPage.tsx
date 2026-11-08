import { useEffect, useState } from "react";
import { api } from "../api";

export function DataPage() {
  const [meta, setMeta] = useState<any>(null);

  useEffect(() => {
    api("/api/v1/data/universe").then(setMeta).catch(() => setMeta(null));
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Données</h1>
      {meta ? (
        <ul className="text-sm">
          <li>Symboles : {meta.symbols.join(", ")}</li>
          <li>Lignes : {meta.rows}</li>
          <li>Période : {meta.from} → {meta.to}</li>
          <li>Fournisseur DEMO : synthétique reproductible (seed 42)</li>
        </ul>
      ) : (
        <p className="text-sm text-red-600">Jeu démo indisponible — générer via scripts/generate_demo_parquet.py</p>
      )}
    </div>
  );
}
