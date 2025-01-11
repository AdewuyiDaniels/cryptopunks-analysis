# tests/test_fetch_cryptopunks_data.py
import pytest
from scripts.fetch_cryptopunks_data import fetch_cryptopunks_transfers

def test_fetch_cryptopunks_transfers():
    api_key = "YourApiKeyToken"
    data = fetch_cryptopunks_transfers(api_key)
    assert data["status"] == "1"
    assert len(data["result"]) > 0