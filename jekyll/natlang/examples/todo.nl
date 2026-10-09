# todo.nl — a todo list API
# Shows: state, CRUD, JSON responses, error handling

Create an HTTP server on port 8081.
Store a list of todo items in memory. Each item has an id (number), a title (string), and a done (boolean, default false).

When someone visits "GET /", respond with the full list of todos as JSON.
When someone visits "POST /" with a JSON body containing a title, add a new todo with the next id and respond with the created todo as JSON and status 201.
When someone visits "PATCH /:id" with a JSON body, update the todo with that id and respond with the updated todo as JSON. If the id doesn't exist, respond with 404 and { "error": "todo not found" }.
When someone visits "DELETE /:id", remove the todo with that id and respond with 204. If the id doesn't exist, respond with 404.
When someone visits any other path, respond with 404 and { "error": "not found" }.

Start the server and log "Todo API running on http://localhost:8081".