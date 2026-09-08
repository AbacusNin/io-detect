import argparse
import json

from io_detect.ingest.adapters.iu import load_iu
from io_detect.pipeline import run


def main():
    p = argparse.ArgumentParser(prog="io_detect")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect")
    d.add_argument("--input", required=True)
    d.add_argument("--source", default="iu")
    args = p.parse_args()

    df = load_iu(args.input)
    out = run(df)
    out["flagged_accounts"] = sorted(out["flagged_accounts"])
    out.pop("triage", None)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
