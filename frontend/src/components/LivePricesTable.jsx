import { useState, useEffect, useRef } from "react";
import { subscribe } from "../websocket";

const STOCKS = [
  ["RELIANCE.NS", "RELIANCE.BO", "Reliance"],
  ["TCS.NS",      "TCS.BO",      "TCS"],
  ["HDFCBANK.NS", "HDFCBANK.BO", "HDFC Bank"],
];

function fmt(v) {
  if (v == null) return <span className="text-gray-600">—</span>;
  return "₹" + Number(v).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function PriceCell({ value, prev }) {
  const flash = useRef(null);
  const [dir, setDir] = useState(null);

  useEffect(() => {
    if (prev == null || value == null || prev === value) return;
    const d = value > prev ? "up" : "down";
    setDir(d);
    clearTimeout(flash.current);
    flash.current = setTimeout(() => setDir(null), 800);
  }, [value]);

  const color =
    dir === "up"   ? "text-emerald-400" :
    dir === "down" ? "text-red-400"     :
    "text-gray-100";

  return (
    <td className={`td text-right font-mono transition-colors duration-300 ${color}`}>
      {fmt(value)}
    </td>
  );
}

function SpreadBadge({ nse, bse }) {
  if (nse == null || bse == null) return <td className="td text-right text-gray-600">—</td>;
  const diff = Math.abs(Number(nse) - Number(bse));
  const color = diff >= 1 ? "text-amber-400 font-semibold" : "text-gray-500";
  return (
    <td className={`td text-right font-mono ${color}`}>
      {diff >= 1 && <span className="mr-1 text-amber-500">▲</span>}
      ₹{diff.toFixed(2)}
    </td>
  );
}

export default function LivePricesTable() {
  const [prices, setPrices]     = useState({});
  const [prevPrices, setPrev]   = useState({});
  const [updatedAt, setUpdatedAt] = useState(null);

  useEffect(() => {
    subscribe((data) => {
      setPrev((p) => ({ ...p, ...prices }));
      setPrices(data);
      setUpdatedAt(new Date());
    });
  }, []);

  return (
    <div className="card flex flex-col">
      {/* Card header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-border">
        <div>
          <h2 className="text-sm font-semibold text-white">Live Prices</h2>
          <p className="text-xs text-gray-600 mt-0.5">NSE vs BSE — last close</p>
        </div>
        {updatedAt ? (
          <span className="text-xs text-gray-600">
            Updated {updatedAt.toLocaleTimeString()}
          </span>
        ) : (
          <span className="flex items-center gap-1.5 text-xs text-yellow-500">
            <span className="h-1.5 w-1.5 rounded-full bg-yellow-400 animate-pulse" />
            Waiting for first fetch…
          </span>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border">
              <th className="th">Stock</th>
              <th className="th text-right">NSE</th>
              <th className="th text-right">BSE</th>
              <th className="th text-right">Spread</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {STOCKS.map(([nse, bse, name]) => (
              <tr key={nse} className="hover:bg-white/[0.02] transition-colors">
                <td className="td">
                  <div className="font-medium text-white">{name}</div>
                  <div className="text-xs text-gray-600 mt-0.5">{nse.replace(".NS", "")}</div>
                </td>
                <PriceCell value={prices[nse]}  prev={prevPrices[nse]} />
                <PriceCell value={prices[bse]}  prev={prevPrices[bse]} />
                <SpreadBadge nse={prices[nse]} bse={prices[bse]} />
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Empty state */}
      {Object.keys(prices).length === 0 && (
        <div className="flex flex-col items-center justify-center py-12 text-gray-600">
          <svg className="h-8 w-8 mb-3 animate-spin text-gray-700" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
          </svg>
          <p className="text-sm">Fetching prices from yfinance…</p>
        </div>
      )}
    </div>
  );
}
