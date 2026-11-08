import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { OverviewPage } from "./pages/OverviewPage";
import { ArenaPage } from "./pages/ArenaPage";
import { CampaignsPage } from "./pages/CampaignsPage";
import { PortfolioPage } from "./pages/PortfolioPage";
import { DecisionsPage } from "./pages/DecisionsPage";
import { OrdersPage } from "./pages/OrdersPage";
import { BacktestsPage } from "./pages/BacktestsPage";
import { DataPage } from "./pages/DataPage";
import { ReportsPage } from "./pages/ReportsPage";
import { SettingsPage } from "./pages/SettingsPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<OverviewPage />} />
        <Route path="/arene" element={<ArenaPage />} />
        <Route path="/campagnes" element={<CampaignsPage />} />
        <Route path="/portefeuille" element={<PortfolioPage />} />
        <Route path="/decisions" element={<DecisionsPage />} />
        <Route path="/ordres" element={<OrdersPage />} />
        <Route path="/backtests" element={<BacktestsPage />} />
        <Route path="/donnees" element={<DataPage />} />
        <Route path="/rapports" element={<ReportsPage />} />
        <Route path="/parametres" element={<SettingsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
