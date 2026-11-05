#!/usr/bin/env bash
# Deploy the shop app artifact to AWS.
# Safe by default: DRY_RUN=true means "print what I would do, change nothing".
set -euo pipefail

CLOUD="aws"
DRY_RUN="${DRY_RUN:-true}"
VERSION="${VERSION:-1.0.0}"
ARTIFACT="${ARTIFACT:-artifacts/shop-app.tar.gz}"
LOG_DIR="${LOG_DIR:-logs}"
TARGET="s3://${AWS_BUCKET:-sai-shop-artifacts-aws-demo}/shop-app"

# If the Package stage wrote a version file, use that version.
if [ -f "artifacts/version.txt" ]; then
  VERSION="$(cat artifacts/version.txt)"
fi

LOG_FILE="$LOG_DIR/deploy-$CLOUD.json"

echo "Cloud: AWS"
echo "Target: $TARGET"
echo "Version: $VERSION"
echo "DRY_RUN: $DRY_RUN"

if [ -f "$ARTIFACT" ]; then
  echo "Artifact found: $ARTIFACT"
else
  echo "Artifact not found at $ARTIFACT (in a full Jenkins run, the Package stage creates it first)"
fi

mkdir -p "$LOG_DIR"

# Duplicate guard: do not deploy the same version two times.
if [ -f "$LOG_FILE" ] && grep -q "\"version\": \"$VERSION\"" "$LOG_FILE"; then
  echo "Version $VERSION already done, skipping."
  exit 0
fi

if [ "$DRY_RUN" = "true" ]; then
  echo "DRY-RUN: I would run: aws s3 cp "$ARTIFACT" "$TARGET/shop-app-$VERSION.tar.gz""
  printf '{"cloud": "%s", "version": "%s", "mode": "dry-run", "status": "simulated", "target": "%s"}\n' "$CLOUD" "$VERSION" "$TARGET" > "$LOG_FILE"
  echo "Wrote dry-run log: $LOG_FILE"
  exit 0
fi

echo "Real run requested. Command: aws s3 cp "$ARTIFACT" "$TARGET/shop-app-$VERSION.tar.gz""
if command -v aws >/dev/null 2>&1; then
  aws s3 cp "$ARTIFACT" "$TARGET/shop-app-$VERSION.tar.gz"
  printf '{"cloud": "%s", "version": "%s", "mode": "real", "status": "deployed", "target": "%s"}\n' "$CLOUD" "$VERSION" "$TARGET" > "$LOG_FILE"
else
  echo "ERROR: aws CLI is not installed, so I cannot deploy for real. Install it and add credentials in Jenkins first." >&2
  exit 1
fi
