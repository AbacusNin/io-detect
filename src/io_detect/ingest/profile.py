import polars as pl


def profile_file(path: str, sample_rows: int = 5000) -> dict:
    df = pl.read_csv(path, n_rows=sample_rows, infer_schema_length=sample_rows)
    n = df.height
    cols = []
    for name in df.columns:
        s = df[name]
        cols.append({
            "name": name,
            "dtype": str(s.dtype),
            "null_rate": (s.null_count() / n) if n else 0.0,
            "n_unique": s.n_unique(),
            "examples": s.drop_nulls().head(3).to_list(),
        })
    return {"columns": cols, "sampled_rows": n}
