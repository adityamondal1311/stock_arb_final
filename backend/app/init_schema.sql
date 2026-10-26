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

-- Supabase-only roles; skip on plain Postgres and on re-runs
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon')
       AND EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated')
       AND NOT EXISTS (
           SELECT 1 FROM pg_policies
           WHERE tablename = 'arbitrage' AND policyname = 'allow_public_read'
       )
    THEN
        CREATE POLICY allow_public_read ON arbitrage
            FOR SELECT TO anon, authenticated
            USING (true);
    END IF;
END
$$;
