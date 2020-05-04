-- phpMyAdmin SQL Dump
-- version 4.0.10deb1ubuntu0.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 03, 2020 at 06:17 PM
-- Server version: 5.5.62-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `rajones_IS437`
--

-- --------------------------------------------------------

--
-- Table structure for table `animals`
--

CREATE TABLE IF NOT EXISTS `animals` (
  `animalID` int(11) NOT NULL AUTO_INCREMENT,
  `animalName` varchar(100) NOT NULL,
  `animalType` varchar(50) NOT NULL,
  `animalBreed` varchar(100) NOT NULL,
  `animalAge` int(3) NOT NULL,
  `animalGender` varchar(10) NOT NULL,
  `animalSize` varchar(50) NOT NULL,
  `animalPhoto` varchar(500) NOT NULL,
  `animalStatus` varchar(50) NOT NULL,
  `userID` int(5) DEFAULT NULL,
  PRIMARY KEY (`animalID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `animals`
--

INSERT INTO `animals` (`animalID`, `animalName`, `animalType`, `animalBreed`, `animalAge`, `animalGender`, `animalSize`, `animalPhoto`, `animalStatus`, `userID`) VALUES
(1, 'Toby', 'Dog', 'Black Lab', 3, 'Male', 'Medium', 'Toby.jpg', 'Available', NULL),
(2, 'Charlie', 'Cat', 'domestic shorthair', 3, 'Male', 'Small', 'charlie.jpg', 'New Intake', NULL),
(3, 'Kenzi', 'Dog', 'Husky', 8, 'Female', 'Large', 'kenzi.jpg', 'Adopted', 1),
(4, 'Milo', 'Dog', 'shih tzu', 7, 'Male', 'Small', 'milo.jpg', 'Regular Patient', 2),
(5, 'Lucy', 'Dog', 'Golden Retriever', 9, 'Female', 'Large', 'lucy.jpg', 'Available', NULL),
(6, 'Gibson', 'Dog', 'Lab', 4, 'Male', 'Medium', 'noPhoto.jpg', 'Available', NULL),
(7, 'Molly', 'Cat', 'domestic longhair', 10, 'Female', 'Small', 'molly.jpg', 'Available', NULL),
(8, 'Tom', 'Cat', 'domestic shorthair', 2, 'Male', 'Small', 'noPhoto.jpg', 'Available', NULL),
(9, 'Fish', 'Cat', 'domestic shorthair', 1, 'Male', 'Small', 'fish.jpg', 'Adopted', 3),
(10, 'Rex', 'Dog', 'German Shepherd', 1, 'Male', 'Large', 'rex.jpg', 'Adopted', 4);

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE IF NOT EXISTS `events` (
  `eventID` int(10) NOT NULL AUTO_INCREMENT,
  `eventType` varchar(50) NOT NULL,
  `eventScheduleDate` date NOT NULL,
  `eventCompletedDate` date NOT NULL,
  `eventName` varchar(150) NOT NULL,
  `eventResult` varchar(150) NOT NULL,
  `animalID` int(10) NOT NULL,
  `userID` int(10) NOT NULL,
  `transactionID` int(10) NOT NULL,
  PRIMARY KEY (`eventID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=35 ;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`eventID`, `eventType`, `eventScheduleDate`, `eventCompletedDate`, `eventName`, `eventResult`, `animalID`, `userID`, `transactionID`) VALUES
(1, 'check up', '2020-04-27', '2020-01-01', 'Annual Checkup', '', 1, 2, 3),
(2, 'procedure', '2020-04-29', '2020-01-01', 'Rabies test', 'negative', 2, 2, 3),
(34, 'Procedure', '2020-05-03', '2020-05-06', 'Heartworm test for Rex', 'negative', 10, 2, 0),
(33, 'Check up', '2020-05-03', '2020-05-06', 'Check up for Fish', '', 9, 3, 47),
(31, 'Meet & Greet', '2020-05-03', '2020-05-10', 'Meet Toby', '', 0, 2, 44),
(30, 'Meet & Greet', '2020-05-03', '2020-05-05', 'Meet Lucy', 'n/a', 5, 2, 43);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `transactionID` int(10) NOT NULL AUTO_INCREMENT,
  `transactionType` varchar(30) NOT NULL,
  `transactionAmount` decimal(5,2) NOT NULL,
  `userID` int(10) NOT NULL,
  `transactionDate` date NOT NULL,
  PRIMARY KEY (`transactionID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=50 ;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`transactionID`, `transactionType`, `transactionAmount`, `userID`, `transactionDate`) VALUES
(1, 'Donation', 50.00, 1, '2020-04-29'),
(2, 'Donation', 25.00, 2, '2020-05-03'),
(4, 'Donation', 30.00, 2, '2020-04-27'),
(5, 'Donation', 200.00, 2, '2020-04-30'),
(6, 'Donation', 125.00, 2, '2020-04-30'),
(7, 'Donation', 125.00, 2, '2020-04-30'),
(9, 'Donation', 100.00, 2, '2020-04-30'),
(47, 'Check up', 0.00, 3, '2020-05-03'),
(49, 'Donation', 10.00, 2, '2020-05-03'),
(48, 'Procedure', 0.00, 2, '2020-05-03'),
(46, 'Donation', 999.99, 3, '2020-05-03'),
(43, 'Meet & Greet', 0.00, 2, '2020-05-03'),
(44, 'Meet & Greet', 0.00, 2, '2020-05-03'),
(37, 'Adoption', 150.00, 4, '2020-05-03');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `userType` varchar(25) NOT NULL,
  `userPassword` varchar(50) NOT NULL,
  `userFName` varchar(50) NOT NULL,
  `userLName` varchar(50) NOT NULL,
  `userEmail` varchar(100) NOT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `userType`, `userPassword`, `userFName`, `userLName`, `userEmail`) VALUES
(1, 'customer', '123123', 'John', 'Smith', 'js@g.com'),
(2, 'employee', '000000', 'Megan', 'Jones', 'mj@gmail.com'),
(3, 'customer', '131313', 'Kenai', 'Jones', 'kj@g.com'),
(4, 'customer', '123456', 'Raili', 'Utiger', 'ru@g.com');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
