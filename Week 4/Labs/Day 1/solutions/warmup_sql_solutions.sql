-- Week 4 Day 1 Warmup SQL Solutions (instructor-only)
-- Target: student-created warmup_claims.db, table claims

-- D1: Show only the Connecticut claims.
-- pandas: claims[claims["state"] == "CT"]
SELECT *
FROM claims
WHERE state = 'CT';
-- Expected: 4 rows (C001, C003, C005, C008)

-- D2: Claim id and amount for claims over 2,000.
-- pandas: claims.loc[claims["amount"] > 2000, ["claim_id", "amount"]]
SELECT claim_id, amount
FROM claims
WHERE amount > 2000;
-- Expected: 4 rows (C002 5400, C004 3100, C005 9900, C007 2200). C008's
-- NULL amount fails the comparison, exactly like NaN in pandas.

-- D3: How many claims per state?
-- pandas: claims.groupby("state").size()
SELECT state, COUNT(*) AS claim_count
FROM claims
GROUP BY state;
-- Expected: CT 4, MA 2, NY 2

-- D4: Average claim amount for auto vs home.
-- pandas: claims.groupby("claim_type")["amount"].mean()
SELECT claim_type, AVG(amount) AS avg_amount
FROM claims
GROUP BY claim_type;
-- Expected: auto 1162.5 (NULL skipped: (1200+800+450+2200)/4), home 6133.33
-- Teaching moment: AVG skips NULL exactly like pandas mean() skips NaN.

-- D5: Top three claims by amount, biggest first.
-- pandas: claims.sort_values("amount", ascending=False).head(3)
SELECT *
FROM claims
ORDER BY amount DESC
LIMIT 3;
-- Expected: C005 9900, C002 5400, C004 3100
-- Note: pandas puts NaN last on a descending sort; SQLite treats NULL as
-- smallest, so it also lands last here. Dialects differ on this; some
-- engines need NULLS LAST. One sentence, then move on.

-- D6: Find the claim with no recorded amount.
-- pandas: claims[claims["amount"].isna()]
SELECT *
FROM claims
WHERE amount IS NULL;
-- Expected: 1 row (C008). "= NULL" returns zero rows; let them hit that.
