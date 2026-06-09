CREATE TABLE IF NOT EXISTS arbitrage (
    id          SERIAL PRIMARY KEY,
    symbol      VARCHAR(20)    NOT NULL,
    nse_price   NUMERIC(12, 4) NOT NULL,
    bse_price   NUMERIC(12, 4) NOT NULL,
    difference  NUMERIC(12, 4) NOT NULL,
    timestamp   TIMESTAMPTZ    NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_arbitrage_timestamp ON arbitrage (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_arbitrage_symbol    ON arbitrage (symbol);

ALTER TABLE arbitrage ENABLE ROW LEVEL SECURITY;

CREATE POLICY allow_public_read ON arbitrage
    FOR SELECT TO anon, authenticated
    USING (true);
