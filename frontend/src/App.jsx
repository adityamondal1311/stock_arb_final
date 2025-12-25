import LivePricesTable from "./components/LivePricesTable";
import ArbitragePanel from "./components/ArbitragePanel";

function App() {
  return (
    <div>
      <h1>Real-Time Stock Arbitrage Screener</h1>
      <LivePricesTable />
      <ArbitragePanel />
    </div>
  );
}

export default App;
