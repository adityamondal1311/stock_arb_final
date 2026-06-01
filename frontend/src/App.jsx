import LivePricesTable from "./components/LivePricesTable";
import ArbitragePanel from "./components/ArbitragePanel";
import { useWsStatus } from "./useWsStatus";

const STATUS_CONFIG = {
  live:         { dot: "bg-emerald-400 animate-pulse2", text: "text-emerald-400", label: "LIVE" },
  connecting:   { dot: "bg-yellow-400 animate-pulse2", text: "text-yellow-400",  label: "CONNECTING" },
  reconnecting: { dot: "bg-yellow-400 animate-pulse2", text: "text-yellow-400",  label: "RECONNECTING" },
  disconnected: { dot: "bg-red-500",                   text: "text-red-400",     label: "DISCONNECTED" },
};

function StatusBadge() {
  const status = useWsStatus();
  const cfg = STATUS_CONFIG[status] ?? STATUS_CONFIG.disconnected;
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-800 border border-border">
      <span className={`h-2 w-2 rounded-full ${cfg.dot}`} />
      <span className={`text-xs font-semibold tracking-widest ${cfg.text}`}>{cfg.label}</span>
    </div>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-surface">
      {/* Header */}
      <header className="border-b border-border bg-card/60 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-7 w-7 rounded-lg bg-blue-600 flex items-center justify-center">
              <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <span className="text-white font-semibold text-lg tracking-tight">ArbScreen</span>
            <span className="hidden sm:block text-gray-600 text-sm">NSE · BSE Arbitrage</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden md:block text-xs text-gray-600">⚠ Prices delayed ~15 min (yfinance)</span>
            <StatusBadge />
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-7xl mx-auto px-6 py-8 space-y-6">
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <LivePricesTable />
          <ArbitragePanel />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border mt-8 py-4 text-center text-xs text-gray-700">
        ArbScreen — NSE/BSE arbitrage screener · Data via yfinance
      </footer>
    </div>
  );
}
