#!/usr/bin/env bash
# Build a throwaway demo repo for the memclash Pi extension.  Usage: demo/setup.sh <dir>
set -euo pipefail
DIR="${1:?usage: setup.sh <dir>}"
HERE="$(cd "$(dirname "$0")" && pwd)"
rm -rf "$DIR" && mkdir -p "$DIR"/{src,migrations,tests}
cd "$DIR"
cp "$HERE/MEMORY.md" MEMORY.md
cat > package.json <<'J'
{ "name": "demo-shop", "version": "1.0.0",
  "scripts": { "test": "node tests/price.test.js", "lint": "node --check src/price.js" } }
J
cat > src/price.js <<'J'
// Bug: discounts above 100% give a negative price.
export function discounted(price, pct) { return price * (1 - pct / 100); }
J
cat > tests/price.test.js <<'J'
import { discounted } from "../src/price.js";
if (discounted(100, 150) < 0) { console.error("FAIL: negative price"); process.exit(1); }
console.log("ok");
J
echo "CREATE TABLE orders (id INTEGER PRIMARY KEY, total REAL);" > migrations/001_init.sql
echo "PAYMENT_API_KEY=demo-not-a-real-key" > .env
echo "PAYMENT_API_KEY=your-key-here" > .env.example
printf '.env\n.memclash/\n' > .gitignore
git init -q -b main
git add -A && git -c user.name=demo -c user.email=demo@example.com commit -qm "Initial demo project"
git branch release/1.0
# a local stand-in for GitHub, so pushes have somewhere to go
rm -rf "$DIR-origin.git" && git init -q --bare "$DIR-origin.git" && git remote add origin "$DIR-origin.git"
git push -q origin main release/1.0
echo "demo repo ready: $DIR"
