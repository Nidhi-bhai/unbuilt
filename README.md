# The Unbuilt Index

**What Hacker News said it would pay for.** 11,986 HN comments and posts that say "I'd pay for", "someone should build", "take my money" or "is there a tool that", grouped by what people asked for and ranked by how many *different* people asked.

Live: https://nidhi-bhai.github.io/unbuilt/

Pick one and build it. They already asked.

## Data
- `docs/unbuilt-requests.csv`: every request sentence (HN id, author, date, phrase, text, story, link)
- `docs/data.json`: themes, requests, and the "take my money" post leaderboard
- `data/raw.jsonl.gz`: raw HN Algolia hits
- Hugging Face: https://huggingface.co/datasets/Nidhibhai/unbuilt-index

## Method
1. `harvest.py`: phrase queries for 20 buyer phrases against the public HN Algolia API, 2007 to today, sliced by date.
2. `process.py`: keep sentences that hold a buyer phrase and name a concrete thing (drops "I'd pay for this"). Top-level "I'd pay for this" replies count toward the post's "take my money" score.
3. `cluster.py`: software/product requests embedded with BAAI/bge-small-en-v1.5, grouped by cosine similarity (average linkage, threshold 0.22). A theme needs 3+ different accounts.
4. `build.py`, `og.py`: site data and share image. `ops/refresh.yml` is a ready GitHub Action for a daily refresh (copy to `.github/workflows/` to enable).

Limits: phrase matching leaves some noise. A comment is words, not a purchase.

Not affiliated with Hacker News or Y Combinator. Comment text belongs to its authors; each row links to the original.

Built by [@RealNidhibhai](https://x.com/RealNidhibhai). Same idea, live, on HN: [Buyer Signal Finder](https://nidhi-bhai.github.io/buyer-signal-finder/). On X: [Buyer Hunt](https://nidhi-bhai.github.io/buyer-hunt/).
