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

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 max-w-xl mx-auto my-12 bg-white dark:bg-slate-900 border border-rose-300 dark:border-rose-800 rounded-2xl shadow-sm text-center">
          <h3 className="text-lg font-bold text-rose-600 mb-2">Something went wrong rendering this view</h3>
          <p className="text-xs text-slate-500 mb-4">{this.state.error?.message || "Unknown rendering exception"}</p>
          <button
            onClick={() => { this.setState({ hasError: false }); window.location.reload(); }}
            className="px-4 py-2 bg-finblue-600 hover:bg-finblue-500 text-white rounded-lg text-xs font-semibold"
          >
            Reload Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

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
          <ErrorBoundary>
            {renderCurrentPage()}
          </ErrorBoundary>
        </main>
      </div>
    </div>
  );
}
