## Backend

### How to use
1. Create .env file in root directory. It should contain:
```
DB_USER=<YOUR DB USER>
DB_PASS=<YOUR DB PASSWORD>
```
2. Edit link in application.yml:
```
ml:
    url: <YOUR ML URL>
```
3. Run docker
4. Run command:
```
docker compose up --build -d
```