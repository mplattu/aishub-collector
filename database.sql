-- phpMyAdmin SQL Dump
-- version 4.4.12
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 21, 2018 at 04:52 PM
-- Server version: 5.5.59-0+deb8u1
-- PHP Version: 5.6.33-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `ais`
--
CREATE DATABASE IF NOT EXISTS `ais` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `ais`;

-- --------------------------------------------------------

--
-- Table structure for table `aisdata`
--

CREATE TABLE IF NOT EXISTS `aisdata` (
  `mmsi` char(16) DEFAULT NULL,
  `time` datetime DEFAULT NULL COMMENT 'GMT',
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `cog` float DEFAULT NULL,
  `sog` float DEFAULT NULL,
  `heading` int(11) DEFAULT NULL,
  `navstat` int(11) DEFAULT NULL,
  `imo` char(16) DEFAULT NULL,
  `name` char(32) DEFAULT NULL,
  `callsign` char(16) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  `d` int(11) DEFAULT NULL,
  `draught` float DEFAULT NULL,
  `dest` char(32) DEFAULT NULL,
  `eta` char(32) DEFAULT NULL,
  `_writetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Data written to db'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `temp`
--

CREATE TABLE IF NOT EXISTS `temp` (
  `mmsi` char(16) DEFAULT NULL,
  `time` datetime DEFAULT NULL COMMENT 'GMT',
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `cog` float DEFAULT NULL,
  `sog` float DEFAULT NULL,
  `heading` int(11) DEFAULT NULL,
  `navstat` int(11) DEFAULT NULL,
  `imo` char(16) DEFAULT NULL,
  `name` char(32) DEFAULT NULL,
  `callsign` char(16) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  `d` int(11) DEFAULT NULL,
  `draught` float DEFAULT NULL,
  `dest` char(32) DEFAULT NULL,
  `eta` char(32) DEFAULT NULL,
  `_writetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Data written to db'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
