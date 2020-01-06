heroku pg:backups:capture --app derby-pub-and-club-darts
heroku pg:backups:download --app derby-pub-and-club-darts

docker cp latest.dump db:/var/lib/postgresql/data
docker exec db pg_restore --clean  --no-privileges --no-owner -U postgres -d postgres /var/lib/postgresql/data/latest.dump