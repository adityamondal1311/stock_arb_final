import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function fmt(v) {
  return "₹" + Number(v).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function DiffBadge({ value }) {
  const n = Number(value);
  const color =
    n >= 5  ? "bg-red-500/20 text-red-400 border-red-500/30" :
    n >= 2  ? "bg-amber-500/20 text-amber-400 border-amber-500/30" :
              "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold border ${color}`}>
      {fmt(n)}
    </span>
  );
}

function Direction({ nse, bse }) {
  const diff = Number(nse) - Number(bse);
  if (diff > 0) return <span className="text-xs text-blue-400 font-medium">NSE &gt; BSE</span>;
  if (diff < 0) return <span className="text-xs text-purple-400 font-medium">BSE &gt; NSE</span>;
  return null;
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-14 text-gray-600">
      <svg className="h-10 w-10 mb-3 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      <p className="text-sm font-medium">No opportunities yet</p>
      <p className="text-xs mt-1">Gaps ≥ ₹1 between NSE and BSE will appear here</p>
    </div>
  );
}

export default function ArbitragePanel() {
  const [ops, setOps]         = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);
  const [fetchedAt, setFetchedAt] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch(`${API_URL}/arbitrage/latest`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        setOps(await res.json());
        setError(null);
        setFetchedAt(new Date());
      } catch {
        setError("Unable to reach backend.");
      } finally {
        setLoading(false);
      }
    }
    load();
    const t = setInterval(load, 5000);
    return () => clearInterval(t);
  }, []);

  return (
    <div className="card flex flex-col">
      {/* Card header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-border">
        <div>
          <h2 className="text-sm font-semibold text-white">Arbitrage Opportunities</h2>
          <p className="text-xs text-gray-600 mt-0.5">Gaps ≥ ₹1 · last 20 records</p>
        </div>
        <div className="flex items-center gap-3">
          {ops.length > 0 && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold">
              {ops.length} found
            </span>
          )}
          {fetchedAt && (
            <span className="text-xs text-gray-600">
              {fetchedAt.toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="mx-5 mt-4 px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Loading skeleton */}
      {loading && !error && (
        <div className="space-y-3 p-5">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-10 rounded-lg bg-white/5 animate-pulse" />
          ))}
        </div>
      )}

      {/* Table */}
      {!loading && !error && ops.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="th">Stock</th>
                <th className="th text-right">NSE</th>
                <th className="th text-right">BSE</th>
                <th className="th text-right">Spread</th>
                <th className="th text-right">Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {ops.map((o) => (
                <tr key={o.id} className="hover:bg-white/[0.02] transition-colors">
                  <td className="td">
                    <div className="font-medium text-white">{o.symbol}</div>
                    <Direction nse={o.nse_price} bse={o.bse_price} />
                  </td>
                  <td className="td text-right font-mono text-gray-200">{fmt(o.nse_price)}</td>
                  <td className="td text-right font-mono text-gray-200">{fmt(o.bse_price)}</td>
                  <td className="td text-right">
                    <DiffBadge value={o.difference} />
                  </td>
                  <td className="td text-right text-xs text-gray-600">
                    {new Date(o.timestamp).toLocaleTimeString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && ops.length === 0 && <EmptyState />}
    </div>
  );
}
