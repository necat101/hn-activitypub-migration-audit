# HN ActivityPub Migration Audit

Shutdown-readiness protocol check for the claim that **"ActivityPub has Move, so accounts, followers, old posts, media, and identity all migrate together."**

Discussion anchor: [HN item 49112327 — Toot.community is shutting down](https://news.ycombinator.com/item?id=49112327)

> This lab is not an ActivityPub conformance suite. It demonstrates only the structure of its synthetic fixtures and the evidence boundaries between W3C standards and Mastodon implementation behavior.

---

## Shutdown Scenario

A Mastodon administrator is preparing to close an instance (here anchored by toot.community). Users expect that "Move" will carry everything — followers, old posts, media, identity — to a new account in one operation. The lab tests that expectation against two separate evidence classes:

1. **W3C standards** — ActivityPub Recommendation and ActivityStreams 2.0 Vocabulary (especially `Move`).
2. **Mastodon deployment documentation** — current `docs.joinmastodon.org` behavior for account migration.

Keeping those classes separate is the point. Conflating a vocabulary term with a deployment workflow produces the overclaim.

---

## Standards / Implementation Map

| Concept | Where it is defined | What it means |
|---|---|---|
| **ActivityPub** | W3C Recommendation, **23 January 2018** (`https://www.w3.org/TR/activitypub/`) | A decentralized social networking protocol based on ActivityStreams 2.0, defining client-to-server and server-to-server interactions. Does not standardize a one-shot portable migration of followers, old posts, media, follows, blocks, mutes, and bookmarks. |
| **ActivityStreams `Move`** | W3C ActivityStreams 2.0 Vocabulary (`https://www.w3.org/TR/activitystreams-vocabulary/#dfn-move`) | A generic activity meaning **an actor moved an object from an origin to a target** (e.g. "Sally moved a post from List A to List B"). The vocabulary defines the activity type and its `actor`/`object`/`origin`/`target` properties; it does **not** define an account-portability protocol. Do not silently transform this vocabulary definition into a standardized account-migration operation. |
| **Mastodon account migration** | `https://docs.joinmastodon.org/user/moving/` (inspected 2026-09-04) | An **implementation profile** that *uses* `Move` plus additional conventions. Requires an alias relationship (`alsoKnownAs`) from new account → old account before a move is accepted; can move followers when remote software supports `Move`; does **not** move posts/media as part of the profile move; follows/blocks/mutes/bookmarks are handled via separate CSV export/import and archive export, not via `Move`. |
| **`tootctl self-destruct`** | `https://docs.joinmastodon.org/admin/tootctl/#self-destruct` | Mastodon-specific **implementation tooling** for instance shutdown: broadcasts `Delete` activities to known peers to leave little cached material behind. **Not a W3C ActivityPub requirement.** |

**Boundary preserved:** ActivityStreams `Move` exists as a generic vocabulary activity; Mastodon's account-migration workflow is an implementation profile using `Move` plus additional conventions (alias, follower handling, non-migration of posts). That does not mean the W3C ActivityPub Recommendation itself standardizes portable migration of followers, old posts, media, follows, blocks, mutes, and bookmarks as one operation.

---

## HN Claims Checked (from item 49112327)

HN comments are **claims to inspect, not evidence**. Each proposition below was retrieved via the HN API and is identified by commenter and/or comment ID.

### 1. Old posts/media not transferring during a Mastodon move
- **Source:** `dewey` — comment `49113081` — quoting the toot.community shutdown notice: *"Mastodon can move your followers, but it can't transfer your old posts or uploaded media to your new account. If you want to keep a copy, download an archive."* and linking `mastodon/mastodon#12423`.
- **HN proposition:** A Mastodon Move migrates followers but does not carry historical posts/media.
- **Classification:** **supported by inspected Mastodon implementation documentation** — `docs.joinmastodon.org/user/moving/` states: *"Your posts will not be moved, due to technical limitations"* and *"Mastodon currently does not support importing posts or media."*

### 2. "ActivityPub should support migrating posts"
- **Source:** `throwawayk7h` — comment `49113074` — *"Yes, it's called ActivityPub. I'm surprised it doesn't support migrating posts."*
- **HN proposition:** The ActivityPub standard itself should provide portable migration of posts.
- **Classification:** **not established by the inspected sources** — the W3C ActivityPub Recommendation (23 Jan 2018) and ActivityStreams `Move` definition describe a generic move, not a standardized post-migration protocol. No evidence in the inspected W3C documents for this as a standard feature.

### 3. Follower migration versus content migration are distinct
- **Source:** `whywhywhywhy` — comment `49113171` — *"I mean the actual thing that has value IS the posts and there would be less burden on people shutting down these servers if you were not destroying that work by doing so."* (contrasting with `49113081`'s follower-only move).
- **HN proposition:** Follower graph migration and historical post/content migration are separate concerns with different outcomes.
- **Classification:** **supported by inspected Mastodon implementation documentation** — Mastodon's migration moves followers (when remote supports `Move`) but explicitly does not move posts/media; the two are handled via different mechanisms (Move vs archive export).

### 4. FEP 1580 as a proposal to move content
- **Source:** `NoraCodes` — comment `49113056` — *"The protocol is ActivityPub and the feature you suggest is being considered as FEP 1580"* (linking `codeberg.org/fediverse/fep` `fep/1580`).
- **HN proposition:** There is an active proposal (FEP 1580) to standardize content migration for ActivityPub.
- **Classification:** **needs qualification / extension or deployment evidence** — FEP 1580 is a Fediverse Enhancement Proposal (community extension track), not part of the W3C ActivityPub Recommendation. Its existence shows the gap is recognized, but its adoption/standardization status requires inspecting the FEP itself and deployment uptake, beyond the W3C Recommendation and Mastodon docs inspected here.

### 5. Mastodon `tootctl self-destruct` for shutdown
- **Source:** `riffic` — comment `49112943` — *"don't forget to `tootctl self-destruct`"* with link to `docs.joinmastodon.org/admin/tootctl/#self-destruct`, and note: *"Without self-destruct, remote servers may retain cached profiles and posts indefinitely."*
- **HN proposition:** Administrators should run `tootctl self-destruct` to cleanly erase the server from the federation on shutdown.
- **Classification:** **supported by inspected Mastodon implementation documentation** — `docs.joinmastodon.org/admin/tootctl/#self-destruct` documents this as Mastodon CLI tooling that broadcasts `Delete` activities. It is **implementation tooling, not a W3C ActivityPub requirement.**

### 6. Instance shutdown undermines federation
- **Source:** synthesis of `dewey` (`49113081`) — *"basically forces people to stick to the largest instances that are less likely to go away, defeating the purpose of a distributed social network"* — and `0xDEAFBEAD` (`49114041`) on not handing the server over.
- **HN proposition:** Instance shutdown as currently implemented undermines the federation promise because content is lost and users consolidate on large instances.
- **Classification:** **needs qualification / extension or deployment evidence** — this is an architectural/social assessment. The inspected W3C standards do not address instance longevity; Mastodon docs confirm posts don't migrate but do not themselves establish the broader federation-viability claim, which would require deployment data, measurement, or broader policy evidence.

---

## Classification Labels

Every HN proposition above is classified with exactly one of:

- `supported by inspected W3C standard`
- `supported by inspected Mastodon implementation documentation`
- `needs qualification / extension or deployment evidence`
- `not established by the inspected sources`

In particular, Mastodon's `alsoKnownAs` migration rule, post-import limitation, and `tootctl` behavior are **not** classified as W3C requirements merely because Mastodon speaks ActivityPub. Evidence classes are kept separate throughout.

---

## Fixtures

| File | Purpose |
|---|---|
| `fixtures/old_actor.json` | Synthetic old account (`https://old.example/users/alice`). |
| `fixtures/new_actor.json` | Synthetic replacement account; contains `alsoKnownAs: ["https://old.example/users/alice"]` — the alias relationship required by the lab's Mastodon-style migration example. |
| `fixtures/move.json` | Synthetic Mastodon-style `Move` activity (`actor` + `object` + `target` + `origin`). |
| `fixtures/archive.json` | Tiny synthetic historical-post archive (`OrderedCollection` of `Note`s) — **deliberately separate** from the Move fixture. |

## Scripts

- `scripts/check_migration.py` — inspects the fixtures and reports what is present in actor/Move data versus what exists only in the archive.
- `scripts/verify.sh` — asserts the lab's intended distinctions (see below).

## Walkthrough

```bash
# Inspect fixtures
python3 scripts/check_migration.py

# Run the full verification
bash scripts/verify.sh
```

The CI workflow (`.github/workflows/audit.yml`) runs `bash scripts/verify.sh` on Ubuntu using only Python and shell.

---

## What Verification Shows

1. The `Move` fixture identifies an `actor`/`object` and migration `target` but **does not contain** the historical post bodies from `archive.json`.
2. The new synthetic actor contains the `alsoKnownAs` alias relationship required by the lab's Mastodon-style migration example.
3. Follower migration and historical-content migration are represented as **separate concepts** (Move vs archive).
4. **Absence of post bodies from the synthetic Move fixture is not itself proof that no implementation could ever migrate posts** — that stronger claim must come from inspected Mastodon documentation or another authoritative deployment source (here: `docs.joinmastodon.org/user/moving/` confirms Mastodon currently does not move posts/media).
5. Branch/server shutdown administration such as Mastodon-specific `tootctl self-destruct` behavior is **implementation tooling, not a W3C ActivityPub requirement.**

---

## Sources Inspected

- W3C ActivityPub Recommendation — `https://www.w3.org/TR/activitypub/` (W3C Recommendation 23 January 2018)
- W3C ActivityStreams 2.0 Vocabulary, `Move` — `https://www.w3.org/TR/activitystreams-vocabulary/#dfn-move` (generic: actor moved object from origin to target)
- Mastodon documentation — `https://docs.joinmastodon.org/user/moving/` and `https://docs.joinmastodon.org/admin/tootctl/#self-destruct` (retrieved 2026-09-04)
- HN discussion — `https://news.ycombinator.com/item?id=49112327` (comments retrieved via HN API; treated as claims, not evidence)

## License

Public evidence repo. No live federation, no external packages.
