import { useState, useEffect } from "react";
import { subscribe } from "../websocket";

export default function LivePricesTable() {
  const [prices, setPrices] = useState({});

  useEffect(() => {
    subscribe((data) => setPrices(data));
  }, []);

  return (
    <table>
      <thead>
        <tr><th>Symbol</th><th>Price</th></tr>
      </thead>
      <tbody>
        {Object.keys(prices).map((s) => (
          <tr key={s}>
            <td>{s}</td>
            <td>{prices[s]}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
