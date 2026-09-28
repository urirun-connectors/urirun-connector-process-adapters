# urirun-connector-process-adapters

Docker Sandbox and Chrome DevTools Protocol (CDP) Process URI adapters (`sandbox://`, `pypi://`, `browser://`) for urirun.

## Features
- **Docker Sandbox Runner**: Run untrusted commands or isolated Python tools (`pypi://<pkg>/<tool>`, `sandbox://run`).
- **CDP Browser Controller**: Translate `browser://navigate`, `browser://click`, `browser://screenshot` into CDP JSON-RPC frames.
