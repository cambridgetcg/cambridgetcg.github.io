# hello.nl — a web server
# The first natlang program. English compiles to code.

Create an HTTP server on port 8080.
When someone visits "/", respond with a JSON object: { "message": "hello world", "natlang": true }.
When someone visits "/health", respond with { "status": "ok" }.
When someone visits any other path, respond with 404 and { "error": "not found" }.
Start the server and log "Server running on http://localhost:8080".