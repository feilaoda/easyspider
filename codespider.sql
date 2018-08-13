-- MySQL dump 10.13  Distrib 5.6.21, for osx10.10 (x86_64)
--
-- Host: localhost    Database: news
-- ------------------------------------------------------
-- Server version	5.6.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `spider_project`
--

DROP TABLE IF EXISTS `spider_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0',
  `process` text NOT NULL,
  `create_at` datetime DEFAULT NULL,
  `queue_name` varchar(30) DEFAULT NULL,
  `url` varchar(1000) DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_name` (`name`),
  KEY `ix_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spider_result`
--

DROP TABLE IF EXISTS `spider_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` varchar(30) NOT NULL,
  `task_id` varchar(64) NOT NULL,
  `url` varchar(1000) NOT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_project` (`project`),
  KEY `ix_task_id` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7568 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spider_scheduler`
--

DROP TABLE IF EXISTS `spider_scheduler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider_scheduler` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` varchar(30) NOT NULL,
  `task_id` varchar(64) NOT NULL,
  `url` varchar(1000) NOT NULL,
  `process` text NOT NULL,
  `next_time` int(11) DEFAULT NULL,
  `last_time` int(11) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_project` (`project`),
  KEY `ix_task_id` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spider_task`
--

DROP TABLE IF EXISTS `spider_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` varchar(30) NOT NULL,
  `task_id` varchar(64) NOT NULL,
  `url` varchar(1000) NOT NULL,
  `callback` varchar(100) DEFAULT NULL,
  `priority` int(11) NOT NULL DEFAULT '0',
  `last_time` int(11) DEFAULT NULL,
  `result` text,
  `status` int(11) NOT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_project` (`project`),
  KEY `ix_task_id` (`task_id`),
  KEY `ix_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=9853 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-05 17:58:32
