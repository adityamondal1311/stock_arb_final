import { useEffect, useState } from "react";

export default function ArbitragePanel() {
  const [ops, setOps] = useState([]);

  useEffect(() => {
    const timer = setInterval(async () => {
      const data = await fetch("http://localhost:8000/arbitrage/latest").then(r => r.json());
      setOps(data);
    }, 2000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div>
      <h2>Arbitrage Opportunities</h2>
      {ops.map((o) => (
        <div key={o.id}>
          {o.symbol}: NSE={o.nse_price}, BSE={o.bse_price}, Diff={o.difference}
        </div>
      ))}
    </div>
  );
}
