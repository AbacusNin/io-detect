import pytest
from io_detect.ingest.integrity import sha256_file, verify, IntegrityError

def test_verify_roundtrip(tmp_path):
    p = tmp_path / "f.bin"
    p.write_bytes(b"abc")
    h = sha256_file(str(p))
    verify(str(p), h)  # no raise
    with pytest.raises(IntegrityError):
        verify(str(p), "0" * 64)
