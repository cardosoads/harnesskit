#!/usr/bin/env bash
# =============================================================================
# OverSpec Validation Script
# =============================================================================
# Validates all YAML and JSON files in the .overspec directory for syntax
# correctness. Optionally validates agent YAML files against _schema.json
# if a JSON Schema validator (ajv) is available.
#
# Usage: bash .overspec/scripts/validate.sh
# =============================================================================

set -euo pipefail

OVERSPEC_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0
WARNINGS=0
CHECKED=0

# Colors (disabled if not a terminal)
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' NC=''
fi

log_ok()    { echo -e "  ${GREEN}✓${NC} $1"; }
log_err()   { echo -e "  ${RED}✗${NC} $1"; ERRORS=$((ERRORS + 1)); }
log_warn()  { echo -e "  ${YELLOW}!${NC} $1"; WARNINGS=$((WARNINGS + 1)); }

# ---------------------------------------------------------------------------
# 1. Validate JSON files
# ---------------------------------------------------------------------------
echo "Validating JSON files..."
while IFS= read -r -d '' file; do
  rel="${file#"$OVERSPEC_DIR"/}"
  if python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
    log_ok "$rel"
  else
    log_err "$rel — invalid JSON"
  fi
  CHECKED=$((CHECKED + 1))
done < <(find "$OVERSPEC_DIR" -name '*.json' -not -path '*/artifacts/*' -print0)

# ---------------------------------------------------------------------------
# 2. Validate YAML files
# ---------------------------------------------------------------------------
echo ""
echo "Validating YAML files..."

# Check if python3 + PyYAML are available
if python3 -c "import yaml" 2>/dev/null; then
  YAML_VALIDATOR="python3"
else
  log_warn "PyYAML not installed — skipping YAML validation (pip install pyyaml)"
  YAML_VALIDATOR=""
fi

if [ -n "$YAML_VALIDATOR" ]; then
  while IFS= read -r -d '' file; do
    rel="${file#"$OVERSPEC_DIR"/}"
    if python3 -c "import yaml, sys; yaml.safe_load(open('$file'))" 2>/dev/null; then
      log_ok "$rel"
    else
      log_err "$rel — invalid YAML"
    fi
    CHECKED=$((CHECKED + 1))
  done < <(find "$OVERSPEC_DIR" -name '*.yaml' -o -name '*.yml' | sort | tr '\n' '\0')
fi

# ---------------------------------------------------------------------------
# 3. Validate agent files against schema (if ajv-cli is available)
# ---------------------------------------------------------------------------
echo ""
AGENT_SCHEMA="$OVERSPEC_DIR/core/agents/_schema.json"
if [ -f "$AGENT_SCHEMA" ]; then
  if command -v ajv &>/dev/null; then
    echo "Validating agent files against schema..."
    while IFS= read -r -d '' file; do
      rel="${file#"$OVERSPEC_DIR"/}"
      # Convert YAML to JSON for validation
      json_tmp=$(mktemp)
      if python3 -c "import yaml,json,sys; json.dump(yaml.safe_load(open('$file')),open('$json_tmp','w'))" 2>/dev/null; then
        if ajv validate -s "$AGENT_SCHEMA" -d "$json_tmp" --spec=draft7 2>/dev/null; then
          log_ok "$rel — schema valid"
        else
          log_err "$rel — schema validation failed"
        fi
      else
        log_warn "$rel — could not convert to JSON for schema validation"
      fi
      rm -f "$json_tmp"
      CHECKED=$((CHECKED + 1))
    done < <(find "$OVERSPEC_DIR/core/agents" -name '*.agent.yaml' -print0)
  else
    echo "Schema validation (agent files)..."
    log_warn "ajv-cli not installed — skipping schema validation (npm install -g ajv-cli)"
  fi
fi

# ---------------------------------------------------------------------------
# 4. Check required files exist
# ---------------------------------------------------------------------------
echo ""
echo "Checking required files..."

REQUIRED_FILES=(
  "overspec.yaml"
  "state.json"
  "core/agents/sheldon.agent.yaml"
  "core/engine/workflow-engine.md"
  "core/engine/state-machine.md"
  "core/constitution.md"
  "schemas/spec-schema.json"
)

for req in "${REQUIRED_FILES[@]}"; do
  if [ -f "$OVERSPEC_DIR/$req" ]; then
    log_ok "$req"
  else
    log_err "$req — missing required file"
  fi
  CHECKED=$((CHECKED + 1))
done

# ---------------------------------------------------------------------------
# 5. Check required directories exist
# ---------------------------------------------------------------------------
echo ""
echo "Checking required directories..."

REQUIRED_DIRS=(
  "artifacts"
  "core/agents"
  "core/engine"
  "core/workflows"
  "handoffs"
  "schemas"
  "specs"
  "teams"
)

for dir in "${REQUIRED_DIRS[@]}"; do
  if [ -d "$OVERSPEC_DIR/$dir" ]; then
    log_ok "$dir/"
  else
    log_err "$dir/ — missing required directory"
  fi
  CHECKED=$((CHECKED + 1))
done

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "==========================================="
echo "  Validation complete"
echo "  Checked: $CHECKED items"
echo -e "  Passed:  ${GREEN}$((CHECKED - ERRORS))${NC}"
if [ $ERRORS -gt 0 ]; then
  echo -e "  Failed:  ${RED}$ERRORS${NC}"
fi
if [ $WARNINGS -gt 0 ]; then
  echo -e "  Warnings: ${YELLOW}$WARNINGS${NC}"
fi
echo "==========================================="

exit $ERRORS
