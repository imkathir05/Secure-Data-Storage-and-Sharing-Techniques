-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 21, 2023 at 09:49 AM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 5.6.38

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blockchain_logistics`
--

-- --------------------------------------------------------

--
-- Table structure for table `cloud`
--

CREATE TABLE `cloud` (
  `cid` int(3) NOT NULL,
  `lid` varchar(10) NOT NULL,
  `lpass` varchar(10) NOT NULL,
  `cname` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cloud`
--

INSERT INTO `cloud` (`cid`, `lid`, `lpass`, `cname`) VALUES
(1, 'cloud', 'cloud', 'Cloud Server');

-- --------------------------------------------------------

--
-- Table structure for table `data_request`
--

CREATE TABLE `data_request` (
  `reqid` int(3) NOT NULL,
  `did` int(3) NOT NULL,
  `sid` int(3) NOT NULL,
  `dname` longtext NOT NULL,
  `rid` int(3) NOT NULL,
  `reqdate` varchar(25) NOT NULL,
  `reqtime` varchar(25) NOT NULL,
  `resdate` varchar(25) NOT NULL,
  `restime` varchar(25) NOT NULL,
  `skey` longtext NOT NULL,
  `reqstatus` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `logistics_data`
--

CREATE TABLE `logistics_data` (
  `did` int(3) NOT NULL,
  `sid` int(3) NOT NULL,
  `dname` varchar(250) NOT NULL,
  `dcontent` longtext NOT NULL,
  `hkey` longtext NOT NULL,
  `hsign` longtext NOT NULL,
  `date` varchar(15) NOT NULL,
  `time` varchar(15) NOT NULL,
  `adata` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `reciever`
--

CREATE TABLE `reciever` (
  `rid` int(3) NOT NULL,
  `rname` varchar(50) NOT NULL,
  `remail` varchar(100) NOT NULL,
  `rpass` varchar(10) NOT NULL,
  `rmno` varchar(10) NOT NULL,
  `raddress` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sender`
--

CREATE TABLE `sender` (
  `sid` int(3) NOT NULL,
  `sname` varchar(50) NOT NULL,
  `semail` varchar(100) NOT NULL,
  `spass` varchar(10) NOT NULL,
  `smno` varchar(10) NOT NULL,
  `saddress` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cloud`
--
ALTER TABLE `cloud`
  ADD PRIMARY KEY (`cid`);

--
-- Indexes for table `data_request`
--
ALTER TABLE `data_request`
  ADD PRIMARY KEY (`reqid`);

--
-- Indexes for table `logistics_data`
--
ALTER TABLE `logistics_data`
  ADD PRIMARY KEY (`did`);

--
-- Indexes for table `reciever`
--
ALTER TABLE `reciever`
  ADD PRIMARY KEY (`rid`);

--
-- Indexes for table `sender`
--
ALTER TABLE `sender`
  ADD PRIMARY KEY (`sid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cloud`
--
ALTER TABLE `cloud`
  MODIFY `cid` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `data_request`
--
ALTER TABLE `data_request`
  MODIFY `reqid` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `logistics_data`
--
ALTER TABLE `logistics_data`
  MODIFY `did` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `reciever`
--
ALTER TABLE `reciever`
  MODIFY `rid` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `sender`
--
ALTER TABLE `sender`
  MODIFY `sid` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
