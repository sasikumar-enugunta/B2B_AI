-- phpMyAdmin SQL Dump
-- version 3.4.11.1
-- http://www.phpmyadmin.net
--
-- Host: mysql3000.mochahost.com
-- Generation Time: Nov 10, 2020 at 03:57 PM
-- Server version: 5.6.23
-- PHP Version: 7.3.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ivision1_ivisions_b2bai`
--

-- --------------------------------------------------------

--
-- Table structure for table `ai_login`
--

CREATE TABLE IF NOT EXISTS `ai_login` (
  `login_user` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `json_file` varchar(50) NOT NULL,
  `uploaded_json` date NOT NULL,
  `csv_file` varchar(50) NOT NULL,
  PRIMARY KEY (`login_user`),
  KEY `json_file` (`json_file`),
  KEY `csv_file` (`csv_file`),
  KEY `uploaded_json` (`uploaded_json`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ai_login`
--

INSERT INTO `ai_login` (`login_user`, `password`, `json_file`, `uploaded_json`, `csv_file`) VALUES
('mnasseri210@outlook.com', 'Forever2020!', 'messages_maryam.json', '2020-09-11', 'contacts_maryam.csv');

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE IF NOT EXISTS `client` (
  `skype_id` varchar(50) NOT NULL,
  `conv_date` date NOT NULL,
  `conversation` text NOT NULL,
  `manufacturer` varchar(50) NOT NULL,
  `outgoing_chat` text NOT NULL,
  `logged_in_user` varchar(50) NOT NULL,
  KEY `skype_id` (`skype_id`),
  KEY `manufacturer` (`manufacturer`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `contact_info`
--

CREATE TABLE IF NOT EXISTS `contact_info` (
  `skype_id` varchar(40) NOT NULL,
  `display_name` text NOT NULL,
  `gender` varchar(10) NOT NULL,
  `country` varchar(20) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `firstname` varchar(30) NOT NULL,
  `surname` varchar(30) NOT NULL,
  `mobile_no` varchar(30) NOT NULL,
  `office_no` varchar(30) NOT NULL,
  `website` text NOT NULL,
  `added_date` date NOT NULL,
  `imported_date` date NOT NULL,
  PRIMARY KEY (`skype_id`),
  KEY `country` (`country`),
  KEY `added_date` (`added_date`),
  KEY `imported_date` (`imported_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE IF NOT EXISTS `login` (
  `username` varchar(40) NOT NULL,
  `password` varchar(40) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`username`, `password`) VALUES
('santhosh', 'santhosh'),
('sasi', 'sasi');

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE IF NOT EXISTS `vendor` (
  `skype_id` varchar(50) NOT NULL,
  `conv_date` date NOT NULL,
  `conversation` text NOT NULL,
  `manufacturer` varchar(50) NOT NULL,
  `outgoing_chat` text NOT NULL,
  `logged_in_user` varchar(50) NOT NULL,
  KEY `skype_id` (`skype_id`),
  KEY `manufacturer` (`manufacturer`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
