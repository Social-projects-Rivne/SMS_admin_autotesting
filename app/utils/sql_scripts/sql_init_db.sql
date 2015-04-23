-- create db. CHARACTER SET!!!
CREATE DATABASE IF NOT EXISTS SMSDB CHARACTER SET utf8;

-- switch to ur db
USE SMSDB;

-- drop tables before create new

DROP TABLE IF EXISTS `Teachers`;
DROP TABLE IF EXISTS `Roles`;
DROP TABLE IF EXISTS `Schools`;
DROP TABLE IF EXISTS `Subjects`;


-- table Roles
CREATE TABLE `Roles` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`)
);

-- table Schools
CREATE TABLE `Schools` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL,
  `address` VARCHAR(256) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- table Subjects
CREATE TABLE `Subjects` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id`)
);

-- table Teachers
CREATE TABLE `Teachers` (
  `school_id` INTEGER NULL DEFAULT NULL,
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `role_id` INTEGER NOT NULL,
  `login` VARCHAR(40) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`)
);

-- create foreign key
ALTER TABLE `Teachers` ADD FOREIGN KEY (school_id) REFERENCES `Schools` (`id`);
ALTER TABLE `Teachers` ADD FOREIGN KEY (role_id) REFERENCES `Roles` (`id`);

SHOW TABLES;

-- Insert Data
INSERT INTO `Roles` (`id`,`role_name`) VALUES ('1','Головний вчитель');
INSERT INTO `Roles` (`id`,`role_name`) VALUES ('2','Завуч');
INSERT INTO `Roles` (`id`,`role_name`) VALUES ('3','Викладач');


-- Test Data

INSERT INTO `Teachers` (`id`,`name`,`role_id`,`login`, `email`, `password`)
VALUES ('1','Teacher Name1','1','kihh', 'ffffdd@gmail.com', 'df5sdf');
INSERT INTO `Teachers` (`id`,`name`,`role_id`,`login`, `email`, `password`)
VALUES ('2','Teacher Name2','2','folk', 'dfsd@gmail.com', 'dffffdh');

INSERT INTO `Schools` (`id`,`name`,`address`) VALUES ('1','School2', 'City1');
INSERT INTO `Schools` (`id`,`name`,`address`) VALUES ('2','School3', 'City2');

INSERT INTO `Subjects` (`id`,`name`) VALUES ('1','Math');
INSERT INTO `Subjects` (`id`,`name`) VALUES ('2','Geography');