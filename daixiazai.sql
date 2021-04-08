/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : daixiazai

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2018-03-26 23:37:07
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `csdn_account`
-- ----------------------------
DROP TABLE IF EXISTS `csdn_account`;
CREATE TABLE `csdn_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `account_type` varchar(255) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `today_download_times` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of csdn_account
-- ----------------------------
INSERT INTO `csdn_account` VALUES ('1', '13052237150', 'Qwert12345@', 'normal', '10', '21', null);
INSERT INTO `csdn_account` VALUES ('2', '18701863761', 'Qwert12345@', 'normal', '10', '21', null);
INSERT INTO `csdn_account` VALUES ('3', '13817249443', 'Qwert12345@', 'normal', '10', '21', null);
INSERT INTO `csdn_account` VALUES ('4', '13761151584', 'Qwert12345@', 'vip', '10', '11', null);

-- ----------------------------
-- Table structure for `csdn_download`
-- ----------------------------
DROP TABLE IF EXISTS `csdn_download`;
CREATE TABLE `csdn_download` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(1000) NOT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `src_url` varchar(255) NOT NULL,
  `path` varchar(255) DEFAULT NULL,
  `csdn_account` varchar(255) DEFAULT NULL,
  `order_no` varchar(255) DEFAULT NULL,
  `step` int(11) DEFAULT NULL COMMENT '0 已下载 1已发送',
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of csdn_download
-- ----------------------------
INSERT INTO `csdn_download` VALUES ('1', 'students也是考勤.rar', 'goldarowana@163.com', 'https://download.csdn.net/download/shanshanxiao/1807189', 'E:\\code\\python\\csdn\\files\\', '13761151584', '139651690069334590', '1', '1522056493');
INSERT INTO `csdn_download` VALUES ('2', 'opencv-python-tutroals.pdf', 'zhangchungame@163.com', 'https://download.csdn.net/download/qq_41843436/10287685', 'E:\\code\\python\\csdn\\files\\', '13761151584', '140052581942747907', '1', '1522056965');
INSERT INTO `csdn_download` VALUES ('3', '单片机c语言实例程序300篇.doc', '342219728@qq.com', 'https://download.csdn.net/download/fenkao/2717741', 'E:\\code\\python\\csdn\\files\\', '13761151584', '141349933488747907', '1', '1522074904');

-- ----------------------------
-- Table structure for `tb_order`
-- ----------------------------
DROP TABLE IF EXISTS `tb_order`;
CREATE TABLE `tb_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(255) DEFAULT NULL,
  `step` int(11) NOT NULL COMMENT '0初始化 1处理中 2处理完成 9remark失败 8 下载失败 ',
  `order_type` varchar(255) NOT NULL,
  `remark` text,
  `create_time` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tb_order
-- ----------------------------
INSERT INTO `tb_order` VALUES ('1', '139651690069334590', '2', 'csdn', 'goldarowana@163.com https://download.csdn.net/download/shanshanxiao/1807189#comment', '1522056393', '1522056493');
INSERT INTO `tb_order` VALUES ('2', '140052581942747907', '2', 'csdn', 'zhangchungame@163.com https://download.csdn.net/download/qq_41843436/10287685', '1522056405', '1522056967');
INSERT INTO `tb_order` VALUES ('3', '79398960182763154', '9', '', '', '1522056417', '1522056572');
INSERT INTO `tb_order` VALUES ('4', '141349933488747907', '2', 'csdn', '342219728@qq.com https://download.csdn.net/download/fenkao/2717741', '1522074771', '1522074904');
