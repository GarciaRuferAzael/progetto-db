-- MySQL dump 10.13  Distrib 8.0.38, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: banca
-- ------------------------------------------------------
-- Server version	9.0.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('510cf168874c');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bancari`
--

DROP TABLE IF EXISTS `bancari`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bancari` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(32) DEFAULT NULL,
  `password` varchar(120) DEFAULT NULL,
  `codice_fiscale` varchar(16) DEFAULT NULL,
  `nome` varchar(32) DEFAULT NULL,
  `cognome` varchar(32) DEFAULT NULL,
  `data_nascita` date DEFAULT NULL,
  `indirizzo` varchar(64) DEFAULT NULL,
  `telefono` varchar(16) DEFAULT NULL,
  `filiale_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `codice_fiscale` (`codice_fiscale`),
  KEY `filiale_id` (`filiale_id`),
  CONSTRAINT `bancari_ibfk_1` FOREIGN KEY (`filiale_id`) REFERENCES `filiali` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bancari`
--

LOCK TABLES `bancari` WRITE;
/*!40000 ALTER TABLE `bancari` DISABLE KEYS */;
INSERT INTO `bancari` VALUES (1,'giacomo@mail.com','24326224313224594f35482f6e6e412f7746496353474d43487165344f7a63736a614e31307a724d7a32394b526e686b4f5461453635577256756147','ZFVMMJ46A24F537M','Franco','Garibaldi','2003-12-31','via Bucarest 9','38912345678',1);
/*!40000 ALTER TABLE `bancari` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carte_prepagate`
--

DROP TABLE IF EXISTS `carte_prepagate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carte_prepagate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `numero` varchar(16) DEFAULT NULL,
  `scadenza` date DEFAULT NULL,
  `cvv` varchar(3) DEFAULT NULL,
  `pin` varchar(4) DEFAULT NULL,
  `saldo` float DEFAULT NULL,
  `limite_spesa` float DEFAULT NULL,
  `disabilitata` tinyint(1) DEFAULT NULL,
  `cliente_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero` (`numero`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `carte_prepagate_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clienti` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carte_prepagate`
--

LOCK TABLES `carte_prepagate` WRITE;
/*!40000 ALTER TABLE `carte_prepagate` DISABLE KEYS */;
INSERT INTO `carte_prepagate` VALUES (1,'1234567874986633','2027-08-01','459','2933',260,0,0,1);
/*!40000 ALTER TABLE `carte_prepagate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clienti`
--

DROP TABLE IF EXISTS `clienti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clienti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(32) DEFAULT NULL,
  `password` varchar(120) DEFAULT NULL,
  `codice_fiscale` varchar(16) DEFAULT NULL,
  `nome` varchar(32) DEFAULT NULL,
  `cognome` varchar(32) DEFAULT NULL,
  `data_nascita` date DEFAULT NULL,
  `indirizzo` varchar(64) DEFAULT NULL,
  `telefono` varchar(16) DEFAULT NULL,
  `bancario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `codice_fiscale` (`codice_fiscale`),
  KEY `bancario_id` (`bancario_id`),
  CONSTRAINT `clienti_ibfk_1` FOREIGN KEY (`bancario_id`) REFERENCES `bancari` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clienti`
--

LOCK TABLES `clienti` WRITE;
/*!40000 ALTER TABLE `clienti` DISABLE KEYS */;
INSERT INTO `clienti` VALUES (1,'giacomo@mail.com','24326224313224594f35482f6e6e412f7746496353474d43487165344f7a63736a614e31307a724d7a32394b526e686b4f5461453635577256756147','DTUHPJ62M06C900F','Mario','Rossi','2003-12-31','via Parigi 4','3661234567',1),(5,'giacomo2@mail.com','24326224313224594f35482f6e6e412f7746496353474d43487165344f7a63736a614e31307a724d7a32394b526e686b4f5461453635577256756147','HNMZMN57R24C283J','Paolo','Verdi','2003-12-31','via Londra 1','3381234567',1);
/*!40000 ALTER TABLE `clienti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conti_correnti`
--

DROP TABLE IF EXISTS `conti_correnti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conti_correnti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `saldo` float DEFAULT NULL,
  `cliente1_id` int DEFAULT NULL,
  `cliente2_id` int DEFAULT NULL,
  `filiale_id` int DEFAULT NULL,
  `iban` varchar(27) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `iban` (`iban`),
  KEY `cliente1_id` (`cliente1_id`),
  KEY `cliente2_id` (`cliente2_id`),
  KEY `filiale_id` (`filiale_id`),
  CONSTRAINT `conti_correnti_ibfk_1` FOREIGN KEY (`cliente1_id`) REFERENCES `clienti` (`id`),
  CONSTRAINT `conti_correnti_ibfk_2` FOREIGN KEY (`cliente2_id`) REFERENCES `clienti` (`id`),
  CONSTRAINT `conti_correnti_ibfk_3` FOREIGN KEY (`filiale_id`) REFERENCES `filiali` (`id`),
  CONSTRAINT `conti_correnti_chk_1` CHECK ((`saldo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conti_correnti`
--

LOCK TABLES `conti_correnti` WRITE;
/*!40000 ALTER TABLE `conti_correnti` DISABLE KEYS */;
INSERT INTO `conti_correnti` VALUES (3,180,5,1,1,'IT1112341000000000001'),(5,160,1,NULL,1,'IT0714025000000000001');
/*!40000 ALTER TABLE `conti_correnti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direttori`
--

DROP TABLE IF EXISTS `direttori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direttori` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(32) DEFAULT NULL,
  `password` varchar(120) DEFAULT NULL,
  `codice_fiscale` varchar(16) DEFAULT NULL,
  `nome` varchar(32) DEFAULT NULL,
  `cognome` varchar(32) DEFAULT NULL,
  `data_nascita` date DEFAULT NULL,
  `indirizzo` varchar(64) DEFAULT NULL,
  `telefono` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codice_fiscale` (`codice_fiscale`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direttori`
--

LOCK TABLES `direttori` WRITE;
/*!40000 ALTER TABLE `direttori` DISABLE KEYS */;
INSERT INTO `direttori` VALUES (1,'giacomo@mail.com','24326224313224594f35482f6e6e412f7746496353474d43487165344f7a63736a614e31307a724d7a32394b526e686b4f5461453635577256756147','QDMNZM36L28C920J','Giovanni','Neri','2003-12-31','via Praga 4','33512345678');
/*!40000 ALTER TABLE `direttori` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filiali`
--

DROP TABLE IF EXISTS `filiali`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filiali` (
  `id` int NOT NULL AUTO_INCREMENT,
  `saldo` float DEFAULT NULL,
  `sede` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filiali`
--

LOCK TABLES `filiali` WRITE;
/*!40000 ALTER TABLE `filiali` DISABLE KEYS */;
INSERT INTO `filiali` VALUES (1,9800,'via Roma 1');
/*!40000 ALTER TABLE `filiali` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `garanzie`
--

DROP TABLE IF EXISTS `garanzie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `garanzie` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tiplogia` varchar(256) DEFAULT NULL,
  `file` varchar(256) DEFAULT NULL,
  `valutazione` float DEFAULT NULL,
  `prestito_id` int DEFAULT NULL,
  `mutuo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `prestito_id` (`prestito_id`),
  KEY `mutuo_id` (`mutuo_id`),
  CONSTRAINT `garanzie_ibfk_1` FOREIGN KEY (`prestito_id`) REFERENCES `prestiti` (`id`),
  CONSTRAINT `garanzie_ibfk_2` FOREIGN KEY (`mutuo_id`) REFERENCES `mutui` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `mutui`
--

DROP TABLE IF EXISTS `mutui`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mutui` (
  `id` int NOT NULL AUTO_INCREMENT,
  `importo` float DEFAULT NULL,
  `data_creazione` datetime DEFAULT NULL,
  `data_accettazione` datetime DEFAULT NULL,
  `accettata` tinyint(1) DEFAULT NULL,
  `cliente_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `mutui_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clienti` (`id`),
  CONSTRAINT `mutui_chk_1` CHECK ((`importo` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mutui`
--

LOCK TABLES `mutui` WRITE;
/*!40000 ALTER TABLE `mutui` DISABLE KEYS */;
/*!40000 ALTER TABLE `mutui` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prestiti`
--

DROP TABLE IF EXISTS `prestiti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prestiti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `importo` float DEFAULT NULL,
  `data_creazione` datetime DEFAULT NULL,
  `data_accettazione` datetime DEFAULT NULL,
  `accettata` tinyint(1) DEFAULT NULL,
  `cliente_id` int DEFAULT NULL,
  `conto_corrente_id` int DEFAULT NULL,
  `direttore_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `direttore_id` (`direttore_id`),
  KEY `prestiti_ibfk_2` (`conto_corrente_id`),
  CONSTRAINT `prestiti_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clienti` (`id`),
  CONSTRAINT `prestiti_ibfk_2` FOREIGN KEY (`conto_corrente_id`) REFERENCES `conti_correnti` (`id`),
  CONSTRAINT `prestiti_ibfk_3` FOREIGN KEY (`direttore_id`) REFERENCES `direttori` (`id`),
  CONSTRAINT `prestiti_chk_1` CHECK ((`importo` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prestiti`
--

LOCK TABLES `prestiti` WRITE;
/*!40000 ALTER TABLE `prestiti` DISABLE KEYS */;
INSERT INTO `prestiti` VALUES (6,100,'2024-07-30 13:55:15','2024-07-31 10:41:08',1,1,3,1);
/*!40000 ALTER TABLE `prestiti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `richieste_carte_prepagate`
--

DROP TABLE IF EXISTS `richieste_carte_prepagate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `richieste_carte_prepagate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_creazione` datetime DEFAULT NULL,
  `data_accettazione` datetime DEFAULT NULL,
  `accettata` tinyint(1) DEFAULT NULL,
  `cliente_id` int DEFAULT NULL,
  `bancario_id` int DEFAULT NULL,
  `carta_prepagata_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bancario_id` (`bancario_id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `carta_prepagata_id` (`carta_prepagata_id`),
  CONSTRAINT `richieste_carte_prepagate_ibfk_1` FOREIGN KEY (`bancario_id`) REFERENCES `bancari` (`id`),
  CONSTRAINT `richieste_carte_prepagate_ibfk_2` FOREIGN KEY (`cliente_id`) REFERENCES `clienti` (`id`),
  CONSTRAINT `richieste_carte_prepagate_ibfk_3` FOREIGN KEY (`carta_prepagata_id`) REFERENCES `carte_prepagate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `richieste_carte_prepagate`
--

LOCK TABLES `richieste_carte_prepagate` WRITE;
/*!40000 ALTER TABLE `richieste_carte_prepagate` DISABLE KEYS */;
INSERT INTO `richieste_carte_prepagate` VALUES (1,'2024-08-02 10:02:14','2024-08-02 10:15:41',1,1,1,1),(2,'2024-08-05 09:40:30',NULL,NULL,1,NULL,NULL),(3,'2024-08-06 10:25:48',NULL,NULL,1,NULL,NULL);
/*!40000 ALTER TABLE `richieste_carte_prepagate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `richieste_conti_correnti`
--

DROP TABLE IF EXISTS `richieste_conti_correnti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `richieste_conti_correnti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_creazione` datetime DEFAULT NULL,
  `data_accettazione` datetime DEFAULT NULL,
  `accettata` tinyint(1) DEFAULT NULL,
  `cliente_id` int DEFAULT NULL,
  `bancario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `bancario_id` (`bancario_id`),
  CONSTRAINT `richieste_conti_correnti_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clienti` (`id`),
  CONSTRAINT `richieste_conti_correnti_ibfk_2` FOREIGN KEY (`bancario_id`) REFERENCES `bancari` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `richieste_conti_correnti`
--

LOCK TABLES `richieste_conti_correnti` WRITE;
/*!40000 ALTER TABLE `richieste_conti_correnti` DISABLE KEYS */;
INSERT INTO `richieste_conti_correnti` VALUES (1,'2024-07-25 10:14:32','2024-07-25 14:17:43',0,1,1),(2,'2024-07-25 10:34:15','2024-07-25 14:17:43',1,1,1),(3,'2024-07-26 08:28:41','2024-07-26 08:30:11',1,1,1),(4,'2024-07-29 10:57:34','2024-07-29 11:02:20',1,1,1),(5,'2024-08-01 07:19:18',NULL,NULL,1,NULL),(6,'2024-08-06 10:22:47',NULL,NULL,1,NULL);
/*!40000 ALTER TABLE `richieste_conti_correnti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storico_direzione`
--

DROP TABLE IF EXISTS `storico_direzione`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storico_direzione` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int DEFAULT NULL,
  `direttore_id` int DEFAULT NULL,
  `filiale_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `direttore_id` (`direttore_id`),
  KEY `filiale_id` (`filiale_id`),
  CONSTRAINT `storico_direzione_ibfk_1` FOREIGN KEY (`direttore_id`) REFERENCES `direttori` (`id`),
  CONSTRAINT `storico_direzione_ibfk_2` FOREIGN KEY (`filiale_id`) REFERENCES `filiali` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storico_direzione`
--

LOCK TABLES `storico_direzione` WRITE;
/*!40000 ALTER TABLE `storico_direzione` DISABLE KEYS */;
INSERT INTO `storico_direzione` VALUES (1,2024,1,1);
/*!40000 ALTER TABLE `storico_direzione` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transazioni`
--

DROP TABLE IF EXISTS `transazioni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transazioni` (
  `id` int NOT NULL AUTO_INCREMENT,
  `importo` float DEFAULT NULL,
  `data` datetime DEFAULT NULL,
  `entrata` tinyint(1) DEFAULT NULL,
  `transazione_interna_id` int DEFAULT NULL,
  `transazione_esterna_id` int DEFAULT NULL,
  `descrizione` varchar(256) DEFAULT NULL,
  `causale` varchar(256) DEFAULT NULL,
  `transazione_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `transazione_esterna_id` (`transazione_esterna_id`),
  KEY `transazione_interna_id` (`transazione_interna_id`),
  KEY `transazione_id` (`transazione_id`),
  CONSTRAINT `transazioni_ibfk_1` FOREIGN KEY (`transazione_esterna_id`) REFERENCES `transazioni_esterne` (`id`),
  CONSTRAINT `transazioni_ibfk_2` FOREIGN KEY (`transazione_interna_id`) REFERENCES `transazioni_interne` (`id`),
  CONSTRAINT `transazioni_ibfk_3` FOREIGN KEY (`transazione_id`) REFERENCES `transazioni` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transazioni`
--

LOCK TABLES `transazioni` WRITE;
/*!40000 ALTER TABLE `transazioni` DISABLE KEYS */;
INSERT INTO `transazioni` VALUES (1,100,'2024-07-29 11:08:48',0,1,NULL,'Bonifico in favore di IT0714025000000000001','ciao',2),(2,100,'2024-07-29 11:08:48',1,2,NULL,'Bonifico da IT1112341000000000001',NULL,1),(3,50,'2024-07-29 14:24:19',0,3,NULL,'Bonifico in favore di IT0714025000000000001','prova',4),(4,50,'2024-07-29 14:24:19',1,4,NULL,'Bonifico da IT1112341000000000001',NULL,3),(5,10,'2024-07-29 14:26:16',0,5,NULL,'Bonifico in favore di IT0714025000000000001','test',6),(6,10,'2024-07-29 14:26:16',1,6,NULL,'Bonifico da IT1112341000000000001',NULL,5),(7,100,'2024-07-31 10:41:08',1,7,NULL,'Prestito n. 6',NULL,NULL),(8,100,'2024-08-01 08:02:09',0,8,NULL,'Bonifico in favore di IT0714025000000000001','prova',9),(9,100,'2024-08-01 08:02:09',1,9,NULL,'Bonifico da IT1112341000000000001',NULL,8),(10,100,'2024-08-02 08:02:09',0,10,NULL,'Bonifo in favore di IT0714025000000000001','prova',11),(11,100,'2024-08-02 08:02:09',1,11,NULL,'Bonifico da IT1112341000000000001',NULL,10),(12,100,'2024-08-02 09:18:34',0,12,NULL,'Bonifico in favore di IT0714025000000000002','prova',13),(13,100,'2024-08-02 09:18:34',1,1,NULL,'Bonifico da IT0714025000000000001',NULL,12),(14,100,'2024-08-05 08:56:56',0,13,NULL,'Ricarica carta prepagata 1234567874986633',NULL,15),(15,100,'2024-08-05 08:56:56',1,14,NULL,'Ricarica da IT0714025000000000001',NULL,14),(16,50,'2024-08-05 08:58:40',0,15,NULL,'Ricarica carta prepagata 1234567874986633',NULL,17),(17,50,'2024-08-05 08:58:40',1,16,NULL,'Ricarica da IT1112341000000000001',NULL,16),(18,100,'2024-08-05 08:58:40',0,17,NULL,'Ricarica carta prepagata 1234567874986633',NULL,19),(19,100,'2024-08-05 08:58:40',1,18,NULL,'Ricarica da IT1112341000000000001',NULL,18),(20,10,'2024-08-05 09:36:54',0,19,NULL,'Ricarica carta prepagata 1234567874986633',NULL,21),(21,10,'2024-08-05 09:36:54',1,20,NULL,'Ricarica da IT1112341000000000001',NULL,20);
/*!40000 ALTER TABLE `transazioni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transazioni_esterne`
--

DROP TABLE IF EXISTS `transazioni_esterne`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transazioni_esterne` (
  `id` int NOT NULL AUTO_INCREMENT,
  `iban` varchar(27) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transazioni_esterne`
--

LOCK TABLES `transazioni_esterne` WRITE;
/*!40000 ALTER TABLE `transazioni_esterne` DISABLE KEYS */;
INSERT INTO `transazioni_esterne` VALUES (1,'IT0714025000000000002');
/*!40000 ALTER TABLE `transazioni_esterne` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transazioni_interne`
--

DROP TABLE IF EXISTS `transazioni_interne`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transazioni_interne` (
  `id` int NOT NULL AUTO_INCREMENT,
  `conto_corrente_id` int DEFAULT NULL,
  `carta_prepagata_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `conto_corrente_id` (`conto_corrente_id`),
  KEY `carta_prepagata_id` (`carta_prepagata_id`),
  CONSTRAINT `transazioni_interne_ibfk_1` FOREIGN KEY (`conto_corrente_id`) REFERENCES `conti_correnti` (`id`),
  CONSTRAINT `transazioni_interne_ibfk_2` FOREIGN KEY (`carta_prepagata_id`) REFERENCES `carte_prepagate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transazioni_interne`
--

LOCK TABLES `transazioni_interne` WRITE;
/*!40000 ALTER TABLE `transazioni_interne` DISABLE KEYS */;
INSERT INTO `transazioni_interne` VALUES (1,3,NULL),(2,5,NULL),(3,3,NULL),(4,5,NULL),(5,3,NULL),(6,5,NULL),(7,3,NULL),(8,3,NULL),(9,5,NULL),(10,3,NULL),(11,5,NULL),(12,5,NULL),(13,5,NULL),(14,NULL,1),(15,3,NULL),(16,NULL,1),(17,3,NULL),(18,NULL,1),(19,3,NULL),(20,NULL,1);
/*!40000 ALTER TABLE `transazioni_interne` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-06 12:40:43
