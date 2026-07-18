#!/usr/bin/env python3
"""Best-effort seed data for Testbot: a few flows, a work pool, and flow runs
so list/filter/pagination endpoints have more than an empty array to assert against.
Test-only identifiers (testbot-*) — never production data."""
import json
import sys
import urllib.request

BASE = "http://api:4200/api"


def post(path, body):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def main():
    flow_ids = []
    for name in ["testbot-flow-alpha", "testbot-flow-beta", "testbot-flow-gamma"]:
        flow = post("/flows/", {"name": name})
        flow_ids.append(flow["id"])
        print(f"seed: created flow {name} -> {flow['id']}", file=sys.stderr)

    pool = post("/work_pools/", {"name": "testbot-pool", "type": "process"})
    print(f"seed: created work pool -> {pool['id']}", file=sys.stderr)

    for flow_id in flow_ids:
        run = post("/flow_runs/", {"flow_id": flow_id})
        print(f"seed: created flow run -> {run['id']}", file=sys.stderr)

    print("seed: complete", file=sys.stderr)


if __name__ == "__main__":
    main()
