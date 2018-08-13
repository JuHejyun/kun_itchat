/*
SQLyog Ultimate v12.5.1 (64 bit)
MySQL - 5.7.19 : Database - wechat_record
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`wechat_record` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `wechat_record`;

/*Table structure for table `group_chat` */

DROP TABLE IF EXISTS `group_chat`;

CREATE TABLE `group_chat` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `g_id` varchar(200) DEFAULT NULL COMMENT '群id',
  `type` varchar(10) DEFAULT NULL COMMENT '消息类型',
  `from_user_name` varchar(100) DEFAULT NULL COMMENT '消息来至那个群',
  `actual_nick_name` varchar(100) DEFAULT NULL COMMENT '发送者的昵称',
  `content` varchar(2000) DEFAULT NULL COMMENT '文本消息',
  `file_path` varchar(50) DEFAULT NULL COMMENT '文件路径',
  `send_time` bigint(20) DEFAULT NULL COMMENT '发送的时间',
  `create_time` bigint(20) DEFAULT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
