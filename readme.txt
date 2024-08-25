1. Cambiare le credenziali presenti nel file docker-compose.yml

2. Buildare l'immagine del backend
docker build -t banca-backend .

3. Avviare i servizi attraverso docker compose:
docker compose up -d

4. Caricare il dump sul server mysql:
mysql -h localhost -P 3306 --protocol=TCP -u root -p banca < app/db/db.sql

5. Connettersi all'applicativo:
http://127.0.0.1:8080

6. Effettaure il login:
Sia per cliente, che per bancario e direttore le credenziali sono:
giacomo@mail.com:password