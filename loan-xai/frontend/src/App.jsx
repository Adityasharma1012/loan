import React, { useState, useEffect } from "react";
import Banner from "./components/Banner";
import Sidebar from "./components/Sidebar";

// Pages
import LandingPage from "./pages/LandingPage";
import DashboardPage from "./pages/DashboardPage";
import NewApplicationPage from "./pages/NewApplicationPage";
import ResultsPage from "./pages/ResultsPage";
import ExplanationPage from "./pages/ExplanationPage";
import MLComparisonPage from "./pages/MLComparisonPage";
import FairnessPage from "./pages/FairnessPage";
import HistoryPage from "./pages/HistoryPage";
import AuditReportPage from "./pages/AuditReportPage";
import AboutPage from "./pages/AboutPage";

export default function App() {
  const [currentPage, setCurrentPage] = useState("dashboard");
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [latestEvaluation, setLatestEvaluation] = useState(null);
  const [selectedAppId, setSelectedAppId] = useState(null);

  // Sync dark mode class with root <html> element
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  const renderCurrentPage = () => {
    switch (currentPage) {
      case "landing":
        return <LandingPage setCurrentPage={setCurrentPage} />;
      case "dashboard":
        return (
          <DashboardPage
            setCurrentPage={setCurrentPage}
            setSelectedAppId={setSelectedAppId}
          />
        );
      case "new-application":
        return (
          <NewApplicationPage
            setCurrentPage={setCurrentPage}
            setLatestEvaluation={setLatestEvaluation}
            setSelectedAppId={setSelectedAppId}
          />
        );
      case "results":
        return (
          <ResultsPage
            latestEvaluation={latestEvaluation}
            selectedAppId={selectedAppId}
            setCurrentPage={setCurrentPage}
            setSelectedAppId={setSelectedAppId}
          />
        );
      case "explanation":
        return (
          <ExplanationPage
            latestEvaluation={latestEvaluation}
            selectedAppId={selectedAppId}
          />
        );
      case "ml-comparison":
        return <MLComparisonPage />;
      case "fairness":
        return <FairnessPage />;
      case "history":
        return (
          <HistoryPage
            setCurrentPage={setCurrentPage}
            setSelectedAppId={setSelectedAppId}
          />
        );
      case "audit-report":
        return (
          <AuditReportPage
            selectedAppId={selectedAppId}
            setSelectedAppId={setSelectedAppId}
            setCurrentPage={setCurrentPage}
          />
        );
      case "about":
        return <AboutPage />;
      default:
        return <DashboardPage setCurrentPage={setCurrentPage} setSelectedAppId={setSelectedAppId} />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      {/* Persistent Academic Demonstration Banner */}
      <Banner />

      {/* Main Body with Sidebar + Viewport */}
      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          currentPage={currentPage}
          setCurrentPage={setCurrentPage}
          isDarkMode={isDarkMode}
          setIsDarkMode={setIsDarkMode}
        />

        {/* Page Content Viewport */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          {renderCurrentPage()}
        </main>
      </div>
    </div>
  );
}
