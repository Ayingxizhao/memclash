# Project Rules

## Frontend
- After every frontend change (Vue, JS, CSS), always run `npm run build` before finishing.

## Backend
- For any artisan commands, use: `docker compose -f compose.dev.yaml exec php-fpm php artisan ...`
- After changes to queued jobs, migrators, or any code that runs in the queue worker, restart it: `docker restart unitedpassport-laravel-queue-worker-1`

## Testing
- After making changes to the public form (`/form-apply`), test the full flow end-to-end: fetch the form via `GET /api/v1/public/forms/apply`, fill all required fields with realistic test data, and submit via `POST /api/v1/public/forms/apply/submit`. Confirm a new entry is created and return the entry ID.

## Security
- Files are stored in private storage (`local` disk) and served via signed URLs through `GET /api/v1/files/{id}` with `signed` middleware.
- Any public-facing entry links for users must also use signed URLs (via `URL::signedRoute`) to prevent unauthorized access. Never expose entry data through plain/unsigned routes.
