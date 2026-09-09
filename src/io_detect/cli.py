import argparse
import json

from io_detect.ingest.adapters.iu import load_iu, load_iu_parquet
from io_detect.ingest.adapters.clemson import load_clemson
from io_detect.pipeline import run

LOADERS = {
    "iu": load_iu,
    "iu-parquet": load_iu_parquet,
    "clemson": load_clemson,
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="io_detect")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect")
    d.add_argument("--input", required=True)
    d.add_argument("--source", default="iu", choices=sorted(LOADERS))
    return p


def main():
    args = build_parser().parse_args()

    df = LOADERS[args.source](args.input)
    out = run(df)
    out["flagged_accounts"] = sorted(out["flagged_accounts"])
    out.pop("triage", None)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
