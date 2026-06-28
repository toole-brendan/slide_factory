#!/usr/bin/env python3
"""Shared helpers for the Army USV/watercraft contracts pulls (FPDS / USAspending / SAM.gov).

Centralizes the three cross-cutting gotchas proven out on the sibling shipbuilding
pulls (see distributed_shipbuilding/.../SAM_GOV_HOWTO.md) and the project rule that
RAW pulls keep FULL native records (every field), per user direction.

  1. macOS IPv6 hang  -> force IPv4 for all socket lookups (else ~225s/request on
     networks with broken IPv6; the single biggest perf gotcha for api.sam.gov).
  2. SAM key          -> read SAM_API_KEY from the pipeline-light root .env.
  3. politeness + bounded retry on the public endpoints; trap SAM 429 and halt.
"""
from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ---- 1. Force IPv4 for every socket lookup in this process ------------------
_ORIG_GETADDRINFO = socket.getaddrinfo


def _ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
    return _ORIG_GETADDRINFO(host, port, socket.AF_INET, type, proto, flags)


socket.getaddrinfo = _ipv4_only

# ---- 2. env ----------------------------------------------------------------
ENV_PATH = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light/.env")
UA = "army-usv-market-research/1.0 (where-to-play workbook)"


def env(key: str) -> str:
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if line.startswith(key + "="):
            return line[len(key) + 1:].strip().strip('"').strip("'")
    raise SystemExit(f"{key} not found in {ENV_PATH}")


# ---- 3. http ---------------------------------------------------------------
class QuotaExhausted(SystemExit):
    pass


def http_get(url: str, headers: dict | None = None, timeout: int = 90,
             tries: int = 4, backoff: float = 2.0):
    """GET -> (text, status). None text on terminal failure. Halts on SAM 429."""
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace"), r.status
        except urllib.error.HTTPError as e:
            if e.code == 429:
                raise QuotaExhausted("HTTP 429: SAM.gov daily quota exhausted (resets midnight UTC). Halting cleanly.")
            if attempt == tries - 1:
                return None, e.code
        except Exception:
            if attempt == tries - 1:
                return None, None
        time.sleep(backoff ** attempt)
    return None, None


def http_post_json(url: str, body: dict, headers: dict | None = None,
                   timeout: int = 120, tries: int = 4, backoff: float = 2.0):
    """POST JSON -> (parsed_json, status). On terminal HTTPError returns the parsed
    error body (so the caller can read USAspending's 422 detail) + the code."""
    h = {"Content-Type": "application/json", "User-Agent": UA}
    if headers:
        h.update(headers)
    data = json.dumps(body).encode("utf-8")
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=h, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace")), r.status
        except urllib.error.HTTPError as e:
            if attempt == tries - 1:
                try:
                    return json.loads(e.read().decode("utf-8", "replace")), e.code
                except Exception:
                    return None, e.code
        except Exception:
            if attempt == tries - 1:
                return None, None
        time.sleep(backoff ** attempt)
    return None, None


# ---- 4. faithful XML -> dict (every element, attribute, repeat) -------------
def _local(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def xml_to_dict(elem):
    """Recursively convert an ElementTree element to a structure capturing ALL
    descendants: attributes prefixed '@', mixed text under '#text', repeated tags
    promoted to lists. A pure leaf element returns its text string. This is how we
    honor "keep all fields" for FPDS (whose Atom feed is XML)."""
    node: dict = {}
    for k, v in elem.attrib.items():
        node[f"@{_local(k)}"] = v
    for child in elem:
        ctag = _local(child.tag)
        cval = xml_to_dict(child)
        if ctag in node:
            if not isinstance(node[ctag], list):
                node[ctag] = [node[ctag]]
            node[ctag].append(cval)
        else:
            node[ctag] = cval
    text = (elem.text or "").strip()
    if text:
        if node:
            node["#text"] = text
        else:
            return text
    return node


# ---- 5. misc ---------------------------------------------------------------
def slugify(s: str) -> str:
    out = "".join(c.lower() if c.isalnum() else "_" for c in s)
    while "__" in out:
        out = out.replace("__", "_")
    return out.strip("_")


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=str)
