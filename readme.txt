1. Copiare il file .env.example e rinominarlo in .env

2. Cambiare le credenziali presenti nel file .env

3. Buildare l'immagine del backend
docker build -t banca-backend .

4. Avviare i servizi attraverso docker-compose:
docker-compose up -d

5. Caricare il dump sul server mysql:
mysql -h localhost -P 3306 --protocol=TCP -u root -p password < app/db.sql

6. Connettersi all'applicativo:
http://127.0.0.1:8080

7. Effettaure il login:
Sia per cliente, che per bancario e direttore le credenziali sono:
giacomo@mail.com:password