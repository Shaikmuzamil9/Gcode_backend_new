-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 07, 2026 at 03:34 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gcode_transmitter`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `action` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `data_transfers`
--

CREATE TABLE `data_transfers` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `gcode_id` int(11) NOT NULL,
  `status` varchar(50) DEFAULT 'pending',
  `started_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `device_name` varchar(255) NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `registered_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `gcodes`
--

CREATE TABLE `gcodes` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `gcode_path` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `gcodes`
--

INSERT INTO `gcodes` (`id`, `user_id`, `name`, `gcode_path`, `created_at`) VALUES
(1, 1, 'GCode_20260103_123909', '/uploads/gcodes/a32ff7ab-f7e2-432c-96e0-ace95e8270e4.gcode', '2026-01-03 07:09:09'),
(2, 1, 'GCode_20260103_130447', '/uploads/gcodes/0ae700d1-edd5-46d4-825d-361150f76412.gcode', '2026-01-03 07:34:47'),
(3, 1, 'GCode_20260103_130624', '/uploads/gcodes/d997a2a9-5768-4832-802c-0e61dad3719f.gcode', '2026-01-03 07:36:24'),
(4, 1, 'GCode_20260103_132218', '/uploads/gcodes/268f81d9-89ff-4ffc-aaea-8f38ce176161.gcode', '2026-01-03 07:52:18'),
(5, 1, 'GCode_20260103_133414', '/uploads/gcodes/0e0245f2-f516-46a3-8e3b-518eaeded3c2.gcode', '2026-01-03 08:04:14'),
(6, 1, 'GCode_20260103_133722', '/uploads/gcodes/ce681dd7-352d-4264-86dc-8719a4472144.gcode', '2026-01-03 08:07:22'),
(7, 1, 'GCode_20260103_133747', '/uploads/gcodes/aaf737d5-c7aa-46ff-ab05-30ab53bf085b.gcode', '2026-01-03 08:07:47'),
(8, 1, 'GCode_20260103_134929', '/uploads/gcodes/d1bab4bc-836f-442d-ad92-c7e55145db1c.gcode', '2026-01-03 08:19:29'),
(9, 1, 'GCode_20260103_135011', '/uploads/gcodes/23a19bbd-e1ee-45b5-8420-8b4cfd30d675.gcode', '2026-01-03 08:20:11'),
(26, 2, 'GCode_20260105_133116', '/uploads/images/../gcodes/a531dc31-75f0-48af-bf0f-3d4e8b941468.gcode', '2026-01-05 08:01:16'),
(27, 2, 'GCode_20260105_133806', '/uploads/images/../gcodes/e0a214d5-8a71-4bdd-ac6e-e58cb387393a.gcode', '2026-01-05 08:08:06'),
(28, 2, 'GCode_20260105_134502', '/uploads/images/../gcodes/eba8d738-2c8a-4452-83a0-9b3714c75f05.gcode', '2026-01-05 08:15:02'),
(29, 2, 'GCode_20260105_135328', '/uploads/images/../gcodes/263ef54a-9729-4c41-a205-87d018517dac.gcode', '2026-01-05 08:23:28'),
(30, 2, 'GCode_20260105_141447', '/uploads/images/../gcodes/4d953b7d-1a99-4ddd-8ad6-0ef43d76b076.gcode', '2026-01-05 08:44:47'),
(31, 2, 'GCode_20260105_143621', '/uploads/images/../gcodes/79d43d9a-5d2b-4f59-888e-628a8f6ad9d5.gcode', '2026-01-05 09:06:21'),
(32, 2, 'GCode_20260105_143808', '/uploads/images/../gcodes/d09ab9d7-1d2b-4317-892e-cc533760677e.gcode', '2026-01-05 09:08:08'),
(33, 2, 'GCode_20260105_144444', '/uploads/images/../gcodes/aadf6356-f2d9-4b9c-a509-a2533ecc5df3.gcode', '2026-01-05 09:14:44'),
(34, 2, 'GCode_20260105_144831', '/uploads/images/../gcodes/5ed789bb-aa18-4346-be7b-bdbb42797c69.gcode', '2026-01-05 09:18:31'),
(35, 2, 'GCode_20260105_145239', '/uploads/images/../gcodes/fd840a92-46f1-490a-bbec-77ab36c16c72.gcode', '2026-01-05 09:22:39'),
(36, 2, 'GCode_20260105_160053', '/uploads/images/../gcodes/bceaf869-0dbc-4377-9fc6-f8b3f99cd411.gcode', '2026-01-05 10:30:53'),
(37, 2, 'GCode_20260105_160147', '/uploads/images/../gcodes/0589e577-c838-43be-a20b-e3ca8ae6185f.gcode', '2026-01-05 10:31:47'),
(38, 2, 'GCode_20260105_161307', '/uploads/images/../gcodes/dd0be1af-59f2-415c-a71a-7ba96c2456b1.gcode', '2026-01-05 10:43:07'),
(39, 2, 'GCode_20260105_163840', '/uploads/images/../gcodes/9ba06a64-26ef-4b92-90a7-91c4058008b8.gcode', '2026-01-05 11:08:40'),
(40, 2, 'GCode_20260105_164143', '/uploads/images/../gcodes/429f3f41-a929-4ec0-8679-9e30f78c5fbf.gcode', '2026-01-05 11:11:43'),
(41, 2, 'GCode_20260105_164834', '/uploads/images/../gcodes/8344b861-f95f-4c77-8b40-387f5a7fb147.gcode', '2026-01-05 11:18:34'),
(42, 2, 'GCode_20260105_165441', '/uploads/images/../gcodes/e78d7634-1e11-448a-bdfa-e6bdf246249f.gcode', '2026-01-05 11:24:41'),
(43, 2, 'GCode_20260105_171542', '/uploads/images/../gcodes/8563682c-278e-4eac-81b1-9db2f5d75191.gcode', '2026-01-05 11:45:42'),
(44, 2, 'GCode_20260105_173051', '/uploads/images/../gcodes/54b9772a-c11d-4d14-b201-e4f33fb56b4f.gcode', '2026-01-05 12:00:51'),
(45, 2, 'GCode_20260105_191425', '/uploads/images/../gcodes/1048bf81-4343-4757-82a6-0ce659cb6f98.gcode', '2026-01-05 13:44:25');

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `setting_key` varchar(255) NOT NULL,
  `setting_value` text DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `reset_token` varchar(255) DEFAULT NULL,
  `reset_token_expiry` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `reset_token`, `reset_token_expiry`, `created_at`) VALUES
(1, 'shaik', 'shaik@gmail.com', '$2b$12$z1x1IeiQSeiA./tqFtem0ONqWsjAkOuWguJkwUlfNBdKatgpA/llm', NULL, NULL, '2026-01-03 06:12:03'),
(2, 'muzzu', 'muzzushaik1619@gmail.com', '$2b$12$VNhrdfNWt2xliwPw/AHg/.qUT7NJJ.G/mNOiYhnUFmrb2qBRIlA7.', NULL, NULL, '2026-01-05 07:01:11'),
(3, 'akshith', 'akshith9398@gmail.com', '$2b$12$1qqWFQSwGvJK90Xnu5HK/u8Uxe6fGowEbiDC9I26dVjEFkbayhHGS', '6760', '2026-01-05 19:27:18', '2026-01-05 13:47:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `data_transfers`
--
ALTER TABLE `data_transfers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `gcodes`
--
ALTER TABLE `gcodes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_setting` (`user_id`,`setting_key`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `data_transfers`
--
ALTER TABLE `data_transfers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gcodes`
--
ALTER TABLE `gcodes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `images`
--
ALTER TABLE `images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `settings`
--
ALTER TABLE `settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `fk_activity_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `data_transfers`
--
ALTER TABLE `data_transfers`
  ADD CONSTRAINT `fk_transfers_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `fk_devices_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `gcodes`
--
ALTER TABLE `gcodes`
  ADD CONSTRAINT `fk_gcodes_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `fk_images_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `permissions`
--
ALTER TABLE `permissions`
  ADD CONSTRAINT `fk_permissions_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `settings`
--
ALTER TABLE `settings`
  ADD CONSTRAINT `fk_settings_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
