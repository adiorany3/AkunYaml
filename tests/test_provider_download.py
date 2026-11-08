"""Provider downloads retry transport errors without bypassing TLS verification."""
from contextlib import contextmanager
from http.client import IncompleteRead
import ssl
import urllib.error

import pytest

import build_support


URL = "https://raw.githubusercontent.com/example/feed/main/domains.txt"


@pytest.mark.parametrize("error", [
    urllib.error.URLError(ssl.SSLEOFError(8, "unexpected EOF")),
    IncompleteRead(b"partial", 10),
    TimeoutError("timed out"),
    urllib.error.HTTPError(URL, 503, "unavailable", {}, None),
])
def test_download_retries_transient_errors(monkeypatch, error):
    calls, delays = [], []

    @contextmanager
    def open_url(url, timeout):
        calls.append((url, timeout))
        if len(calls) == 1:
            raise error

        class Response:
            def read(self, limit):
                assert limit == 40 * 1024 * 1024 + 1
                return b"complete feed"

        yield Response()

    monkeypatch.setattr(build_support.urllib.request, "urlopen", open_url)
    monkeypatch.setattr(build_support.time, "sleep", delays.append)
    assert build_support.fetch(URL) == b"complete feed"
    assert calls == [(URL, 90)] * 2
    assert delays == [1]


@pytest.mark.parametrize("error,attempts", [
    (urllib.error.URLError(ssl.SSLEOFError(8, "unexpected EOF")), 3),
    (urllib.error.URLError(ssl.SSLCertVerificationError(1, "invalid certificate")), 1),
    (urllib.error.HTTPError(URL, 404, "not found", {}, None), 1),
])
def test_download_failure_is_bounded_and_identifies_source(monkeypatch, error, attempts):
    calls = []

    def open_url(url, timeout):
        calls.append(url)
        raise error

    monkeypatch.setattr(build_support.urllib.request, "urlopen", open_url)
    monkeypatch.setattr(build_support.time, "sleep", lambda _: None)
    with pytest.raises(OSError, match="Unduhan provider gagal") as caught:
        build_support.fetch(URL)
    assert URL in str(caught.value)
    assert len(calls) == attempts
