-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: 408_everyday
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 课程',8,'add_course'),(26,'Can change 课程',8,'change_course'),(27,'Can delete 课程',8,'delete_course'),(28,'Can view 课程',8,'view_course'),(29,'Can add 章节',7,'add_chapter'),(30,'Can change 章节',7,'change_chapter'),(31,'Can delete 章节',7,'delete_chapter'),(32,'Can view 章节',7,'view_chapter'),(33,'Can add 子章节',10,'add_subchapter'),(34,'Can change 子章节',10,'change_subchapter'),(35,'Can delete 子章节',10,'delete_subchapter'),(36,'Can view 子章节',10,'view_subchapter'),(37,'Can add 题目',9,'add_question'),(38,'Can change 题目',9,'change_question'),(39,'Can delete 题目',9,'delete_question'),(40,'Can view 题目',9,'view_question'),(41,'Can add 练习会话',12,'add_practicesession'),(42,'Can change 练习会话',12,'change_practicesession'),(43,'Can delete 练习会话',12,'delete_practicesession'),(44,'Can view 练习会话',12,'view_practicesession'),(45,'Can add 练习记录',11,'add_practicerecord'),(46,'Can change 练习记录',11,'change_practicerecord'),(47,'Can delete 练习记录',11,'delete_practicerecord'),(48,'Can view 练习记录',11,'view_practicerecord'),(49,'Can add 收藏记录',13,'add_favoritequestion'),(50,'Can change 收藏记录',13,'change_favoritequestion'),(51,'Can delete 收藏记录',13,'delete_favoritequestion'),(52,'Can view 收藏记录',13,'view_favoritequestion'),(53,'Can add 错题记录',14,'add_wrongquestion'),(54,'Can change 错题记录',14,'change_wrongquestion'),(55,'Can delete 错题记录',14,'delete_wrongquestion'),(56,'Can view 错题记录',14,'view_wrongquestion'),(57,'Can add 子章节刷题进度',15,'add_subchapterpracticeprogress'),(58,'Can change 子章节刷题进度',15,'change_subchapterpracticeprogress'),(59,'Can delete 子章节刷题进度',15,'delete_subchapterpracticeprogress'),(60,'Can view 子章节刷题进度',15,'view_subchapterpracticeprogress'),(61,'Can add 错题复习记录',16,'add_wrongquestionreview'),(62,'Can change 错题复习记录',16,'change_wrongquestionreview'),(63,'Can delete 错题复习记录',16,'delete_wrongquestionreview'),(64,'Can view 错题复习记录',16,'view_wrongquestionreview');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$jrJwOo9KS249tTecuUb6BJ$j4RIUWvkRQUITuLTHHlMA3n5SFFblXfp5rZABOG3IcM=','2026-04-17 07:53:02.098789',1,'谭红秋雨','','','3436517506@qq.com',1,1,'2026-04-16 10:53:53.346859'),(2,'pbkdf2_sha256$1200000$y7aVrPLM4KYRFC0dYN6EUB$z7ZAC7HfHDc+xiVc8Pixjb06/RKPOuzulrtBkQuTUAw=',NULL,0,'王宇欣','','','',0,1,'2026-04-17 03:13:54.729624'),(3,'pbkdf2_sha256$1200000$W4WGnmJ4SidjX4qBYGRhjs$0xfQHxqdKCUNhAK8n9E89tLPxpJXpVO+YC7eFxf3oks=',NULL,0,'testuser_api','','','api@test.com',0,1,'2026-04-22 05:25:46.926009'),(4,'pbkdf2_sha256$1200000$JNVZ4xPI5NdWrZaJPD13Wr$IIYh1OZbmUSR31Y79bxqBxH4IYxvECVmE7FEspKFDPg=',NULL,0,'testuser','','','',0,1,'2026-04-22 05:43:55.211060'),(5,'pbkdf2_sha256$1200000$maxtYcshyzXkbD2h8bRb4z$kgTyQPy6oVGVOXl/EE/cJM4Vx9XATQrnSXWZZyJhJDc=',NULL,0,'Believer','','','',0,1,'2026-04-22 05:45:24.155345');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-04-16 11:04:47.551907','1','数据结构',1,'[{\"added\": {}}]',8,1),(2,'2026-04-16 11:04:56.248798','2','计算机组成原理',1,'[{\"added\": {}}]',8,1),(3,'2026-04-16 11:05:02.390311','3','操作系统',1,'[{\"added\": {}}]',8,1),(4,'2026-04-16 11:05:12.120171','4','计算机网络',1,'[{\"added\": {}}]',8,1),(5,'2026-04-16 11:05:40.836277','1','数据结构 / 绪论',1,'[{\"added\": {}}]',7,1),(6,'2026-04-16 11:06:07.075245','2','数据结构 / 线性表',1,'[{\"added\": {}}]',7,1),(7,'2026-04-16 12:10:24.389136','1','数据结构',1,'[{\"added\": {}}]',8,1),(8,'2026-04-16 12:10:37.867765','2','计算机组成原理',1,'[{\"added\": {}}]',8,1),(9,'2026-04-16 12:10:55.579119','3','操作系统',1,'[{\"added\": {}}]',8,1),(10,'2026-04-16 12:11:14.604342','4','计算机网络',1,'[{\"added\": {}}]',8,1),(11,'2026-04-16 12:11:53.478601','1','数据结构 / 绪论',1,'[{\"added\": {}}]',7,1),(12,'2026-04-16 12:22:05.031760','2','数据结构 / 线性表',1,'[{\"added\": {}}]',7,1),(13,'2026-04-16 12:23:33.727385','2','数据结构 / 线性表',2,'[]',7,1),(14,'2026-04-16 12:24:44.311063','2','数据结构 / 线性表',2,'[]',7,1),(15,'2026-04-17 02:49:37.087546','1','数据结构 / 绪论 / 栈',1,'[{\"added\": {}}]',10,1),(16,'2026-04-17 02:53:28.632895','1','[0101010001] 数据结构 / 绪论 / 栈 / 测试题目文本',1,'[{\"added\": {}}]',9,1),(17,'2026-04-17 02:58:11.660067','2','数据结构 / 线性表',2,'[{\"changed\": {\"fields\": [\"\\u987a\\u5e8f\\u53f7\"]}}]',7,1),(18,'2026-04-17 02:58:38.845318','2','数据结构 / 线性表',2,'[{\"changed\": {\"fields\": [\"\\u987a\\u5e8f\\u53f7\"]}}]',7,1),(19,'2026-04-17 02:58:42.006017','1','数据结构 / 绪论',2,'[{\"changed\": {\"fields\": [\"\\u987a\\u5e8f\\u53f7\"]}}]',7,1),(20,'2026-04-17 02:59:21.131736','1','数据结构 / 绪论',2,'[{\"changed\": {\"fields\": [\"\\u987a\\u5e8f\\u53f7\"]}}]',7,1),(21,'2026-04-17 04:04:05.274669','3','计算机组成原理 / 计算机系统概述',1,'[{\"added\": {}}]',7,1),(22,'2026-04-17 04:04:22.376432','4','计算机组成原理 / 数据的表示与运算',1,'[{\"added\": {}}]',7,1),(23,'2026-04-17 04:06:26.602148','1','数据结构 / 线性表 / 栈',2,'[{\"changed\": {\"fields\": [\"\\u6240\\u5c5e\\u7ae0\\u8282\"]}}]',10,1),(24,'2026-04-17 04:08:12.826101','1','数据结构',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u542f\\u7528\"]}}]',8,1),(25,'2026-04-17 04:08:21.584871','1','数据结构',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u542f\\u7528\"]}}]',8,1),(26,'2026-04-17 04:12:51.711524','2','[0102010002] 数据结构 / 线性表 / 栈 / 测试题干2',1,'[{\"added\": {}}]',9,1),(27,'2026-04-17 04:16:03.185631','1','数据结构 / 绪论',2,'[{\"changed\": {\"fields\": [\"\\u987a\\u5e8f\\u53f7\"]}}]',7,1),(28,'2026-04-17 04:16:49.486583','1','数据结构 / 绪论',2,'[{\"changed\": {\"fields\": [\"\\u987a\\u5e8f\\u53f7\"]}}]',7,1),(29,'2026-04-17 04:55:08.115988','2','数据结构 / 线性表 / 队列',1,'[{\"added\": {}}]',10,1),(30,'2026-04-17 08:42:42.654108','5','数据结构 / 图',1,'[{\"added\": {}}]',7,1),(31,'2026-04-17 09:05:56.196312','6','数据结构 / 树',1,'[{\"added\": {}}]',7,1),(32,'2026-04-17 09:06:11.208307','5','离散数学',1,'[{\"added\": {}}]',8,1),(33,'2026-04-17 09:20:00.894859','7','计算机组成原理 / 存储系统',1,'[{\"added\": {}}]',7,1),(34,'2026-04-22 09:01:28.304667','5','离散数学',3,'',8,1),(35,'2026-04-22 09:35:53.376831','3','数据结构 / 绪论 / 1',1,'[{\"added\": {}}]',10,1),(36,'2026-04-22 09:36:09.738727','3','[0101010001] 数据结构 / 绪论 / 1 / 1',1,'[{\"added\": {}}]',9,1),(37,'2026-04-23 06:28:55.703075','6','离散数学',1,'[{\"added\": {}}]',8,1),(38,'2026-04-23 07:53:05.934245','2','计算机组成原理',2,'[{\"changed\": {\"fields\": [\"\\u601d\\u7ef4\\u5bfc\\u56fe PDF\"]}}]',8,1),(39,'2026-04-23 07:53:38.427128','2','计算机组成原理',2,'[]',8,1),(40,'2026-04-23 08:28:43.647214','6','离散数学',3,'',8,1),(41,'2026-04-23 08:28:58.797745','1','数据结构',2,'[{\"changed\": {\"fields\": [\"\\u601d\\u7ef4\\u5bfc\\u56fe PDF\"]}}]',8,1),(42,'2026-04-23 08:29:13.890865','3','操作系统',2,'[{\"changed\": {\"fields\": [\"\\u601d\\u7ef4\\u5bfc\\u56fe PDF\"]}}]',8,1),(43,'2026-04-23 08:29:26.636316','4','计算机网络',2,'[{\"changed\": {\"fields\": [\"\\u601d\\u7ef4\\u5bfc\\u56fe PDF\"]}}]',8,1),(44,'2026-04-24 08:51:09.066541','4','计算机组成原理 / 计算机系统概述 / 1',1,'[{\"added\": {}}]',10,1),(45,'2026-04-24 08:51:33.374073','4','[0201010001] 计算机组成原理 / 计算机系统概述 / 1 / 1',1,'[{\"added\": {}}]',9,1),(46,'2026-04-24 14:46:44.894931','1','数据结构 / 绪论',3,'',7,1),(47,'2026-04-24 14:46:44.894931','2','数据结构 / 线性表',3,'',7,1),(48,'2026-04-24 14:46:44.894931','5','数据结构 / 图',3,'',7,1),(49,'2026-04-24 14:46:44.894931','6','数据结构 / 树',3,'',7,1),(50,'2026-04-24 14:46:44.894931','3','计算机组成原理 / 计算机系统概述',3,'',7,1),(51,'2026-04-24 14:46:44.894931','4','计算机组成原理 / 数据的表示与运算',3,'',7,1),(52,'2026-04-24 14:46:44.894931','7','计算机组成原理 / 存储系统',3,'',7,1),(53,'2026-04-24 14:46:58.537656','8','数据结构 / 绪论',1,'[{\"added\": {}}]',7,1),(54,'2026-04-24 14:47:05.770582','9','数据结构 / 线性表',1,'[{\"added\": {}}]',7,1),(55,'2026-04-24 14:47:18.317799','10','数据结构 / 栈、队列和数组',1,'[{\"added\": {}}]',7,1),(56,'2026-04-24 14:47:26.396623','11','数据结构 / 串',1,'[{\"added\": {}}]',7,1),(57,'2026-04-24 14:47:38.058222','12','数据结构 / 树与二叉树',1,'[{\"added\": {}}]',7,1),(58,'2026-04-24 14:47:42.587051','13','数据结构 / 图',1,'[{\"added\": {}}]',7,1),(59,'2026-04-24 14:47:50.192715','14','数据结构 / 查找',1,'[{\"added\": {}}]',7,1),(60,'2026-04-24 14:47:58.675617','15','数据结构 / 排序',1,'[{\"added\": {}}]',7,1),(61,'2026-04-24 14:48:34.043753','5','数据结构 / 绪论 / 数据结构的基本概念',1,'[{\"added\": {}}]',10,1),(62,'2026-04-24 14:48:44.350393','6','数据结构 / 绪论 / 算法和算法评价',1,'[{\"added\": {}}]',10,1),(63,'2026-04-24 14:48:59.594617','7','数据结构 / 线性表 / 线性表的定义和基本操作',1,'[{\"added\": {}}]',10,1),(64,'2026-04-24 14:49:14.405154','8','数据结构 / 线性表 / 线性表的顺序表示',1,'[{\"added\": {}}]',10,1),(65,'2026-04-24 14:49:26.211418','9','数据结构 / 线性表 / 线性表的链式表示',1,'[{\"added\": {}}]',10,1),(66,'2026-04-24 14:49:42.165538','10','数据结构 / 栈、队列和数组 / 栈',1,'[{\"added\": {}}]',10,1),(67,'2026-04-24 14:49:50.404920','11','数据结构 / 栈、队列和数组 / 队列',1,'[{\"added\": {}}]',10,1),(68,'2026-04-24 14:50:03.284210','12','数据结构 / 栈、队列和数组 / 栈和队列的应用',1,'[{\"added\": {}}]',10,1),(69,'2026-04-24 14:50:14.523908','13','数据结构 / 栈、队列和数组 / 数组和特殊矩阵',1,'[{\"added\": {}}]',10,1),(70,'2026-04-24 14:50:27.417484','14','数据结构 / 串 / 串的定义和实现',1,'[{\"added\": {}}]',10,1),(71,'2026-04-24 14:50:37.860147','15','数据结构 / 串 / 串的模式匹配',1,'[{\"added\": {}}]',10,1),(72,'2026-04-24 14:50:47.080632','16','数据结构 / 树与二叉树 / 树的基本概念',1,'[{\"added\": {}}]',10,1),(73,'2026-04-24 14:50:56.511815','17','数据结构 / 树与二叉树 / 二叉树的概念',1,'[{\"added\": {}}]',10,1),(74,'2026-04-24 14:51:18.691110','18','数据结构 / 树与二叉树 / 二叉树的遍历和线索二叉树',1,'[{\"added\": {}}]',10,1),(75,'2026-04-24 14:51:33.323349','19','数据结构 / 树与二叉树 / 树、森林',1,'[{\"added\": {}}]',10,1),(76,'2026-04-24 14:51:47.777650','20','数据结构 / 树与二叉树 / 树与二叉树的应用',1,'[{\"added\": {}}]',10,1),(77,'2026-04-24 14:51:58.408712','21','数据结构 / 图 / 图的基本概念',1,'[{\"added\": {}}]',10,1),(78,'2026-04-24 14:52:28.042239','22','数据结构 / 图 / 图的存储及基本操作',1,'[{\"added\": {}}]',10,1),(79,'2026-04-24 14:52:44.901105','23','数据结构 / 图 / 图的遍历',1,'[{\"added\": {}}]',10,1),(80,'2026-04-24 14:52:56.642738','24','数据结构 / 图 / 图的应用',1,'[{\"added\": {}}]',10,1),(81,'2026-04-24 14:53:06.807680','25','数据结构 / 查找 / 查找的基本概念',1,'[{\"added\": {}}]',10,1),(82,'2026-04-24 14:53:26.697766','26','数据结构 / 查找 / 顺序查找和折半查找',1,'[{\"added\": {}}]',10,1),(83,'2026-04-24 14:53:43.482153','27','数据结构 / 查找 / 树形查找',1,'[{\"added\": {}}]',10,1),(84,'2026-04-24 14:53:58.609823','28','数据结构 / 查找 / B树和B+树',1,'[{\"added\": {}}]',10,1),(85,'2026-04-24 14:54:11.995696','29','数据结构 / 查找 / 散列（Hash）表',1,'[{\"added\": {}}]',10,1),(86,'2026-04-24 14:54:26.823018','30','数据结构 / 排序 / 排序的基本概念',1,'[{\"added\": {}}]',10,1),(87,'2026-04-24 14:54:34.272293','31','数据结构 / 排序 / 插入排序',1,'[{\"added\": {}}]',10,1),(88,'2026-04-24 14:54:42.999899','32','数据结构 / 排序 / 交换排序',1,'[{\"added\": {}}]',10,1),(89,'2026-04-24 14:54:51.817483','33','数据结构 / 排序 / 选择排序',1,'[{\"added\": {}}]',10,1),(90,'2026-04-24 14:55:20.482067','34','数据结构 / 排序 / 归并排序、基数排序和计数排序',1,'[{\"added\": {}}]',10,1),(91,'2026-04-24 14:55:43.658890','35','数据结构 / 排序 / 各种内部排序算法的比较及应用',1,'[{\"added\": {}}]',10,1),(92,'2026-04-24 14:55:55.378160','36','数据结构 / 排序 / 外部排序',1,'[{\"added\": {}}]',10,1),(93,'2026-04-27 02:27:00.942562','5','[0109010001] 数据结构 / 第一章 线性表 / 1.1 顺序表 / 顺序表相较于链表的主要优点是？',3,'',9,1),(94,'2026-04-27 02:27:00.942562','6','[0109010002] 数据结构 / 第一章 线性表 / 1.1 顺序表 / 在长度为n的顺序表中删除第i个元素，需要',3,'',9,1),(95,'2026-04-27 02:27:00.942562','7','[0109010003] 数据结构 / 第一章 线性表 / 1.1 顺序表 / 线性表的链式存储结构与顺序存储结构相比，',3,'',9,1),(96,'2026-04-27 02:27:00.942562','10','[0110010001] 数据结构 / 第二章 栈和队列 / 2.1 栈 / 栈的特点是？',3,'',9,1),(97,'2026-04-27 02:27:00.942562','11','[0110010002] 数据结构 / 第二章 栈和队列 / 2.1 栈 / 一个栈的输入序列为1,2,3,4,5，以',3,'',9,1),(98,'2026-04-27 02:27:00.942562','12','[0401010001] 计算机网络 / 第一章 计算机网络体系结构 / 1.1 网络分层 / OSI参考模型分为几层？',3,'',9,1),(99,'2026-04-27 02:27:00.942562','13','[0401010002] 计算机网络 / 第一章 计算机网络体系结构 / 1.1 网络分层 / TCP/IP体系结构分为几层？',3,'',9,1),(100,'2026-04-27 02:27:00.942562','8','[0109020001] 数据结构 / 第一章 线性表 / 1.2 链表 / 单链表中每个结点至少包含什么域？',3,'',9,1),(101,'2026-04-27 02:27:00.942562','9','[0109020002] 数据结构 / 第一章 线性表 / 1.2 链表 / 设计一个算法，实现单链表的就地逆置（不允',3,'',9,1),(102,'2026-04-27 02:39:53.075007','8','计算机网络',1,'[{\"added\": {}}]',8,1),(103,'2026-04-27 02:39:57.921074','9','操作系统',1,'[{\"added\": {}}]',8,1),(104,'2026-04-27 02:40:02.961107','10','计算机网络',1,'[{\"added\": {}}]',8,1),(105,'2026-04-27 05:31:08.032669','5','Believer',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',4,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(11,'practice','practicerecord'),(12,'practice','practicesession'),(15,'practice','subchapterpracticeprogress'),(7,'question_bank','chapter'),(8,'question_bank','course'),(9,'question_bank','question'),(10,'question_bank','subchapter'),(16,'recommendation','wrongquestionreview'),(13,'records','favoritequestion'),(14,'records','wrongquestion'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-04-16 10:26:08.040272'),(2,'auth','0001_initial','2026-04-16 10:26:09.123428'),(3,'admin','0001_initial','2026-04-16 10:26:09.338513'),(4,'admin','0002_logentry_remove_auto_add','2026-04-16 10:26:09.347617'),(5,'admin','0003_logentry_add_action_flag_choices','2026-04-16 10:26:09.356291'),(6,'contenttypes','0002_remove_content_type_name','2026-04-16 10:26:09.502594'),(7,'auth','0002_alter_permission_name_max_length','2026-04-16 10:26:09.595780'),(8,'auth','0003_alter_user_email_max_length','2026-04-16 10:26:09.620280'),(9,'auth','0004_alter_user_username_opts','2026-04-16 10:26:09.628096'),(10,'auth','0005_alter_user_last_login_null','2026-04-16 10:26:09.706313'),(11,'auth','0006_require_contenttypes_0002','2026-04-16 10:26:09.710935'),(12,'auth','0007_alter_validators_add_error_messages','2026-04-16 10:26:09.720017'),(13,'auth','0008_alter_user_username_max_length','2026-04-16 10:26:09.814402'),(14,'auth','0009_alter_user_last_name_max_length','2026-04-16 10:26:09.910810'),(15,'auth','0010_alter_group_name_max_length','2026-04-16 10:26:09.934148'),(16,'auth','0011_update_proxy_permissions','2026-04-16 10:26:09.943506'),(17,'auth','0012_alter_user_first_name_max_length','2026-04-16 10:26:10.037719'),(18,'sessions','0001_initial','2026-04-16 10:26:10.092777'),(20,'question_bank','0001_initial','2026-04-16 12:05:03.775531'),(21,'question_bank','0002_alter_question_options_question_business_id','2026-04-17 06:37:17.969581'),(22,'practice','0001_init_practice_models','2026-04-22 05:04:15.710555'),(23,'records','0001_initial','2026-04-22 06:45:49.572942'),(24,'question_bank','0003_add_course_mindmap_pdf','2026-04-23 05:28:32.388325'),(25,'practice','0002_subchapterpracticeprogress','2026-04-24 06:20:41.133599'),(26,'recommendation','0001_initial','2026-04-27 02:56:53.046135');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3w0r215ajfx8gzowda01gss579nqjnnh','.eJxVjMEOwiAQBf-FsyHQLrB49N5vILCAVA0kpT0Z_9026UGvb2bemzm_rcVtPS1ujuzKJLv8bsHTM9UDxIev98ap1XWZAz8UftLOpxbT63a6fwfF97LXwUgiBByzhJgpk9YoVEqDCWjQqgyjhyjACosgUSOoNKAIfi8CZc0-X94-N5Q:1wDdeJ:J0bQauo0p8-fbJaXGhvBRrp06yDIOPB-xWlaYYLCX4Y','2026-05-01 07:29:59.588339'),('4zonma23yziyss6o3r2gxtoy4jv4w8zg','.eJxVjMEOwiAQBf-FsyHQLrB49N5vILCAVA0kpT0Z_9026UGvb2bemzm_rcVtPS1ujuzKJLv8bsHTM9UDxIev98ap1XWZAz8UftLOpxbT63a6fwfF97LXwUgiBByzhJgpk9YoVEqDCWjQqgyjhyjACosgUSOoNKAIfi8CZc0-X94-N5Q:1wHEYm:SUeD2Vn_CKEFM_lEByYel2cAuC30ygGUk_oQPTSdWZI','2026-05-11 05:31:08.052895'),('dsduicqm4js30kbut0owln702h4wga11','.eJxVjMEOwiAQBf-FsyHQLrB49N5vILCAVA0kpT0Z_9026UGvb2bemzm_rcVtPS1ujuzKJLv8bsHTM9UDxIev98ap1XWZAz8UftLOpxbT63a6fwfF97LXwUgiBByzhJgpk9YoVEqDCWjQqgyjhyjACosgUSOoNKAIfi8CZc0-X94-N5Q:1wDKMR:muBebN4R92PClUrHnv38QrbisYIVWoehck27vESzU_M','2026-04-30 10:54:15.668953'),('hidwp2jat241t0vhhona9sp4bgllmo9t','.eJxVjMEOwiAQBf-FsyHQLrB49N5vILCAVA0kpT0Z_9026UGvb2bemzm_rcVtPS1ujuzKJLv8bsHTM9UDxIev98ap1XWZAz8UftLOpxbT63a6fwfF97LXwUgiBByzhJgpk9YoVEqDCWjQqgyjhyjACosgUSOoNKAIfi8CZc0-X94-N5Q:1wDe0c:T322ZZzSvkijOLCrDjOk78Jqesu9Sc3d3cOWe4hwbWo','2026-05-01 07:53:02.107178');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorite_questions`
--

DROP TABLE IF EXISTS `favorite_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorite_questions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `question_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_favorite_question` (`user_id`,`question_id`),
  KEY `favorite_questions_question_id_f5c7f326_fk_question_` (`question_id`),
  CONSTRAINT `favorite_questions_question_id_f5c7f326_fk_question_` FOREIGN KEY (`question_id`) REFERENCES `question_bank_question` (`id`),
  CONSTRAINT `favorite_questions_user_id_ccd6e394_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorite_questions`
--

LOCK TABLES `favorite_questions` WRITE;
/*!40000 ALTER TABLE `favorite_questions` DISABLE KEYS */;
INSERT INTO `favorite_questions` VALUES (3,'2026-04-28 02:54:02.177592',39,1),(4,'2026-04-28 02:54:04.639520',40,1),(5,'2026-04-28 02:54:08.319869',41,1);
/*!40000 ALTER TABLE `favorite_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `practice_record`
--

DROP TABLE IF EXISTS `practice_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `practice_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_answer` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_correct` tinyint(1) DEFAULT NULL,
  `is_answered` tinyint(1) NOT NULL,
  `answer_mode` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `answered_at` datetime(6) NOT NULL,
  `question_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `session_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_session_question_record` (`session_id`,`question_id`),
  KEY `practice_re_user_id_ea46a6_idx` (`user_id`,`question_id`),
  KEY `practice_re_session_8a9920_idx` (`session_id`,`question_id`),
  KEY `practice_record_question_id_c1b8d257_fk_question_` (`question_id`),
  CONSTRAINT `practice_record_question_id_c1b8d257_fk_question_` FOREIGN KEY (`question_id`) REFERENCES `question_bank_question` (`id`),
  CONSTRAINT `practice_record_session_id_81d4596d_fk_practice_session_id` FOREIGN KEY (`session_id`) REFERENCES `practice_session` (`id`),
  CONSTRAINT `practice_record_user_id_11430e45_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `practice_record`
--

LOCK TABLES `practice_record` WRITE;
/*!40000 ALTER TABLE `practice_record` DISABLE KEYS */;
INSERT INTO `practice_record` VALUES (51,'C',1,1,'single_choice','2026-04-27 02:41:14.782106',39,1,56),(52,'C',0,1,'single_choice','2026-04-27 02:41:26.154670',40,1,56),(53,'C',1,1,'single_choice','2026-04-27 02:41:41.124801',41,1,56),(54,'C',1,1,'single_choice','2026-04-27 02:41:53.492856',42,1,56),(55,'D',1,1,'single_choice','2026-04-27 02:42:02.555727',43,1,56),(56,'B',1,1,'single_choice','2026-04-27 02:42:21.796398',44,1,56),(57,'D',0,1,'single_choice','2026-04-27 02:42:42.808629',45,1,56),(58,'A',0,1,'single_choice','2026-04-27 02:43:06.238631',46,1,56),(59,'D',1,1,'single_choice','2026-04-27 02:43:26.667653',47,1,56),(60,'B',1,1,'single_choice','2026-04-27 02:43:39.665847',48,1,56),(61,'B',0,1,'single_choice','2026-04-27 05:29:19.396052',39,2,60),(62,'D',0,1,'single_choice','2026-04-27 05:29:22.283570',40,2,60),(63,'C',1,1,'single_choice','2026-04-27 05:29:25.553908',41,2,60),(64,'D',0,1,'single_choice','2026-04-27 05:29:28.274306',42,2,60),(65,'D',1,1,'single_choice','2026-04-27 05:29:30.282786',43,2,60),(66,'C',0,1,'single_choice','2026-04-27 05:29:32.913399',44,2,60),(67,'D',0,1,'single_choice','2026-04-27 05:29:36.380094',45,2,60),(68,'C',0,1,'single_choice','2026-04-27 05:29:39.366234',46,2,60),(69,'D',1,1,'single_choice','2026-04-27 05:29:41.667630',47,2,60),(70,'B',1,1,'single_choice','2026-04-27 05:29:44.483619',48,2,60),(71,'D',0,1,'single_choice','2026-04-27 05:31:17.812777',39,5,61),(72,'D',0,1,'single_choice','2026-04-27 05:31:20.107797',40,5,61),(73,'D',0,1,'single_choice','2026-04-27 05:31:22.530011',41,5,61),(74,'D',0,1,'single_choice','2026-04-27 05:31:25.075677',42,5,61),(75,'D',1,1,'single_choice','2026-04-27 05:31:26.955126',43,5,61),(76,'D',0,1,'single_choice','2026-04-27 05:31:29.493274',44,5,61),(77,'D',0,1,'single_choice','2026-04-27 05:31:32.620884',45,5,61),(78,'D',0,1,'single_choice','2026-04-27 05:31:35.051362',46,5,61),(79,'D',1,1,'single_choice','2026-04-27 05:31:37.214577',47,5,61),(80,'D',0,1,'single_choice','2026-04-27 05:31:40.131919',48,5,61),(81,'B',0,1,'single_choice','2026-04-28 02:51:09.691339',64,1,63),(82,'D',0,1,'single_choice','2026-04-28 02:51:12.043427',65,1,63),(83,'B',0,1,'single_choice','2026-04-28 02:51:23.581055',66,1,63),(84,'A',1,1,'single_choice','2026-04-28 02:51:35.660426',67,1,63),(85,'C',1,1,'single_choice','2026-04-28 02:52:23.326910',39,1,65),(86,'B',0,1,'single_choice','2026-04-28 02:52:26.714763',40,1,65),(87,'D',0,1,'single_choice','2026-04-28 02:52:29.270190',41,1,65),(88,'C',1,1,'single_choice','2026-04-28 02:52:32.347172',42,1,65),(89,'C',0,1,'single_choice','2026-04-28 02:52:35.533497',43,1,65),(90,'B',1,1,'single_choice','2026-04-28 02:52:40.317884',44,1,65),(91,'B',1,1,'single_choice','2026-04-28 02:52:46.227765',45,1,65),(92,'B',1,1,'single_choice','2026-04-28 02:52:52.053949',46,1,65),(93,'D',1,1,'single_choice','2026-04-28 02:52:56.860989',47,1,65),(94,'B',1,1,'single_choice','2026-04-28 02:53:00.908883',48,1,65),(95,'A',1,1,'single_choice','2026-04-28 06:55:48.694179',40,1,68);
/*!40000 ALTER TABLE `practice_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `practice_session`
--

DROP TABLE IF EXISTS `practice_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `practice_session` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_count` int unsigned NOT NULL,
  `answered_count` int unsigned NOT NULL,
  `correct_count` int unsigned NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `started_at` datetime(6) NOT NULL,
  `finished_at` datetime(6) DEFAULT NULL,
  `subchapter_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `practice_se_user_id_30c788_idx` (`user_id`,`status`),
  KEY `practice_se_user_id_56a303_idx` (`user_id`,`subchapter_id`),
  KEY `practice_session_subchapter_id_4bcbe6f2_fk_question_` (`subchapter_id`),
  CONSTRAINT `practice_session_subchapter_id_4bcbe6f2_fk_question_` FOREIGN KEY (`subchapter_id`) REFERENCES `question_bank_subchapter` (`id`),
  CONSTRAINT `practice_session_user_id_e7a76d73_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `practice_session_chk_1` CHECK ((`total_count` >= 0)),
  CONSTRAINT `practice_session_chk_2` CHECK ((`answered_count` >= 0)),
  CONSTRAINT `practice_session_chk_3` CHECK ((`correct_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `practice_session`
--

LOCK TABLES `practice_session` WRITE;
/*!40000 ALTER TABLE `practice_session` DISABLE KEYS */;
INSERT INTO `practice_session` VALUES (56,10,10,7,'finished','2026-04-27 02:41:10.152890','2026-04-27 02:43:40.613126',41,1),(57,10,10,7,'finished','2026-04-27 03:31:47.395837','2026-04-27 03:31:48.736611',41,1),(58,10,0,0,'finished','2026-04-27 05:25:51.349150','2026-04-27 05:26:10.406559',41,2),(59,10,0,0,'in_progress','2026-04-27 05:26:11.661232',NULL,41,2),(60,10,10,4,'finished','2026-04-27 05:26:22.019852','2026-04-27 05:29:45.781509',41,2),(61,10,10,2,'finished','2026-04-27 05:31:15.357741','2026-04-27 05:31:41.108956',41,5),(62,10,10,7,'finished','2026-04-27 05:47:21.078322','2026-04-27 05:48:00.189597',41,1),(63,24,4,1,'finished','2026-04-28 02:51:06.876067','2026-04-28 02:51:40.689365',43,1),(64,10,10,7,'finished','2026-04-28 02:52:10.323415','2026-04-28 02:52:17.018834',41,1),(65,10,10,7,'finished','2026-04-28 02:52:20.745710','2026-04-28 02:53:01.743328',41,1),(66,10,10,7,'finished','2026-04-28 02:53:53.107163','2026-04-28 02:54:10.433310',41,1),(67,10,10,7,'in_progress','2026-04-28 06:47:43.672590',NULL,41,1),(68,10,1,1,'in_progress','2026-04-28 06:52:55.372873',NULL,41,1),(69,10,10,7,'in_progress','2026-04-28 06:55:10.829603',NULL,41,1);
/*!40000 ALTER TABLE `practice_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_bank_chapter`
--

DROP TABLE IF EXISTS `question_bank_chapter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_bank_chapter` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` int unsigned NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `course_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_course_order_no` (`course_id`,`order_no`),
  UNIQUE KEY `unique_course_chapter` (`course_id`,`name`),
  CONSTRAINT `question_bank_chapte_course_id_97358b38_fk_question_` FOREIGN KEY (`course_id`) REFERENCES `question_bank_course` (`id`),
  CONSTRAINT `question_bank_chapter_chk_1` CHECK ((`order_no` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_bank_chapter`
--

LOCK TABLES `question_bank_chapter` WRITE;
/*!40000 ALTER TABLE `question_bank_chapter` DISABLE KEYS */;
INSERT INTO `question_bank_chapter` VALUES (19,1,'绪论',1,'2026-04-27 02:37:54.931189','2026-04-27 02:37:54.931189',7),(20,2,'线性表',1,'2026-04-27 02:37:54.990114','2026-04-27 02:37:54.990114',7);
/*!40000 ALTER TABLE `question_bank_chapter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_bank_course`
--

DROP TABLE IF EXISTS `question_bank_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_bank_course` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` int unsigned NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `mindmap_pdf` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  CONSTRAINT `question_bank_course_chk_1` CHECK ((`order_no` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_bank_course`
--

LOCK TABLES `question_bank_course` WRITE;
/*!40000 ALTER TABLE `question_bank_course` DISABLE KEYS */;
INSERT INTO `question_bank_course` VALUES (7,1,'数据结构',1,'2026-04-27 02:37:54.926651','2026-04-27 02:37:54.926651',''),(8,4,'计算机网络',1,'2026-04-27 02:39:53.074005','2026-04-27 02:39:53.074005',''),(9,5,'操作系统',1,'2026-04-27 02:39:57.920067','2026-04-27 02:39:57.920067',''),(10,6,'计算机网络',1,'2026-04-27 02:40:02.958643','2026-04-27 02:40:02.958643','');
/*!40000 ALTER TABLE `question_bank_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_bank_question`
--

DROP TABLE IF EXISTS `question_bank_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_bank_question` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` int unsigned NOT NULL,
  `question_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `stem_text` longtext COLLATE utf8mb4_unicode_ci,
  `stem_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `option_a_text` longtext COLLATE utf8mb4_unicode_ci,
  `option_a_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `option_b_text` longtext COLLATE utf8mb4_unicode_ci,
  `option_b_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `option_c_text` longtext COLLATE utf8mb4_unicode_ci,
  `option_c_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `option_d_text` longtext COLLATE utf8mb4_unicode_ci,
  `option_d_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `correct_answer` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `analysis_text` longtext COLLATE utf8mb4_unicode_ci,
  `analysis_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `subchapter_id` bigint NOT NULL,
  `business_id` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_subchapter_order_no` (`subchapter_id`,`order_no`),
  CONSTRAINT `question_bank_questi_subchapter_id_3a7e76b3_fk_question_` FOREIGN KEY (`subchapter_id`) REFERENCES `question_bank_subchapter` (`id`),
  CONSTRAINT `question_bank_question_chk_1` CHECK ((`order_no` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_bank_question`
--

LOCK TABLES `question_bank_question` WRITE;
/*!40000 ALTER TABLE `question_bank_question` DISABLE KEYS */;
INSERT INTO `question_bank_question` VALUES (39,1,'single_choice','数据是对客观事物的符号表示，在计算机科学中是指所有能输入到计算机中并被计算机程序处理的符号的总称。下列不属于数据的是？','','整数','','图像','','路由器','','声音','','C','数据是计算机程序的输入对象，包括数值、字符、图像、声音等多种形式。路由器是物理设备，不是符号化的数据表示。','',1,'2026-04-27 02:37:54.941000','2026-04-27 02:37:54.941000',41,'0101010001'),(40,2,'single_choice','数据元素是数据的基本单位，在计算机程序中通常作为一个整体进行考虑和处理。一个数据元素可以由若干个数据项组成，下列说法正确的是？','','数据项是数据的最小单位，不可再分','','数据项是数据的最大单位','','数据项可以由更小的数据项组成','','数据项和数据元素是同一个概念','','A','数据项是构成数据元素的不可分割的最小单位，是数据的最小单位。数据元素是数据的基本单位，而数据项是数据元素的组成部分。','',1,'2026-04-27 02:37:54.942037','2026-04-27 02:37:54.942037',41,'0101010002'),(41,3,'single_choice','数据结构是指相互之间存在一种或多种特定关系的数据元素的集合。在讨论数据结构时，通常关注的是？','','数据的值','','数据的存储介质','','数据元素之间的关系','','数据的输入设备','','C','数据结构关注的是数据元素之间的逻辑关系、存储关系及其操作，不关注数据的具体值或存储介质。','',1,'2026-04-27 02:37:54.943039','2026-04-27 02:37:54.943039',41,'0101010003'),(42,4,'single_choice','数据的逻辑结构是指数据元素之间的逻辑关系，与存储结构无关。下列属于逻辑结构的是？','','顺序结构','','链式结构','','集合','','散列结构','','C','集合是一种逻辑结构，表示数据元素属于同一集合，元素之间无其他关系。顺序结构、链式结构、散列结构属于存储结构（物理结构）。','',1,'2026-04-27 02:37:54.944803','2026-04-27 02:37:54.944803',41,'0101010004'),(43,5,'single_choice','数据的物理结构是指数据结构在计算机中的表示（又称存储结构）。下列不属于物理结构的是？','','顺序存储结构','','链式存储结构','','索引存储结构','','树形结构','','D','树形结构是一种逻辑结构，描述数据元素之间的层次关系。顺序存储、链式存储、索引存储都是物理结构（存储结构）。','',1,'2026-04-27 02:37:54.947326','2026-04-27 02:37:54.947326',41,'0101010005'),(44,6,'single_choice','在数据结构中，算法与数据结构的关系是？','','算法和数据结构是独立的','','算法的设计依赖于数据的结构','','数据的结构决定了算法的选择','','两者没有任何关系','','B','算法是建立在特定数据结构基础上的。数据结构的选择会影响算法的效率，同样的问题在不同数据结构上可能需要不同的算法来解决。','',1,'2026-04-27 02:37:54.948339','2026-04-27 02:37:54.948339',41,'0101010006'),(45,7,'single_choice','以下关于数据结构的说法，错误的是？','','数据结构包括逻辑结构和物理结构','','线性结构是一种非线性结构','','树形结构和图形结构都是非线性结构','','集合结构中的元素之间没有顺序关系','','B','线性结构是一种有线性关系（非非线性）的结构，树形结构和图形结构才是非线性结构。选项B的表述自相矛盾。','',1,'2026-04-27 02:37:54.951022','2026-04-27 02:37:54.951022',41,'0101010007'),(46,8,'single_choice','线性结构的特点是？','','存在唯一一个无前驱的元素和唯一一个无后继的元素','','所有元素都有且仅有一个前驱和后继','','元素之间是一对多的关系','','元素之间没有任何约束关系','','B','线性结构中，元素之间存在一对一的关系，除了第一个元素无前驱和最后一个元素无后继外，其余元素都有且仅有一个前驱和一个后继。','',1,'2026-04-27 02:37:54.952477','2026-04-27 02:37:54.952477',41,'0101010008'),(47,9,'single_choice','非线性结构中，各数据元素不再保持线性关系。下列属于非线性结构的是？','','栈','','队列','','线性表','','树','','D','树是一种非线性结构，数据元素之间存在一对多的层次关系。栈、队列、线性表都是线性结构。','',1,'2026-04-27 02:37:54.952477','2026-04-27 02:37:54.952477',41,'0101010009'),(48,10,'single_choice','数据的存储结构（物理结构）是逻辑结构在计算机中的映射。以下哪种存储结构通过计算元素地址实现随机访问？','','链式存储','','顺序存储','','索引存储','','散列存储','','B','顺序存储结构使用连续的存储单元，通过元素首地址和元素序号可以计算出任意元素的存储地址，实现O(1)的随机访问。','',1,'2026-04-27 02:37:54.954969','2026-04-27 02:37:54.954969',41,'0101010010'),(49,1,'single_choice','算法是对特定问题求解步骤的一种描述，是指令的有限序列。下列关于算法的特性，说法错误的是？','','有穷性：算法必须在执行有限步后结束','','确定性：算法的每一条指令都有确定的含义','','可行性：算法中的操作都可以通过已经实现的基本运算执行有限次来完成','','输入：算法必须至少有一个输入','','D','算法可以有零个或多个输入，但必须至少有一个输出。算法是对输入的处理，没有输入时也可以是一个正确的算法。','',1,'2026-04-27 02:37:54.965229','2026-04-27 02:37:54.965229',42,'0101020001'),(50,2,'single_choice','一个算法的时间复杂度为T(n)=3n³+2n²+n+5，用大O记号表示，该算法的时间复杂度为？','','O(n³)','','O(n⁴)','','O(n²)','','O(3n³)','','A','大O记号只保留最高次幂项，且系数省略。3n³+2n²+n+5的最高次幂是n³，所以时间复杂度为O(n³)。','',1,'2026-04-27 02:37:54.967275','2026-04-27 02:37:54.967275',42,'0101020002'),(51,3,'single_choice','设n为问题规模，以下哪个时间复杂度的算法运行速度最快？','','O(2ⁿ)','','O(n!)','','O(n²)','','O(n log n)','','D','当n较大时，各时间复杂度的增长速度：O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)。O(n log n)最快。','',1,'2026-04-27 02:37:54.968526','2026-04-27 02:37:54.968526',42,'0101020003'),(52,4,'single_choice','下面程序段的时间复杂度是？\nfor(i=0;i<n;i++)\n  for(j=0;j<n;j++)\n    a[i][j]=i*j;','','O(n)','','O(n²)','','O(n³)','','O(2ⁿ)','','B','外层循环执行n次，内层循环也执行n次，总执行次数为n×n=n²次，所以时间复杂度为O(n²)。','',1,'2026-04-27 02:37:54.969791','2026-04-27 02:37:54.969791',42,'0101020004'),(53,5,'single_choice','下面程序段的时间复杂度是？\ni=1;\nwhile(i<=n)\n  i=i*2;','','O(n)','','O(log₂n)','','O(n log n)','','O(n²)','','B','设循环执行k次后i>n，即2ᵏ>n，k>log₂n，所以时间复杂度为O(log₂n)。','',1,'2026-04-27 02:37:54.972103','2026-04-27 02:37:54.972103',42,'0101020005'),(54,6,'single_choice','算法的空间复杂度是指？','','算法源程序所占用的存储空间','','算法执行过程中所需存储空间的度量','','算法输入数据所占用的存储空间','','算法输出结果所占用的存储空间','','B','空间复杂度是算法执行过程中所需存储空间的度量，包括算法本身所占空间、输入/输出数据所占空间以及临时工作区所占空间。','',1,'2026-04-27 02:37:54.973124','2026-04-27 02:37:54.973124',42,'0101020006'),(55,7,'single_choice','设某算法完成某功能所需时间为T(n)=1000n+1000n²+10⁶，当n很大时，该算法的时间复杂度约为？','','O(1000n²)','','O(n²)','','O(n)','','O(10⁶)','','B','当n很大时，最高次幂项起主导作用。n²项的增长速度远大于n项，所以时间复杂度约为O(n²)，系数1000在大O记号中省略。','',1,'2026-04-27 02:37:54.974126','2026-04-27 02:37:54.974126',42,'0101020007'),(56,8,'single_choice','下面程序段的时间复杂度是？\nfor(i=0;i<n;i++)\n  for(j=i;j<n;j++)\n    s++;','','O(n)','','O(n²)','','O(n³)','','O(n log n)','','B','外层循环执行n次，当i=0时内层执行n次，i=1时执行n-1次，...，总执行次数为n+(n-1)+...+1=n(n+1)/2，时间复杂度为O(n²)。','',1,'2026-04-27 02:37:54.976980','2026-04-27 02:37:54.976980',42,'0101020008'),(57,9,'single_choice','递归算法的时间复杂度通常用什么方法分析？','','直接计数法','','主定理法','','顺序查找法','','枚举法','','B','递归算法通常使用主定理（Master Theorem）或递归树来分析时间复杂度。对于形如T(n)=aT(n/b)+f(n)的递归式，主定理可以快速求解。','',1,'2026-04-27 02:37:54.977990','2026-04-27 02:37:54.977990',42,'0101020009'),(58,10,'single_choice','下列哪个不是评价算法优劣的主要标准？','','正确性','','可读性','','代码长度','','时间复杂度','','C','评价算法的主要标准包括：正确性、可读性、健壮性、时间复杂度和空间复杂度。代码长度不是评价算法优劣的标准。','',1,'2026-04-27 02:37:54.978995','2026-04-27 02:37:54.978995',42,'0101020010'),(59,11,'single_choice','设两个n×n矩阵相乘的算法需要n³次乘法运算，则该算法的时间复杂度为？','','O(n)','','O(n²)','','O(n³)','','O(2ⁿ)','','C','矩阵相乘需要进行n³次基本乘法运算，随着n的增长，起主导作用的是n³项，所以时间复杂度为O(n³)。','',1,'2026-04-27 02:37:54.981087','2026-04-27 02:37:54.981087',42,'0101020011'),(60,12,'single_choice','在分析算法复杂度时，通常考虑的是？','','最优情况','','最坏情况','','平均情况','','所有情况都要精确计算','','B','分析算法复杂度时，通常考虑最坏情况的时间复杂度，因为它给出了算法运行时间的上界，是最常用的度量标准。','',1,'2026-04-27 02:37:54.983615','2026-04-27 02:37:54.983615',42,'0101020012'),(61,13,'single_choice','折半查找（二分查找）的时间复杂度是？','','O(n)','','O(1)','','O(log n)','','O(n²)','','C','折半查找每次将搜索范围缩小一半，需要log₂n次比较才能找到目标或确定不存在，所以时间复杂度为O(log n)。','',1,'2026-04-27 02:37:54.983615','2026-04-27 02:37:54.983615',42,'0101020013'),(62,14,'single_choice','下面程序段的时间复杂度是？\ncount=0;\nfor(k=1;k<n;k*=2)\n  for(j=1;j<n;j++)\n    count++;','','O(n)','','O(n log n)','','O(n²)','','O(log n)','','B','外层循环执行log₂n次（因为k每次翻倍），内层循环执行n次，总执行次数为n×log₂n，时间复杂度为O(n log n)。','',1,'2026-04-27 02:37:54.985639','2026-04-27 02:37:54.985639',42,'0101020014'),(63,15,'single_choice','一个算法的空间复杂度为O(1)时，表示？','','算法不占用任何空间','','算法占用的空间大小与问题规模无关','','算法只需要一个存储单元','','算法的存储空间为1字节','','B','空间复杂度O(1)表示算法所需的额外空间是常数级别的，与问题规模n无关，称为原地工作或常量空间复杂度。','',1,'2026-04-27 02:37:54.987247','2026-04-27 02:37:54.987247',42,'0101020015'),(64,1,'single_choice','线性表是最基本、最简单、也是最常用的一种数据结构。线性表中的数据元素之间的关系是？','','一对一','','一对多','','多对一','','多对多','','A','线性表是n个具有相同特性的数据元素的有序序列，元素之间存在一对一的关系。','',1,'2026-04-27 02:37:55.003528','2026-04-27 02:37:55.003528',43,'0102010001'),(65,2,'single_choice','一个线性表是n个数据元素的有序集合。下列关于线性表长度的说法，正确的是？','','线性表的长度是固定不变的','','线性表的长度可以动态变化','','线性表的长度等于数组的大小','','线性表的长度必须为正数','','B','线性表的长度可以根据插入和删除操作动态变化，这是线性表与固定大小数组的区别之一。','',1,'2026-04-27 02:37:55.006043','2026-04-27 02:37:55.006043',43,'0102010002'),(66,3,'single_choice','线性表的ADT（抽象数据类型）定义中，不包括以下哪个操作？','','InitList(&L)：初始化线性表','','DestroyList(&L)：销毁线性表','','SortList(&L)：对线性表进行排序','','ListEmpty(L)：判断线性表是否为空','','C','线性表的基本ADT操作包括初始化、销毁、判空、求长度等，排序不是线性表的基本ADT操作，是基于基本操作的应用。','',1,'2026-04-27 02:37:55.006725','2026-04-27 02:37:55.006725',43,'0102010003'),(67,4,'single_choice','顺序存储结构 和 链式存储结构 是线性表的两种主要存储方式。以下关于两者优缺点的比较，说法正确的是？','','顺序存储查找快，链式存储插入删除快','','顺序存储插入删除快，链式存储查找快','','两者查找和插入删除速度相同','','顺序存储比链式存储节省空间','','A','顺序存储支持随机访问，查找效率高，但插入删除需要移动元素效率低；链式存储插入删除只需修改指针，但查找需要遍历效率低。','',1,'2026-04-27 02:37:55.007733','2026-04-27 02:37:55.007733',43,'0102010004'),(68,5,'single_choice','线性表的链式存储结构中，每个结点包含数据域和指针域。关于指针域的说法，正确的是？','','单链表的每个结点只有一个指针，指向直接后继','','单链表的每个结点有两个指针，分别指向前后结点','','双向链表的每个结点有三个指针','','循环链表的指针指向任意结点','','A','单链表的每个结点只有一个指针域，指向其后继结点；双链表才有前后两个指针；循环链表的尾结点指针指向头结点。','',1,'2026-04-27 02:37:55.009909','2026-04-27 02:37:55.009909',43,'0102010005'),(69,6,'single_choice','在长度为n的线性表末尾添加一个新元素，其时间复杂度为？','','O(1)','','O(n)','','O(n²)','','O(log n)','','B','顺序表需要先判断存储空间是否已满，然后直接在末尾添加。在链表中，如果已经知道尾指针，可以在O(1)内完成；如果需要遍历到尾部，则为O(n)。','',1,'2026-04-27 02:37:55.010913','2026-04-27 02:37:55.010913',43,'0102010006'),(70,7,'single_choice','带头结点的单链表与不带头结点的单链表相比，优点是？','','插入和删除操作更加统一，不需要特殊处理','','可以节省存储空间','','访问第一个元素更快','','不需要存储头指针','','A','带头结点的单链表在插入第一个结点和删除第一个结点时不需要特殊处理，使操作更加统一、简便。','',1,'2026-04-27 02:37:55.013265','2026-04-27 02:37:55.013265',43,'0102010007'),(71,8,'single_choice','循环单链表是一种特殊的单链表，其特点是？','','最后一个结点的指针指向头结点，形成环','','所有结点的指针都指向头结点','','头结点指向尾结点','','表中所有数据元素相同','','A','循环单链表的尾结点指针不为NULL，而是指向头结点，形成一个环。这样可以从任意结点出发访问到所有其他结点。','',1,'2026-04-27 02:37:55.014777','2026-04-27 02:37:55.014777',43,'0102010008'),(72,9,'single_choice','双向链表与单链表相比，每个结点多了一个什么？','','数据域','','前驱指针','','后继指针','','长度信息','','B','双向链表的每个结点除了有后继指针外，还增加了一个前驱指针（prior），可以方便地找到前驱结点，实现双向遍历。','',1,'2026-04-27 02:37:55.016510','2026-04-27 02:37:55.016510',43,'0102010009'),(73,10,'single_choice','线性表的基本特点不包括？','','存在唯一的一个被称作\"第一个\"的元素','','存在唯一的一个被称作\"最后一个\"的元素','','除第一个元素外，每个元素都有且仅有一个前驱元素','','所有元素的值必须互不相同','','D','线性表中的元素值可以相同，线性表的基本特点只要求元素之间有前驱后继的顺序关系，不限制元素的取值是否相同。','',1,'2026-04-27 02:37:55.018012','2026-04-27 02:37:55.018012',43,'0102010010'),(74,11,'single_choice','对于顺序存储的线性表，其存储地址的特点是？','','所有元素存储地址不连续','','元素按链表形式存储','','所有元素存储地址连续','','元素可以分散存储','','C','顺序存储的线性表使用一段连续的存储单元依次存储表中元素，因此所有元素的存储地址是连续的。','',1,'2026-04-27 02:37:55.019035','2026-04-27 02:37:55.019035',43,'0102010011'),(75,12,'single_choice','静态链表是用数组描述的链表，关于静态链表的说法，正确的是？','','静态链表的结点不需要指针域','','静态链表不需要头结点','','静态链表的存储空间是动态分配的','','静态链表只能用于整型数据','','A','静态链表用数组的下标代替指针域来模拟链表，每个结点包含数据域和下一个结点的下标，不需要显式指针，但本质仍是链表结构。','',1,'2026-04-27 02:37:55.029191','2026-04-27 02:37:55.029191',43,'0102010012'),(76,13,'single_choice','线性表采用链式存储时，其存储密度？','','等于1','','小于1','','大于1','','无法确定','','B','存储密度是指数据元素本身占用的存储空间与整个存储空间的比例。链式存储需要额外的指针空间，所以存储密度小于1；顺序存储密度等于1。','',1,'2026-04-27 02:37:55.031251','2026-04-27 02:37:55.031251',43,'0102010013'),(77,14,'single_choice','若线性表最常用的操作是取第i个元素和删除最后一个元素，则以下存储方式中使用时间复杂度最低的是？','','单链表','','双链表','','顺序表','','循环双链表','','C','取第i个元素顺序表是O(1)，单链表是O(n)；删除最后一个元素顺序表是O(1)，单链表需要遍历到倒数第二个结点是O(n)。综合来看顺序表最优。','',1,'2026-04-27 02:37:55.033981','2026-04-27 02:37:55.033981',43,'0102010014'),(78,15,'single_choice','在双向循环链表中，已知指针p指向某个结点，则获取其前驱结点的时间复杂度为？','','O(1)','','O(n)','','O(n²)','','O(log n)','','A','双向循环链表的每个结点都包含指向前驱的指针，因此从p直接获取前驱结点的时间复杂度为O(1)。','',1,'2026-04-27 02:37:55.036655','2026-04-27 02:37:55.036655',43,'0102010015'),(79,16,'single_choice','线性表的顺序存储结构优于链式存储结构的主要场合是？','','需要进行频繁的插入和删除操作时','','需要频繁随机访问元素时','','表中元素个数变化很大时','','需要动态分配存储空间时','','B','顺序存储结构支持O(1)的随机访问，适合需要频繁按位置访问元素的场合。链式存储更适合插入删除频繁但访问需求较少的场合。','',1,'2026-04-27 02:37:55.038791','2026-04-27 02:37:55.038791',43,'0102010016'),(80,17,'single_choice','对于双向链表，以下哪个操作的时间复杂度最低？','','在p结点之后插入新结点','','删除p结点','','在p结点之前插入新结点','','遍历整个链表','','A','在p结点之后插入新结点：O(1)；删除p结点需要修改前驱和后继指针：O(1)；在p结点之前插入需要先找到前驱：O(1)（因为双向链表）；遍历：O(n)。在p结点之后插入相对最简单。','',1,'2026-04-27 02:37:55.039821','2026-04-27 02:37:55.039821',43,'0102010017'),(81,18,'single_choice','单链表的存储密度为？','','1','','小于1','','大于1','','等于0','','B','单链表的存储密度=数据元素占用的存储空间/(数据元素占用的存储空间+指针占用的存储空间)，由于需要额外的指针域，存储密度小于1。','',1,'2026-04-27 02:37:55.041359','2026-04-27 02:37:55.041359',43,'0102010018'),(82,19,'single_choice','在长度为n的顺序表中，在第i个位置插入一个元素，需要移动的元素个数是？','','i','','n-i','','n-i+1','','n-i-1','','C','在第i个位置插入元素，需要将第i到第n个元素（共n-i+1个元素）向后移动一位。','',1,'2026-04-27 02:37:55.042976','2026-04-27 02:37:55.042976',43,'0102010019'),(83,20,'single_choice','线性表的链式存储结构中，头指针和头结点的区别是？','','头指针指向第一个数据结点，头结点是附加结点','','两者没有区别','','头结点指向第一个数据结点，头指针是附加结点','','头指针是数据结点，头结点是指针','','A','头指针是指向第一个结点的指针；头结点是附加在第一个数据结点之前的结点，其指针指向第一个数据结点。头结点不是数据结点。','',1,'2026-04-27 02:37:55.045081','2026-04-27 02:37:55.045081',43,'0102010020'),(84,21,'single_choice','循环双链表与双链表的主要区别是？','','循环双链表的尾结点指针指向头结点','','循环双链表没有头结点','','循环双链表只能从头结点开始访问','','循环双链表不支持双向遍历','','A','循环双链表的尾结点（prior）指向头结点（或最后一个结点），头结点（next）指向尾结点，形成双向循环。普通双链表的尾结点指针为NULL。','',1,'2026-04-27 02:37:55.051811','2026-04-27 02:37:55.051811',43,'0102010021'),(85,22,'single_choice','对于线性表的顺序存储结构，以下说法错误的是？','','可以随机访问任意位置的元素','','存储空间在初始化时需要预先分配','','插入和删除操作的时间复杂度为O(1)','','需要一片连续的存储空间','','C','顺序表的插入和删除操作平均需要移动一半的元素，时间复杂度为O(n)，而不是O(1)。只有链表的插入删除在已知位置时才是O(1)。','',1,'2026-04-27 02:37:55.052923','2026-04-27 02:37:55.052923',43,'0102010022'),(86,23,'single_choice','单链表设置头结点的主要目的是？','','使空表和非空表的处理统一','','存储链表的实际长度','','作为链表的标志','','提高查找效率','','A','头结点不存储实际数据，它的加入使得空表和非空表的插入、删除操作一致，不需要单独处理空表的情况。','',1,'2026-04-27 02:37:55.054878','2026-04-27 02:37:55.054878',43,'0102010023'),(87,24,'single_choice','在一个长度为n的单链表中删除第i个结点（i>1），最坏情况下的时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(n log n)','','B','最坏情况是删除第一个结点，需要遍历找到待删除结点的前驱结点，时间复杂度为O(n)。','',1,'2026-04-27 02:37:55.056730','2026-04-27 02:37:55.056730',43,'0102010024'),(88,1,'single_choice','顺序表使用一段连续的存储单元依次存储线性表中的数据元素。设顺序表的第一个元素存储地址为LOC(A[0])，每个元素占L个存储单元，则第i个元素的存储地址为？','','LOC(A[0]) + i × L','','LOC(A[0]) + (i-1) × L','','LOC(A[0]) + (i+1) × L','','LOC(A[0]) + L','','B','顺序表是连续存储的，第i个元素（从0开始）的地址 = 首地址 + i × 每个元素占用的单元数。第0个元素地址就是首地址。','',1,'2026-04-27 02:37:55.069225','2026-04-27 02:37:55.069225',44,'0102020001'),(89,2,'single_choice','在长度为n的顺序表中，在第i个位置插入一个元素，最好情况下需要移动多少个元素？','','0','','1','','n-i+1','','n-i','','A','最好情况是在表尾插入（i=n+1），不需要移动任何元素，直接在末尾添加即可。','',1,'2026-04-27 02:37:55.070241','2026-04-27 02:37:55.070241',44,'0102020002'),(90,3,'single_choice','在长度为n的顺序表中，在第i个位置插入一个元素，最坏情况下需要移动多少个元素？','','0','','1','','n-i+1','','n','','C','最坏情况是在表头插入（i=1），需要移动除插入位置外的所有n-i+1个元素。','',1,'2026-04-27 02:37:55.071692','2026-04-27 02:37:55.071692',44,'0102020003'),(91,4,'single_choice','顺序表插入操作的平均时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','B','顺序表插入平均需要移动一半的元素，即(n-1)/2个元素，时间复杂度为O(n)。','',1,'2026-04-27 02:37:55.074315','2026-04-27 02:37:55.074315',44,'0102020004'),(92,5,'single_choice','在长度为n的顺序表中删除第i个元素，最好情况下需要移动多少个元素？','','0','','1','','n-i','','n-i+1','','A','删除表尾元素（i=n）时不需要移动任何元素，时间复杂度为O(1)。','',1,'2026-04-27 02:37:55.075431','2026-04-27 02:37:55.075431',44,'0102020005'),(93,6,'single_choice','在长度为n的顺序表中删除第i个元素，最坏情况下需要移动多少个元素？','','0','','1','','n-i','','n-i+1','','C','删除表头元素（i=1）时需要移动除删除元素外的所有n-i个元素，即将后面所有元素前移。','',1,'2026-04-27 02:37:55.080812','2026-04-27 02:37:55.080812',44,'0102020006'),(94,7,'single_choice','顺序表删除操作的平均时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','B','顺序表删除平均需要移动一半的元素，即(n-1)/2个元素，时间复杂度为O(n)。','',1,'2026-04-27 02:37:55.081992','2026-04-27 02:37:55.081992',44,'0102020007'),(95,8,'single_choice','在顺序表中按值查找（顺序查找）的时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','B','顺序查找需要从表头依次比较，最坏情况是查找元素在表尾或不存在，需要遍历整个表，时间复杂度为O(n)。','',1,'2026-04-27 02:37:55.083375','2026-04-27 02:37:55.083375',44,'0102020008'),(96,9,'single_choice','在有序顺序表中进行折半查找，其时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','D','折半查找每次将搜索范围缩小一半，最多需要log₂n次比较，时间复杂度为O(log n)。','',1,'2026-04-27 02:37:55.084885','2026-04-27 02:37:55.084885',44,'0102020009'),(97,10,'single_choice','两个长度分别为m和n的有序顺序表合并成一个有序顺序表，其时间复杂度是？','','O(m+n)','','O(m×n)','','O(max(m,n))','','O(min(m,n))','','A','合并两个有序表使用双指针法，每个元素最多比较一次，总比较次数最多为m+n，时间复杂度为O(m+n)。','',1,'2026-04-27 02:37:55.086691','2026-04-27 02:37:55.086691',44,'0102020010'),(98,11,'single_choice','设顺序表的长度为n，则按序号查找（第i个元素）的时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','A','顺序表支持随机访问（Random Access），通过首地址和元素序号可以直接计算出任意元素的地址，按序号查找的时间复杂度为O(1)。','',1,'2026-04-27 02:37:55.088988','2026-04-27 02:37:55.088988',44,'0102020011'),(99,12,'single_choice','顺序存储的线性表，其存储密度为？','','0','','1','','小于1','','大于1','','B','顺序表的存储密度=数据元素占用的存储空间/整个存储空间=1，因为顺序表只存储数据元素，没有额外的指针开销。','',1,'2026-04-27 02:37:55.090019','2026-04-27 02:37:55.090019',44,'0102020012'),(100,13,'single_choice','顺序表的主要缺点是？','','不便于随机访问','','存储密度低','','需要预先分配连续存储空间，存储空间不方便扩充','','插入删除操作太简单','','C','顺序表需要一片连续的存储空间，且在初始化时需要预先分配。当存储空间不够时，需要重新分配更大的空间并复制所有元素，这是其主要缺点。','',1,'2026-04-27 02:37:55.091023','2026-04-27 02:37:55.091023',44,'0102020013'),(101,14,'single_choice','将两个非递减有序顺序表La和Lb合并成一个非递减有序顺序表Lc，应采用的算法是？','','选择排序','','冒泡排序','','归并排序的思想','','快速排序','','C','合并两个有序表采用归并排序的思想：同时遍历两个表，比较当前元素，较小的放入结果表，指针后移。时间为O(m+n)。','',1,'2026-04-27 02:37:55.093559','2026-04-27 02:37:55.093559',44,'0102020014'),(102,15,'single_choice','在顺序表L的第i个位置之前插入元素e，以下说法正确的是？','','应从第i个位置开始向后移动元素','','应从第i+1个位置开始向后移动元素','','应从第i-1个位置开始向后移动元素','','不需要移动任何元素','','A','在第i个位置插入，需要先将第i个位置及之后的元素全部后移一位，再将新元素插入到第i个位置。','',1,'2026-04-27 02:37:55.095065','2026-04-27 02:37:55.095065',44,'0102020015'),(103,16,'single_choice','设顺序表的长度为n，当需要频繁地在表尾添加元素且表的长度不确定时，以下说法正确的是？','','顺序表效率最高','','单链表效率最高','','两者效率相同','','需要根据具体情况分析','','D','顺序表在表尾添加元素是O(1)，但需要考虑空间不足时的扩容成本。链表在表尾添加需要遍历。如果扩容不频繁，顺序表效率更高；如果扩容频繁，链表可能更好。','',1,'2026-04-27 02:37:55.096016','2026-04-27 02:37:55.096016',44,'0102020016'),(104,17,'single_choice','顺序表A和顺序表B是两个长度相等的递增有序顺序表，现将它们合并成一个递增顺序表C，最优算法的空间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(m+n)','','A','可以使用归并算法原地合并，但需要移动元素。最优情况是借助一个临时变量交换，但通常需要额外O(n)空间存放结果。如果允许覆盖，算法空间复杂度可以是O(1)。','',1,'2026-04-27 02:37:55.098441','2026-04-27 02:37:55.098441',44,'0102020017'),(105,18,'single_choice','在长度为n的顺序表中，若在第n+1个位置插入元素，需要移动多少个元素？','','0','','1','','n','','n+1','','A','在顺序表末尾（第n+1个位置）插入元素不需要移动任何元素，直接在末尾添加即可。','',1,'2026-04-27 02:37:55.099625','2026-04-27 02:37:55.099625',44,'0102020018'),(106,19,'single_choice','一个顺序表第一个元素的存储地址是100，每个元素占用2个存储单元。第二个元素的存储地址是？','','100','','101','','102','','104','','C','第二个元素的地址 = 首地址 + 1 × 每个元素占用的单元数 = 100 + 1 × 2 = 102。','',1,'2026-04-27 02:37:55.101770','2026-04-27 02:37:55.101770',44,'0102020019'),(107,20,'single_choice','顺序表相对于链表的优点是？','','插入删除操作方便','','存储密度高，支持随机访问','','不需要预先分配空间','','便于动态调整大小','','B','顺序表的主要优点是：存储密度高（存储密度为1）；支持O(1)的随机访问；不需要存储指针节省空间。','',1,'2026-04-27 02:37:55.103681','2026-04-27 02:37:55.103681',44,'0102020020'),(108,21,'single_choice','在有序顺序表中，删除所有值重复的元素，使表中所有元素都不相同，说法正确的是？','','时间复杂度一定是O(n)','','时间复杂度一定是O(n²)','','需要移动所有被删除元素之后的元素','','不需要移动任何元素','','C','在顺序表中删除元素后，需要将被删除元素之后的所有元素前移。删除重复元素的时间复杂度与具体算法实现有关，可能为O(n)或O(n²)。','',1,'2026-04-27 02:37:55.105699','2026-04-27 02:37:55.105699',44,'0102020021'),(109,22,'single_choice','设顺序表的长度为n，则获取第i个元素的时间复杂度为O(1)的条件是？','','i是常数','','顺序表是升序的','','i<=n','','任意i值','','D','顺序表支持随机访问，通过地址计算公式可以直接访问任意位置的元素，无论i是否为常数，获取第i个元素的时间复杂度都是O(1)。','',1,'2026-04-27 02:37:55.106381','2026-04-27 02:37:55.106381',44,'0102020022'),(110,23,'single_choice','对于顺序表的动态扩容，以下说法正确的是？','','每次扩容只增加一个元素的空间','','扩容后需要复制所有元素到新空间','','扩容操作的时间复杂度是O(1)','','顺序表不支持动态扩容','','B','当顺序表空间不足时，需要分配更大的连续空间，并将原空间中的所有元素复制到新空间。扩容的时间成本较高，通常采用倍增策略。','',1,'2026-04-27 02:37:55.107401','2026-04-27 02:37:55.107401',44,'0102020023'),(111,24,'single_choice','在长度为n的顺序表中，删除所有值等于x的元素，时间复杂度最低是？','','O(1)','','O(n)','','O(n²)','','O(n log n)','','B','可以使用双指针（快慢指针）一趟扫描完成：遍历一次，将不等于x的元素前移，时间复杂度为O(n)。','',1,'2026-04-27 02:37:55.110009','2026-04-27 02:37:55.110009',44,'0102020024'),(112,25,'single_choice','顺序表采用一维数组作为存储结构，以下关于数组容量和线性表长度的说法，正确的是？','','数组容量等于线性表长度','','数组容量大于或等于线性表长度','','数组容量小于线性表长度','','两者没有关系','','B','数组容量是分配的存储空间大小，线性表长度是实际存储的元素个数。数组容量必须大于或等于线性表长度，实际存储的元素不能超过分配的数组空间。','',1,'2026-04-27 02:37:55.111963','2026-04-27 02:37:55.111963',44,'0102020025'),(113,1,'single_choice','单链表中每个结点的存储结构包含数据域和指针域，其中指针域指向？','','前驱结点','','后继结点','','头结点','','尾结点','','B','单链表的每个结点包含一个指针域，存储该结点直接后继结点的地址，最后一个结点的指针域为NULL。','',1,'2026-04-27 02:37:55.126451','2026-04-27 02:37:55.126451',45,'0102030001'),(114,2,'single_choice','在单链表p结点之后插入新结点s，以下操作序列正确的是？','','s->next=p; p->next=s;','','s->next=p->next; p->next=s;','','p->next=s; s->next=p->next;','','p->next=s; s->next=p;','','B','正确的顺序是：先将s的指针指向p的后继，再将p的指针指向s。如果先修改p的指针，会丢失原p的后继结点地址。','',1,'2026-04-27 02:37:55.128490','2026-04-27 02:37:55.128490',45,'0102030002'),(115,3,'single_choice','在单链表中删除p结点之后的第一个结点，以下操作序列正确的是？','','p->next=p;','','p->next=p->next->next;','','free(p->next); p->next=NULL;','','p=p->next;','','B','删除p结点后的第一个结点：先将p的指针指向待删除结点的后继结点p->next->next，然后释放待删除结点。如果直接释放会导致链表断裂。','',1,'2026-04-27 02:37:55.130542','2026-04-27 02:37:55.130542',45,'0102030003'),(116,4,'single_choice','设某单链表采用带头结点的结构，则空链表的判定条件是？','','head == NULL','','head->next == NULL','','head->next == head','','head == NULL || head->next == NULL','','B','带头结点的单链表，空表时头结点的next指针为NULL，即head->next == NULL。head结点始终存在。','',1,'2026-04-27 02:37:55.131638','2026-04-27 02:37:55.131638',45,'0102030004'),(117,5,'single_choice','设某单链表不带头结点，则空链表的判定条件是？','','head == NULL','','head->next == NULL','','head->next == head','','head != NULL','','A','不带头结点的单链表，空表时head指针为NULL，即head == NULL。','',1,'2026-04-27 02:37:55.133824','2026-04-27 02:37:55.133824',45,'0102030005'),(118,6,'single_choice','在单链表长度为n的表中，在表头插入一个新结点，时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','A','在表头插入只需要修改头指针的指向，将新结点插入到链表头部，时间复杂度为O(1)。','',1,'2026-04-27 02:37:55.134829','2026-04-27 02:37:55.134829',45,'0102030006'),(119,7,'single_choice','在单链表长度为n的表中，在表尾插入一个新结点，时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','B','在表尾插入需要先遍历到最后一个结点，然后修改尾结点的指针。最坏情况时间复杂度为O(n)。如果维护尾指针则是O(1)。','',1,'2026-04-27 02:37:55.136966','2026-04-27 02:37:55.136966',45,'0102030007'),(120,8,'single_choice','在单链表中，按值查找的时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','B','单链表不支持随机访问，只能从头结点开始顺序遍历查找，最坏情况需要遍历整个链表，时间复杂度为O(n)。','',1,'2026-04-27 02:37:55.139489','2026-04-27 02:37:55.139489',45,'0102030008'),(121,9,'single_choice','对于一个长度为n的单链表，在p结点后插入一个新结点，最好情况和最坏情况的时间复杂度分别是？','','O(1), O(1)','','O(1), O(n)','','O(n), O(1)','','O(n), O(n)','','A','如果已经知道p结点的位置，插入操作只需要修改两个指针，时间复杂度为O(1)。最好情况和最坏情况相同。','',1,'2026-04-27 02:37:55.140878','2026-04-27 02:37:55.140878',45,'0102030009'),(122,10,'single_choice','单链表的存储密度是？','','1','','小于1','','大于1','','0','','B','单链表的存储密度=数据元素占用的存储空间/（数据元素占用的存储空间+指针占用的存储空间），由于需要额外的指针域存储后继地址，存储密度小于1。','',1,'2026-04-27 02:37:55.143349','2026-04-27 02:37:55.143349',45,'0102030010'),(123,11,'single_choice','在循环单链表中，尾结点的指针域指向？','','NULL','','头结点','','尾结点自己','','第一个数据结点','','B','循环单链表的尾结点指针指向头结点（或第一个结点），形成环。普通单链表的尾结点指针为NULL。','',1,'2026-04-27 02:37:55.144936','2026-04-27 02:37:55.144936',45,'0102030011'),(124,12,'single_choice','在双向链表中，p结点的前驱指针是？','','p->prior','','p->next','','p->prior->prior','','p->next->prior','','A','双向链表的每个结点包含两个指针：prior指向前驱结点，next指向后继结点。p->prior就是p结点的前驱结点。','',1,'2026-04-27 02:37:55.146734','2026-04-27 02:37:55.146734',45,'0102030012'),(125,13,'single_choice','在双向链表中，在p结点之前插入新结点s，以下操作序列正确的是？','','s->prior=p->prior; s->next=p; p->prior->next=s; p->prior=s;','','p->prior->next=s; s->prior=p->prior; s->next=p; p->prior=s;','','s->next=p; s->prior=p->prior; p->prior=s;','','p->prior=s; s->next=p; s->prior=p->prior;','','A','在双向链表p结点前插入s，需要修改4个指针：s->prior=p->prior，s->next=p，p->prior->next=s，p->prior=s。注意操作顺序不能错，避免链表断裂。','',1,'2026-04-27 02:37:55.147767','2026-04-27 02:37:55.147767',45,'0102030013'),(126,14,'single_choice','在双向链表中，删除p结点，以下操作序列正确的是？','','p->prior->next=p->next; p->next->prior=p->prior; free(p);','','p->prior=p->next; p->next->prior=p->prior;','','p->prior->next=p; p->next->prior=p;','','free(p);','','A','删除双向链表中的p结点，需要将被删除结点的前驱结点的next指向p的后继，p的后继结点的prior指向p的前驱，然后释放p结点。','',1,'2026-04-27 02:37:55.149270','2026-04-27 02:37:55.149270',45,'0102030014'),(127,15,'single_choice','设有一个循环双链表，p指向表中的某个结点（不是头结点），若删除p结点，正确的语句是？','','p->prior->next=p->next; p->next->prior=p->prior; free(p);','','p=p->next; free(p);','','p->prior->next=p; p->next->prior=p;','','p->prior->next=NULL; p->next->prior=NULL;','','A','删除循环双链表中的p结点：将p的前驱结点的next指向p的后继，将p的后继结点的prior指向p的前驱，然后释放p。循环双链表的删除操作与普通双链表类似。','',1,'2026-04-27 02:37:55.151801','2026-04-27 02:37:55.151801',45,'0102030015'),(128,16,'single_choice','在单链表中，设计一个算法就地逆置链表（即空间复杂度为O(1)），以下哪种方法正确？','','头插法','','交换相邻结点','','递归反转','','创建新链表','','A','头插法就地逆置：将原链表结点依次头插到新链表（或原链表头部），不申请新结点空间，空间复杂度为O(1)。','',1,'2026-04-27 02:37:55.153999','2026-04-27 02:37:55.153999',45,'0102030016'),(129,17,'single_choice','对于带头结点的单链表L，其头结点为L，在表头插入元素e，算法的时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','A','带头结点的单链表的表头插入：创建新结点s，s->next=L->next，L->next=s。只需要修改两个指针，时间复杂度为O(1)。','',1,'2026-04-27 02:37:55.155006','2026-04-27 02:37:55.155006',45,'0102030017'),(130,18,'single_choice','单链表的按序号查找（第i个结点）的时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','B','单链表不支持随机访问，需要从表头开始顺序遍历，找到第i个结点。最坏情况i=n，需要遍历n个结点，时间复杂度为O(n)。','',1,'2026-04-27 02:37:55.157398','2026-04-27 02:37:55.157398',45,'0102030018'),(131,19,'single_choice','在循环单链表中，判空条件是（假设表有头结点）？','','head == NULL','','head->next == NULL','','head->next == head','','head->next != head','','C','循环单链表空表时，头结点的next指针指向自己，即head->next == head。','',1,'2026-04-27 02:37:55.163485','2026-04-27 02:37:55.163485',45,'0102030019'),(132,20,'single_choice','在单链表中，删除第i个结点（i>1），若已知表头指针head和p指向第i-1个结点，则时间复杂度是？','','O(1)','','O(n)','','O(n²)','','O(log n)','','A','已知第i-1个结点p，删除第i个结点只需要：q=p->next（待删除结点），p->next=q->next，free(q)。只需要修改指针，时间复杂度O(1)。','',1,'2026-04-27 02:37:55.164988','2026-04-27 02:37:55.164988',45,'0102030020'),(133,21,'single_choice','静态链表与动态单链表的主要区别是？','','静态链表用数组实现，动态链表用指针实现','','静态链表不支持插入删除操作','','动态链表不需要存储空间','','两者完全相同','','A','静态链表用数组的下标模拟指针来存储结点间的逻辑关系；动态单链表用malloc/free或new/delete动态申请和释放结点空间。两者逻辑结构相同，只是存储方式不同。','',1,'2026-04-27 02:37:55.166725','2026-04-27 02:37:55.166725',45,'0102030021'),(134,22,'single_choice','对于双向链表，在p结点之后插入新结点s，正确的操作序列是？','','s->prior=p; s->next=p->next; p->next->prior=s; p->next=s;','','s->next=p->next; p->next=s; s->prior=p;','','p->next=s; s->prior=p; s->next=p->next;','','p->next->prior=s; p->next=s; s->next=p->next; s->prior=p;','','A','在双向链表p结点后插入s：s->prior=p，s->next=p->next，p->next->prior=s，p->next=s。注意先处理s的指针，再处理p后继结点的前驱指针，最后处理p的后继指针。','',1,'2026-04-27 02:37:55.169084','2026-04-27 02:37:55.169084',45,'0102030022'),(135,23,'single_choice','单链表的每个结点占用两个存储域？','','正确','','错误，数据域和指针域可以是多个','','错误，只占用一个存储域','','错误，结点不占用存储域','','A','单链表的每个结点包含两个域：数据域（存储数据元素）和指针域（存储后继结点地址）。这是单链表的基本结构。','',1,'2026-04-27 02:37:55.170108','2026-04-27 02:37:55.170108',45,'0102030023'),(136,24,'single_choice','在单链表中，合并两个有序单链表La和Lb（均为递增有序），使合并后的链表仍然有序，以下说法正确的是？','','需要申请新结点存储合并结果','','可以原地合并，不需要申请新结点','','无法合并','','合并后链表必为递减有序','','B','可以采用归并思想原地合并两个有序单链表：同时遍历La和Lb，将较小的结点尾插到结果链表，不需要申请新结点。','',1,'2026-04-27 02:37:55.172052','2026-04-27 02:37:55.172052',45,'0102030024');
/*!40000 ALTER TABLE `question_bank_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_bank_subchapter`
--

DROP TABLE IF EXISTS `question_bank_subchapter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_bank_subchapter` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` int unsigned NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `chapter_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_chapter_order_no` (`chapter_id`,`order_no`),
  UNIQUE KEY `unique_chapter_subchapter` (`chapter_id`,`name`),
  CONSTRAINT `question_bank_subcha_chapter_id_4f10054a_fk_question_` FOREIGN KEY (`chapter_id`) REFERENCES `question_bank_chapter` (`id`),
  CONSTRAINT `question_bank_subchapter_chk_1` CHECK ((`order_no` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_bank_subchapter`
--

LOCK TABLES `question_bank_subchapter` WRITE;
/*!40000 ALTER TABLE `question_bank_subchapter` DISABLE KEYS */;
INSERT INTO `question_bank_subchapter` VALUES (41,1,'数据结构的基本概念',1,'2026-04-27 02:37:54.935883','2026-04-27 02:37:54.935883',19),(42,2,'算法和算法评价',1,'2026-04-27 02:37:54.957310','2026-04-27 02:37:54.957310',19),(43,1,'线性表的基本概念',1,'2026-04-27 02:37:55.000551','2026-04-27 02:37:55.000551',20),(44,2,'线性表的顺序表示和实现',1,'2026-04-27 02:37:55.060060','2026-04-27 02:37:55.060060',20),(45,3,'线性表的链式表示和实现',1,'2026-04-27 02:37:55.113967','2026-04-27 02:37:55.113967',20);
/*!40000 ALTER TABLE `question_bank_subchapter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subchapter_practice_progress`
--

DROP TABLE IF EXISTS `subchapter_practice_progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subchapter_practice_progress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_answer` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_locked` tinyint(1) NOT NULL,
  `first_answered_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `question_id` bigint NOT NULL,
  `subchapter_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_subchapter_question_progress` (`user_id`,`subchapter_id`,`question_id`),
  KEY `subchapter_practice__question_id_bce542e2_fk_question_` (`question_id`),
  KEY `subchapter_practice__subchapter_id_01d05f8f_fk_question_` (`subchapter_id`),
  KEY `subchapter__user_id_1a6c1f_idx` (`user_id`,`subchapter_id`),
  KEY `subchapter__user_id_f5cbfd_idx` (`user_id`,`subchapter_id`,`status`),
  CONSTRAINT `subchapter_practice__question_id_bce542e2_fk_question_` FOREIGN KEY (`question_id`) REFERENCES `question_bank_question` (`id`),
  CONSTRAINT `subchapter_practice__subchapter_id_01d05f8f_fk_question_` FOREIGN KEY (`subchapter_id`) REFERENCES `question_bank_subchapter` (`id`),
  CONSTRAINT `subchapter_practice_progress_user_id_59fc909d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subchapter_practice_progress`
--

LOCK TABLES `subchapter_practice_progress` WRITE;
/*!40000 ALTER TABLE `subchapter_practice_progress` DISABLE KEYS */;
INSERT INTO `subchapter_practice_progress` VALUES (22,'wrong','B',1,'2026-04-27 05:29:19.390746','2026-04-27 05:29:19.392906','2026-04-27 05:29:19.392906',39,41,2),(23,'wrong','D',1,'2026-04-27 05:29:22.279737','2026-04-27 05:29:22.281112','2026-04-27 05:29:22.281112',40,41,2),(24,'correct','C',1,'2026-04-27 05:29:25.550466','2026-04-27 05:29:25.551468','2026-04-27 05:29:25.551468',41,41,2),(25,'wrong','D',1,'2026-04-27 05:29:28.271036','2026-04-27 05:29:28.272215','2026-04-27 05:29:28.272215',42,41,2),(26,'correct','D',1,'2026-04-27 05:29:30.279085','2026-04-27 05:29:30.280635','2026-04-27 05:29:30.280635',43,41,2),(27,'wrong','C',1,'2026-04-27 05:29:32.909902','2026-04-27 05:29:32.910964','2026-04-27 05:29:32.910964',44,41,2),(28,'wrong','D',1,'2026-04-27 05:29:36.375460','2026-04-27 05:29:36.376466','2026-04-27 05:29:36.376466',45,41,2),(29,'wrong','C',1,'2026-04-27 05:29:39.360746','2026-04-27 05:29:39.362596','2026-04-27 05:29:39.362596',46,41,2),(30,'correct','D',1,'2026-04-27 05:29:41.662620','2026-04-27 05:29:41.664774','2026-04-27 05:29:41.664774',47,41,2),(31,'correct','B',1,'2026-04-27 05:29:44.478201','2026-04-27 05:29:44.480209','2026-04-27 05:29:44.480209',48,41,2),(32,'wrong','D',1,'2026-04-27 05:31:17.809752','2026-04-27 05:31:17.810768','2026-04-27 05:31:17.810768',39,41,5),(33,'wrong','D',1,'2026-04-27 05:31:20.103694','2026-04-27 05:31:20.104701','2026-04-27 05:31:20.104701',40,41,5),(34,'wrong','D',1,'2026-04-27 05:31:22.526190','2026-04-27 05:31:22.527192','2026-04-27 05:31:22.527192',41,41,5),(35,'wrong','D',1,'2026-04-27 05:31:25.072217','2026-04-27 05:31:25.073222','2026-04-27 05:31:25.073222',42,41,5),(36,'correct','D',1,'2026-04-27 05:31:26.950467','2026-04-27 05:31:26.952477','2026-04-27 05:31:26.952477',43,41,5),(37,'wrong','D',1,'2026-04-27 05:31:29.488500','2026-04-27 05:31:29.490996','2026-04-27 05:31:29.490996',44,41,5),(38,'wrong','D',1,'2026-04-27 05:31:32.614794','2026-04-27 05:31:32.616821','2026-04-27 05:31:32.616821',45,41,5),(39,'wrong','D',1,'2026-04-27 05:31:35.047199','2026-04-27 05:31:35.048201','2026-04-27 05:31:35.048201',46,41,5),(40,'correct','D',1,'2026-04-27 05:31:37.210427','2026-04-27 05:31:37.212499','2026-04-27 05:31:37.212499',47,41,5),(41,'wrong','D',1,'2026-04-27 05:31:40.127822','2026-04-27 05:31:40.128827','2026-04-27 05:31:40.129830',48,41,5),(42,'wrong','B',1,'2026-04-28 02:51:09.684717','2026-04-28 02:51:09.684717','2026-04-28 02:51:09.684717',64,43,1),(43,'wrong','D',1,'2026-04-28 02:51:12.036317','2026-04-28 02:51:12.042922','2026-04-28 02:51:12.043427',65,43,1),(44,'wrong','B',1,'2026-04-28 02:51:23.577380','2026-04-28 02:51:23.578920','2026-04-28 02:51:23.578920',66,43,1),(45,'correct','A',1,'2026-04-28 02:51:35.655932','2026-04-28 02:51:35.655932','2026-04-28 02:51:35.655932',67,43,1),(56,'correct','A',1,'2026-04-28 06:55:48.689414','2026-04-28 06:55:48.689414','2026-04-28 06:55:48.689414',40,41,1);
/*!40000 ALTER TABLE `subchapter_practice_progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrong_question_reviews`
--

DROP TABLE IF EXISTS `wrong_question_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wrong_question_reviews` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_wrong_time` datetime(6) NOT NULL,
  `last_review_time` datetime(6) DEFAULT NULL,
  `review_count` int unsigned NOT NULL,
  `next_review_time` datetime(6) NOT NULL,
  `is_mastered` tinyint(1) NOT NULL,
  `is_removed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `question_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_question_review` (`user_id`,`question_id`),
  KEY `wrong_question_revie_question_id_41ecbd50_fk_question_` (`question_id`),
  CONSTRAINT `wrong_question_revie_question_id_41ecbd50_fk_question_` FOREIGN KEY (`question_id`) REFERENCES `question_bank_question` (`id`),
  CONSTRAINT `wrong_question_reviews_user_id_74dc266a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `wrong_question_reviews_chk_1` CHECK ((`review_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrong_question_reviews`
--

LOCK TABLES `wrong_question_reviews` WRITE;
/*!40000 ALTER TABLE `wrong_question_reviews` DISABLE KEYS */;
INSERT INTO `wrong_question_reviews` VALUES (1,'2026-04-27 03:28:34.892032','2026-04-27 03:36:03.453360',1,'2026-04-29 03:36:03.453360',0,0,'2026-04-27 03:28:34.892032','2026-04-27 03:36:03.454400',39,1),(2,'2026-04-27 03:28:34.899417',NULL,0,'2026-04-27 03:28:34.898912',0,0,'2026-04-27 03:28:34.900418','2026-04-27 03:28:34.900418',40,1),(3,'2026-04-27 03:28:34.910348',NULL,0,'2026-04-27 03:28:34.907836',0,0,'2026-04-27 03:28:34.910348','2026-04-27 03:28:34.910348',41,1),(4,'2026-04-27 05:29:19.406546',NULL,0,'2026-04-28 05:29:19.405297',0,0,'2026-04-27 05:29:19.407549','2026-04-27 05:29:19.407549',39,2),(5,'2026-04-27 05:29:22.293778',NULL,0,'2026-04-28 05:29:22.292776',0,0,'2026-04-27 05:29:22.293778','2026-04-27 05:29:22.293778',40,2),(6,'2026-04-27 05:29:28.284701',NULL,0,'2026-04-28 05:29:28.282685',0,0,'2026-04-27 05:29:28.284701','2026-04-27 05:29:28.284701',42,2),(7,'2026-04-27 05:29:32.926918',NULL,0,'2026-04-28 05:29:32.924653',0,0,'2026-04-27 05:29:32.926918','2026-04-27 05:29:32.926918',44,2),(8,'2026-04-27 05:29:36.390044',NULL,0,'2026-04-28 05:29:36.388801',0,0,'2026-04-27 05:29:36.390044','2026-04-27 05:29:36.390044',45,2),(9,'2026-04-27 05:29:39.375827',NULL,0,'2026-04-28 05:29:39.374592',0,0,'2026-04-27 05:29:39.375827','2026-04-27 05:29:39.375827',46,2),(10,'2026-04-27 05:31:17.825977',NULL,0,'2026-04-28 05:31:17.823727',0,0,'2026-04-27 05:31:17.825977','2026-04-27 05:31:17.825977',39,5),(11,'2026-04-27 05:31:20.116416',NULL,0,'2026-04-28 05:31:20.115403',0,0,'2026-04-27 05:31:20.116416','2026-04-27 05:31:20.116416',40,5),(12,'2026-04-27 05:31:22.539074',NULL,0,'2026-04-28 05:31:22.538071',0,0,'2026-04-27 05:31:22.539074','2026-04-27 05:31:22.539074',41,5),(13,'2026-04-27 05:31:25.084677',NULL,0,'2026-04-28 05:31:25.083314',0,0,'2026-04-27 05:31:25.084677','2026-04-27 05:31:25.084677',42,5),(14,'2026-04-27 05:31:29.504050',NULL,0,'2026-04-28 05:31:29.502039',0,0,'2026-04-27 05:31:29.504050','2026-04-27 05:31:29.504050',44,5),(15,'2026-04-27 05:31:32.629707',NULL,0,'2026-04-28 05:31:32.628475',0,0,'2026-04-27 05:31:32.629707','2026-04-27 05:31:32.629707',45,5),(16,'2026-04-27 05:31:35.061362',NULL,0,'2026-04-28 05:31:35.060219',0,0,'2026-04-27 05:31:35.061362','2026-04-27 05:31:35.061362',46,5),(17,'2026-04-27 05:31:40.142372',NULL,0,'2026-04-28 05:31:40.140365',0,0,'2026-04-27 05:31:40.142372','2026-04-27 05:31:40.142372',48,5),(18,'2026-04-28 02:51:09.705168',NULL,0,'2026-04-29 02:51:09.702803',0,0,'2026-04-28 02:51:09.705168','2026-04-28 02:51:09.705168',64,1),(19,'2026-04-28 02:51:12.050411',NULL,0,'2026-04-29 02:51:12.050411',0,0,'2026-04-28 02:51:12.050411','2026-04-28 02:51:12.050411',65,1),(20,'2026-04-28 02:51:23.591331',NULL,0,'2026-04-29 02:51:23.588026',0,0,'2026-04-28 02:51:23.591331','2026-04-28 02:51:23.591331',66,1),(21,'2026-04-28 02:52:35.543657',NULL,0,'2026-04-29 02:52:35.541464',0,0,'2026-04-28 02:52:35.543657','2026-04-28 02:52:35.543657',43,1);
/*!40000 ALTER TABLE `wrong_question_reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrong_questions`
--

DROP TABLE IF EXISTS `wrong_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wrong_questions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `wrong_count` int unsigned NOT NULL,
  `last_wrong_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `question_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_wrong_question` (`user_id`,`question_id`),
  KEY `wrong_questions_question_id_3c8d5432_fk_question_` (`question_id`),
  CONSTRAINT `wrong_questions_question_id_3c8d5432_fk_question_` FOREIGN KEY (`question_id`) REFERENCES `question_bank_question` (`id`),
  CONSTRAINT `wrong_questions_user_id_3341c1bd_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `wrong_questions_chk_1` CHECK ((`wrong_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrong_questions`
--

LOCK TABLES `wrong_questions` WRITE;
/*!40000 ALTER TABLE `wrong_questions` DISABLE KEYS */;
INSERT INTO `wrong_questions` VALUES (7,2,'2026-04-26 02:41:26.161704',1,'2026-04-26 02:41:26.161704','2026-04-28 02:52:26.723839',40,1),(8,1,'2026-04-27 02:42:42.817526',1,'2026-04-27 02:42:42.817526','2026-04-27 02:42:42.817526',45,1),(9,1,'2026-04-27 02:43:06.252482',1,'2026-04-27 02:43:06.252482','2026-04-27 02:43:06.252482',46,1),(10,1,'2026-04-27 05:29:19.404178',1,'2026-04-27 05:29:19.404178','2026-04-27 05:29:19.404178',39,2),(11,1,'2026-04-27 05:29:22.291653',1,'2026-04-27 05:29:22.291653','2026-04-27 05:29:22.291653',40,2),(12,1,'2026-04-27 05:29:28.282685',1,'2026-04-27 05:29:28.282685','2026-04-27 05:29:28.282685',42,2),(13,1,'2026-04-27 05:29:32.924653',1,'2026-04-27 05:29:32.924653','2026-04-27 05:29:32.924653',44,2),(14,1,'2026-04-27 05:29:36.388801',1,'2026-04-27 05:29:36.388801','2026-04-27 05:29:36.388801',45,2),(15,1,'2026-04-27 05:29:39.373589',1,'2026-04-27 05:29:39.373589','2026-04-27 05:29:39.373589',46,2),(16,1,'2026-04-27 05:31:17.822724',1,'2026-04-27 05:31:17.822724','2026-04-27 05:31:17.822724',39,5),(17,1,'2026-04-27 05:31:20.114400',1,'2026-04-27 05:31:20.114400','2026-04-27 05:31:20.114400',40,5),(18,1,'2026-04-27 05:31:22.537069',1,'2026-04-27 05:31:22.537069','2026-04-27 05:31:22.537069',41,5),(19,1,'2026-04-27 05:31:25.082150',1,'2026-04-27 05:31:25.082150','2026-04-27 05:31:25.082150',42,5),(20,1,'2026-04-27 05:31:29.500814',1,'2026-04-27 05:31:29.500814','2026-04-27 05:31:29.500814',44,5),(21,1,'2026-04-27 05:31:32.628475',1,'2026-04-27 05:31:32.628475','2026-04-27 05:31:32.628475',45,5),(22,1,'2026-04-27 05:31:35.058927',1,'2026-04-27 05:31:35.058927','2026-04-27 05:31:35.058927',46,5),(23,1,'2026-04-27 05:31:40.139357',1,'2026-04-27 05:31:40.139357','2026-04-27 05:31:40.139357',48,5),(24,1,'2026-04-28 02:51:09.702803',1,'2026-04-28 02:51:09.702803','2026-04-28 02:51:09.702803',64,1),(25,1,'2026-04-28 02:51:12.050411',1,'2026-04-28 02:51:12.050411','2026-04-28 02:51:12.050411',65,1),(26,1,'2026-04-28 02:51:23.588026',1,'2026-04-28 02:51:23.588026','2026-04-28 02:51:23.588026',66,1),(27,1,'2026-04-28 02:52:29.277158',1,'2026-04-28 02:52:29.277158','2026-04-28 02:52:29.277158',41,1),(28,1,'2026-04-28 02:52:35.541464',1,'2026-04-28 02:52:35.541464','2026-04-28 02:52:35.541464',43,1);
/*!40000 ALTER TABLE `wrong_questions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-16 12:07:46
