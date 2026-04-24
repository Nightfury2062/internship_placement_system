CREATE DATABASE  IF NOT EXISTS `internship_placement_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `internship_placement_db`;
-- MySQL dump 10.13  Distrib 8.0.44, for macos15 (arm64)
--
-- Host: localhost    Database: internship_placement_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `Admin`
--

DROP TABLE IF EXISTS `Admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Admin` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Admin`
--

LOCK TABLES `Admin` WRITE;
/*!40000 ALTER TABLE `Admin` DISABLE KEYS */;
INSERT INTO `Admin` VALUES (1,'Muhammad Ashraf','ashraf24344@university.edu'),(2,'Rohit kunnath','rohit24480@university.edu'),(3,'Nikhil Singhal','nikhil24384@university.edu');
/*!40000 ALTER TABLE `Admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Company`
--

DROP TABLE IF EXISTS `Company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Company` (
  `company_id` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(100) NOT NULL,
  `industry` varchar(50) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`company_id`),
  KEY `idx_company_name` (`company_name`),
  KEY `idx_company_industry` (`industry`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Company`
--

LOCK TABLES `Company` WRITE;
/*!40000 ALTER TABLE `Company` DISABLE KEYS */;
INSERT INTO `Company` VALUES (1,'Google','Technology','Bangalore'),(2,'Microsoft','Technology','Hyderabad'),(3,'Amazon','E-commerce','Mumbai'),(4,'Goldman Sachs','Finance','Bangalore'),(5,'Deloitte','Consulting','Delhi'),(6,'Flipkart','E-commerce','Bangalore'),(7,'TCS','IT Services','Mumbai'),(8,'Infosys','IT Services','Bangalore'),(9,'NVIDIA','Technology','Pune'),(10,'Adobe','Software','Noida'),(11,'Oracle','Technology','Bangalore'),(12,'IBM','Technology','Mumbai'),(13,'Samsung','Electronics','Noida'),(14,'Intel','Technology','Bangalore'),(15,'Accenture','Consulting','Pune');
/*!40000 ALTER TABLE `Company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Forum_Post`
--

DROP TABLE IF EXISTS `Forum_Post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Forum_Post` (
  `post_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `company_id` int DEFAULT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`post_id`),
  KEY `idx_forum_student` (`student_id`),
  KEY `idx_forum_company` (`company_id`),
  KEY `idx_forum_created_at` (`created_at`),
  CONSTRAINT `forum_post_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `Student` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `forum_post_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `Company` (`company_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Forum_Post`
--

LOCK TABLES `Forum_Post` WRITE;
/*!40000 ALTER TABLE `Forum_Post` DISABLE KEYS */;
INSERT INTO `Forum_Post` VALUES (1,1,1,'Has anyone attended the Google interview recently? What kind of questions should I expect?','2024-02-01 10:30:00'),(2,2,2,'Microsoft is coming for on-campus recruitment next week. Looking forward to it!','2024-02-02 14:15:00'),(3,3,1,'Just completed my Google interview. The interviewers were very friendly and professional.','2024-02-03 16:45:00'),(4,4,9,'NVIDIA ML Engineer role seems very interesting. Has anyone applied?','2024-02-04 09:20:00'),(5,5,7,'TCS placement process is quite straightforward. Good luck to everyone applying!','2024-02-05 11:00:00'),(6,6,4,'Goldman Sachs interview tips: Focus on data structures and problem-solving skills.','2024-02-06 13:30:00'),(7,7,13,'Samsung hardware roles are perfect for electronics students. Great opportunity!','2024-02-07 15:00:00'),(8,8,1,'Google coding round was challenging but fair. Practice LeetCode medium/hard problems.','2024-02-08 10:00:00'),(9,9,10,'Adobe creative suite knowledge is a plus for the UX Designer role.','2024-02-09 12:30:00'),(10,10,11,'Oracle database knowledge really helps for their DBA position. Prepare SQL thoroughly.','2024-02-10 14:00:00'),(11,1,3,'Amazon SDE intern selection process has 2 coding rounds followed by HR round.','2024-02-09 16:00:00'),(12,2,5,'Deloitte focuses more on consulting case studies. Prepare accordingly.','2024-02-10 09:00:00');
/*!40000 ALTER TABLE `Forum_Post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Job_Posting`
--

DROP TABLE IF EXISTS `Job_Posting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Job_Posting` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `role` varchar(100) NOT NULL,
  `salary` float DEFAULT NULL,
  `eligibility_cgpa` float DEFAULT NULL,
  `branch_allowed` varchar(200) DEFAULT NULL,
  `batch_allowed` int DEFAULT NULL,
  `status` varchar(20) DEFAULT 'pending',
  PRIMARY KEY (`job_id`),
  KEY `idx_job_company` (`company_id`),
  KEY `idx_job_status` (`status`),
  KEY `idx_job_eligibility` (`eligibility_cgpa`),
  KEY `idx_job_salary` (`salary`),
  CONSTRAINT `job_posting_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `Company` (`company_id`) ON DELETE CASCADE,
  CONSTRAINT `job_posting_chk_1` CHECK ((`salary` > 0)),
  CONSTRAINT `job_posting_chk_2` CHECK (((`eligibility_cgpa` >= 0.0) and (`eligibility_cgpa` <= 10.0))),
  CONSTRAINT `job_posting_chk_3` CHECK ((`status` in (_utf8mb4'approved',_utf8mb4'pending',_utf8mb4'rejected')))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Job_Posting`
--

LOCK TABLES `Job_Posting` WRITE;
/*!40000 ALTER TABLE `Job_Posting` DISABLE KEYS */;
INSERT INTO `Job_Posting` VALUES (1,1,'Software Engineer',1800000,8,'Computer Science,Electronics',2024,'approved'),(2,1,'Data Scientist',2000000,8.5,'Computer Science',2024,'approved'),(3,2,'Software Development Engineer',1900000,8,'Computer Science,Electronics,Electrical',2024,'approved'),(4,2,'Cloud Solutions Architect',2200000,8.5,'Computer Science',2024,'approved'),(5,3,'SDE Intern',1500000,7.5,'Computer Science,Electronics',2024,'approved'),(6,4,'Financial Analyst',1700000,8,'Computer Science,Electronics',2024,'approved'),(7,5,'Business Analyst',1200000,7.5,'Computer Science,Mechanical,Electronics',2024,'approved'),(8,6,'Product Manager',1600000,8,'Computer Science',2024,'pending'),(9,7,'Software Developer',800000,7,'Computer Science,Electronics,Electrical',2024,'approved'),(10,8,'System Engineer',900000,7,'Computer Science,Electronics,Electrical,Mechanical',2024,'approved'),(11,9,'ML Engineer',2100000,8.5,'Computer Science',2024,'approved'),(12,10,'UX Designer',1400000,7.5,'Computer Science',2024,'approved'),(13,11,'Database Administrator',1300000,7.5,'Computer Science,Electronics',2024,'approved'),(14,12,'DevOps Engineer',1750000,8,'Computer Science',2024,'approved'),(15,13,'Hardware Engineer',1100000,7.5,'Electronics,Electrical',2024,'approved'),(16,14,'Chip Design Engineer',1950000,8.5,'Electronics',2024,'approved'),(17,15,'Technology Consultant',1350000,7.5,'Computer Science,Electronics',2024,'approved'),(18,1,'SWE Intern 2025',1200000,8,'Computer Science',2025,'approved'),(19,3,'Software Engineer 2025',1600000,7.5,'Computer Science,Electronics',2025,'approved'),(20,9,'AI Research Intern',1800000,8.5,'Computer Science',2025,'pending');
/*!40000 ALTER TABLE `Job_Posting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Offer`
--

DROP TABLE IF EXISTS `Offer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Offer` (
  `offer_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `job_id` int NOT NULL,
  `offer_status` varchar(20) DEFAULT 'pending',
  PRIMARY KEY (`offer_id`),
  KEY `idx_offer_student` (`student_id`),
  KEY `idx_offer_job` (`job_id`),
  KEY `idx_offer_status` (`offer_status`),
  CONSTRAINT `offer_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `Student` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `offer_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `Job_Posting` (`job_id`) ON DELETE CASCADE,
  CONSTRAINT `offer_chk_1` CHECK ((`offer_status` in (_utf8mb4'accepted',_utf8mb4'rejected',_utf8mb4'pending')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Offer`
--

LOCK TABLES `Offer` WRITE;
/*!40000 ALTER TABLE `Offer` DISABLE KEYS */;
INSERT INTO `Offer` VALUES (1,1,1,'pending'),(2,2,2,'pending'),(3,3,1,'accepted'),(4,4,2,'pending'),(5,4,9,'pending'),(6,6,1,'rejected'),(7,6,4,'pending'),(8,8,12,'accepted'),(9,10,2,'pending'),(10,10,11,'pending');
/*!40000 ALTER TABLE `Offer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Student`
--

DROP TABLE IF EXISTS `Student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Student` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `roll_number` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `branch` varchar(50) NOT NULL,
  `batch` int NOT NULL,
  `cgpa` float NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `roll_number` (`roll_number`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_student_cgpa` (`cgpa`),
  KEY `idx_student_branch` (`branch`),
  KEY `idx_student_batch` (`batch`),
  CONSTRAINT `student_chk_1` CHECK (((`cgpa` >= 0.0) and (`cgpa` <= 10.0)))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Student`
--

LOCK TABLES `Student` WRITE;
/*!40000 ALTER TABLE `Student` DISABLE KEYS */;
INSERT INTO `Student` VALUES (1,'2024101','Priya Sharma','Electronics',2024,9.1,'priya.sharma@university.edu'),(2,'2024102','Rahul Verma','Mechanical',2024,7.8,'rahul.verma@university.edu'),(3,'2024103','Sumit Kumar','Computer Science',2024,9.3,'Sumit@university.edu'),(4,'2024104','Satayjit Singh','Electrical',2024,8.2,'Satyajitsingh@university.edu'),(5,'2024105','Ritanshu Sharma','Computer Science',2024,8.6,'ritanshu@university.edu'),(6,'2024106','Nishnat jangid','Electronics',2024,7.5,'nishant@university.edu'),(7,'2024107','Meera Iyer','Computer Science',2024,9,'meera.iyer@university.edu'),(8,'2025001','Amit Kumar','Computer Science',2025,8.4,'amit.kumar@university.edu'),(9,'2025002','Divya Nair','Mechanical',2025,8.1,'divya.nair@university.edu'),(10,'2025003','Karthik Menon','Electronics',2025,8.8,'karthik.menon@university.edu'),(11,'2025004','Pooja Gupta','Computer Science',2025,9.2,'pooja.gupta@university.edu'),(12,'2025005','Ravi Shankar','Electrical',2025,7.9,'ravi.shankar@university.edu'),(13,'3','Nikhil','Computer Science',2024,9.2,'Nikhil@mail.com');
/*!40000 ALTER TABLE `Student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'internship_placement_db'
--

--
-- Dumping routines for database 'internship_placement_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-16 17:55:17
