-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: campusfix
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'vanshika','vanshika@gmail.com','scrypt:32768:8:1$rg3p5CZOHu2tTJED$5b9f72411f939ac8ea64d322b34646e4a75b83481508418a6a89a5b1124ed2a529df899e07d9e7cf70b5b7418039b3345eae79942e15a2bf5121825d31f7d469');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaints`
--

DROP TABLE IF EXISTS `complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaints` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `category` varchar(100) NOT NULL,
  `location` varchar(200) DEFAULT NULL,
  `priority` varchar(20) DEFAULT 'Medium',
  `status` varchar(30) DEFAULT 'Pending',
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaints`
--

LOCK TABLES `complaints` WRITE;
/*!40000 ALTER TABLE `complaints` DISABLE KEYS */;
INSERT INTO `complaints` VALUES (101,1,'Lights not working','Lights in the hostel corridor are not working properly.','Electricity','Hostel Block A','High','Pending',NULL,'2026-08-31 18:30:00'),(102,2,'Water leakage','Water is leaking near the washroom and the floor is wet.','Water','Hostel Block B','High','In Progress',NULL,'2026-09-01 18:30:00'),(103,3,'Wi-Fi connection issue','Wi-Fi keeps disconnecting during online classes.','Internet/Wi-Fi','Academic Block','Medium','Pending',NULL,'2026-09-02 18:30:00'),(104,4,'Classroom cleaning required','The classroom floor and desks need proper cleaning.','Cleanliness','Room 204','Low','Resolved',NULL,'2026-09-03 18:30:00'),(105,5,'Hostel fan not working','The ceiling fan is not working in the hostel room.','Electricity','Hostel Block C','Medium','Pending',NULL,'2026-09-04 18:30:00'),(106,1,'Damaged canteen chairs','Some chairs in the canteen are damaged and need repair.','Food/Canteen','Main Canteen','Low','In Progress',NULL,'2026-09-05 18:30:00'),(107,2,'Projector not working','The classroom projector does not turn on during lectures.','Academic','Room 105','Medium','Pending',NULL,'2026-09-06 18:30:00'),(108,3,'Broken campus pathway','A section of the pathway near the library needs repair.','Infrastructure','Near Library','Medium','Resolved',NULL,'2026-09-07 18:30:00'),(109,4,'Water cooler not working','The water cooler is not dispensing drinking water.','Water','Academic Block','High','Pending',NULL,'2026-09-08 18:30:00'),(110,5,'Library computer issue','A computer in the library is not starting.','Infrastructure','Library','Low','In Progress',NULL,'2026-09-09 18:30:00'),(111,1,'Washroom tap leaking','The washroom tap continues to leak after use.','Water','Hostel Block A','Medium','Pending',NULL,'2026-09-10 18:30:00'),(112,2,'Garbage not collected','Garbage bins near the hostel entrance need to be emptied.','Cleanliness','Hostel Block B','High','In Progress',NULL,'2026-09-11 18:30:00'),(113,3,'Classroom lights flickering','The lights in the classroom flicker during lectures.','Electricity','Room 301','Medium','Pending',NULL,'2026-09-12 18:30:00'),(114,4,'Canteen drinking water issue','The drinking water station near the canteen is not working.','Food/Canteen','Main Canteen','High','Resolved',NULL,'2026-09-13 18:30:00'),(115,5,'Library Wi-Fi weak','The Wi-Fi signal is weak in the library reading area.','Internet/Wi-Fi','Library','Low','Pending',NULL,'2026-09-14 18:30:00'),(116,1,'Broken classroom desk','A classroom desk is damaged and needs repair.','Infrastructure','Room 202','Low','In Progress',NULL,'2026-09-15 18:30:00'),(117,2,'Hostel bathroom cleaning','The shared bathroom needs more regular cleaning.','Cleanliness','Hostel Block C','Medium','Resolved',NULL,'2026-09-16 18:30:00'),(118,3,'Lab computer not working','A computer in the computer lab does not start.','Academic','Computer Lab 1','Medium','Resolved',NULL,'2026-09-17 18:30:00'),(119,4,'Campus streetlight issue','A streetlight near the campus parking area is not working.','Electricity','Parking Area','High','Pending',NULL,'2026-09-18 18:30:00'),(120,9,'wifi','wifi not working','Wi-Fi / Internet','Admin Block','Medium','In Progress','289d4fc2ecc14d5da97c6c2d955b5ec7.png','2026-09-21 12:02:05'),(121,9,'wifi','wifi not work','Wi-Fi / Internet','MMICTBM','Medium','Pending',NULL,'2026-09-21 12:35:45');
/*!40000 ALTER TABLE `complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `student_id` varchar(50) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Aarav Sharma','STU001','CSE','aarav@example.com','demo','2026-09-20 02:39:09'),(2,'Priya Verma','STU002','CSE','priya@example.com','demo','2026-09-20 02:39:09'),(3,'Rohan Kumar','STU003','AI','rohan@example.com','demo','2026-09-20 02:39:09'),(4,'Ananya Singh','STU004','AI','ananya@example.com','demo','2026-09-20 02:39:09'),(5,'Kabir Gupta','STU005','CSE','kabir@example.com','demo','2026-09-20 02:39:09'),(6,'vanshika','13251052','BSc AI & ML','vanshikasaini4107@gmail.com','scrypt:32768:8:1$flpo7jMQpWyZA54j$cc62a261dd0fe5414eaea99b7bd007c5f9d9e2ffece92a9423dd441ae591484bfb20f55dffd96d85c20f6902c4cec02296542cc9e813b776d7ae6c00436a47fe','2026-09-20 16:29:05'),(7,'Ayra','STU006','BCA','ayra@gmail.com','scrypt:32768:8:1$Bm37XR51s6ruFp6r$0dfe549645461e16cbacc32d6bba5ab65e0f83c98470ec09937635d955183f075c9b912264a6750f85a2501ed5c358897cd91d8f9a3ccf34901e0b85251a8ed6','2026-09-20 17:34:23'),(8,'Lovepreet Chaudhary','STU007','B.Tech CSE','lovepreet@gmail.com','scrypt:32768:8:1$Go4GTX6VukHqS8mD$ad06901a899b47a2df1fda0701677d3ae3ad358a300ede4a6348e46fe11fdba594b4dfdf92677c6b45ed0034acc31ae63993267dc5e25d48bc7f114d8c6955a4','2026-09-20 17:45:37'),(9,'Vasudev Sharma','STU008','BBA','vasudev@gmail.com','scrypt:32768:8:1$ePUXQFJW1ubOzOP6$a58c65cd07a25b7b9360b223bf996b52ac3a45648e16ba01b6cade86a80c95db7f189e23ef5becc5256be4aa17cc77f899b9a40e0c432f25857e1bb48465c847','2026-09-21 11:57:34');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-21 18:56:23
