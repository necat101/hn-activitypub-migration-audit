#!/usr/bin/env python3
"""Inspect synthetic fixtures and report what Move/actor data contains vs archive."""
import json, pathlib, sys

FIX = pathlib.Path(__file__).parent.parent / "fixtures"

def load(name):
    return json.loads((FIX / name).read_text())

def main():
    old = load("old_actor.json")
    new = load("new_actor.json")
    move = load("move.json")
    archive = load("archive.json")

    print("=== Migration Fixture Inspection ===")
    print()

    # Move fixture identifies actor/object and migration target
    has_actor = "actor" in move
    has_object = "object" in move
    has_target = "target" in move
    print(f"Move fixture has actor:   {has_actor} ({move.get('actor')})")
    print(f"Move fixture has object:  {has_object} ({move.get('object')})")
    print(f"Move fixture has target:  {has_target} ({move.get('target')})")
    print(f"Move type: {move.get('type')}")
    print()

    # Check that Move does NOT contain historical post bodies from archive
    archive_bodies = [item.get("content","") for item in archive.get("orderedItems",[])]
    move_str = json.dumps(move)
    contains_bodies = any(body and body in move_str for body in archive_bodies)
    print(f"Move fixture contains historical post bodies from archive.json: {contains_bodies}")
    if contains_bodies:
        print("  FAIL: Move should not contain post bodies")
    else:
        print("  OK: Move does not embed historical post bodies (separate fixtures)")
    print()

    # New actor contains alias relationship (alsoKnownAs)
    also = new.get("alsoKnownAs", [])
    has_alias = old.get("id") in also
    print(f"New actor alsoKnownAs: {also}")
    print(f"New actor aliases old actor ({old.get('id')}): {has_alias}")
    if has_alias:
        print("  OK: alias relationship present (Mastodon-style: new account aliases old)")
    else:
        print("  FAIL: alias relationship missing")
    print()

    # Follower migration vs historical-content migration — precise implementation statement
    print("Mastodon Move semantics vs historical content:")
    print("  Mastodon uses an ActivityStreams Move whose actor/object identify the old")
    print("  account and whose target identifies the new account; compatible remote")
    print("  software can use that migration to move followers. Historical posts/media")
    print("  are not moved by Mastodon's current profile-move workflow.")
    print("  (W3C ActivityStreams vocabulary itself only says an actor moved an object")
    print("  from an origin to a target — not a normative account-portability definition.)")
    separate = not contains_bodies and has_actor and has_target
    print(f"  Separate concepts demonstrated: {separate}")
    print()

    # Caveat
    print("Caveat:")
    print("  Absence of post bodies from the synthetic Move fixture is not itself proof")
    print("  that no implementation could ever migrate posts — that stronger claim must")
    print("  come from inspected Mastodon documentation or another authoritative deployment source.")
    print()

    # Archive caveat
    print("Archive note:")
    print("  archive.json is a synthetic lab fixture representing historical content kept")
    print("  separate from the synthetic Move activity. Mastodon documentation independently")
    print("  states that posts and media can be exported in an Activity Streams 2.0 archive")
    print("  and that Mastodon currently does not import posts/media as part of a profile")
    print("  move. The fixture itself is not evidence of a standardized post-migration")
    print("  protocol. Its OrderedCollection shape is a fixture design choice.")
    print()

    # Self-destruct note
    print("Branch/server shutdown administration:")
    print("  Mastodon tootctl self-destruct is implementation tooling for broadcasting")
    print("  Delete activities on shutdown, not a W3C ActivityPub requirement.")
    print()

    ok = has_actor and has_object and has_target and (not contains_bodies) and has_alias and separate
    if ok:
        print("RESULT: PASS — fixtures demonstrate the required distinctions.")
        return 0
    else:
        print("RESULT: FAIL — one or more distinctions not satisfied.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
