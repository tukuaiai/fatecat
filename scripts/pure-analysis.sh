#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
fatecat_bin="$(resolve_fatecat_bin "${runtime_root}")"

exec "${fatecat_bin}" pure-analysis "$@"
