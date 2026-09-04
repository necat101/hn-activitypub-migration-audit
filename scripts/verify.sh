#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Verifying migration audit fixtures ==="

# 1. Move fixture identifies actor/object and migration target but does not contain historical post bodies
echo "[1] Move fixture does not contain post bodies from archive.json"
python3 -c "
import json, pathlib
move = json.loads(pathlib.Path('fixtures/move.json').read_text())
archive = json.loads(pathlib.Path('fixtures/archive.json').read_text())
bodies = [i.get('content','') for i in archive.get('orderedItems',[])]
s = json.dumps(move)
assert 'actor' in move, 'Move missing actor'
assert 'object' in move, 'Move missing object'
assert 'target' in move, 'Move missing target'
for b in bodies:
    assert b not in s, f'Move should not contain post body: {b[:40]}'
print('  PASS')
"

# 2. New actor contains alias relationship
echo "[2] New actor contains alias relationship (alsoKnownAs)"
python3 -c "
import json, pathlib
old = json.loads(pathlib.Path('fixtures/old_actor.json').read_text())
new = json.loads(pathlib.Path('fixtures/new_actor.json').read_text())
assert old['id'] in new.get('alsoKnownAs', []), 'alias relationship missing'
print('  PASS')
"

# 3. Follower migration and historical-content migration are separate concepts
echo "[3] Follower migration vs historical-content migration are separate"
python3 -c "
import json, pathlib
move = json.loads(pathlib.Path('fixtures/move.json').read_text())
archive = json.loads(pathlib.Path('fixtures/archive.json').read_text())
assert move.get('type') == 'Move'
assert archive.get('type') == 'OrderedCollection'
assert len(archive.get('orderedItems',[])) > 0
print('  PASS')
"

# 4. Absence-of-bodies caveat (checker must mention it)
echo "[4] Caveat about absence of bodies not being proof is present"
grep -q "not itself proof" scripts/check_migration.py
echo "  PASS"

# 5. Self-destruct is implementation tooling, not W3C requirement
echo "[5] Self-destruct described as implementation tooling, not W3C requirement"
grep -q "self-destruct" scripts/check_migration.py
grep -q "not a W3C" scripts/check_migration.py
echo "  PASS"

# 6. Checker runs and passes
echo "[6] Checker executes successfully"
python3 scripts/check_migration.py

echo ""
echo "All verifications passed."
