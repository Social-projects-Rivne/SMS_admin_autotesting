--create db. CHARACTER SET!!!
CREATE DATABASE IF NOT EXISTS SMSDB CHARACTER SET utf8;

--switch to ur db
USE SMSDB;

-- table Roles
DROP TABLE IF EXISTS `Roles`;
		
CREATE TABLE `Roles` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`)
);

-- table Schools
DROP TABLE IF EXISTS `Schools`;
		
CREATE TABLE `Schools` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL,
  PRIMARY KEY (`id`)
);

-- table Teachers
DROP TABLE IF EXISTS `Teachers`;
		
CREATE TABLE `Teachers` (
  `school_id` INTEGER NULL DEFAULT NULL,
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `role_id` INTEGER NOT NULL,
  `login` VARCHAR(40) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`)
);

-- create foreign key
ALTER TABLE `Teachers` ADD FOREIGN KEY (school_id) REFERENCES `Schools` (`id`);
ALTER TABLE `Teachers` ADD FOREIGN KEY (role_id) REFERENCES `Roles` (`id`);

SHOW TABLES;
