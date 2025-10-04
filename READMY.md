


docker run --name booking_db `
    -p 6432:5432 `
    -e POSTGRES_USER=admin `
    -e POSTGRES_PASSWORD=admin `
    -e POSTGRES_DB=booking `
    --network=my_network `
    --volume pg_booking_data:/var/lib/postgresql/data `
    -d postgres:16



docker run --name booking_cache `
    -p 7379:6379 `
    --network=my_network `
    -d redis:7.4


docker run --name booking_back `
    -p 7777:8000 `
    --network=my_network `
    booking_image

docker run --name celery `
    --network=my_network `
    booking_image `
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker build -t booking_image .