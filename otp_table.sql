-- OTP Table for Email Verification

CREATE TABLE IF NOT EXISTS `otps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `otp_code` varchar(10) NOT NULL,
  `expiry_time` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `email` (`email`),
  KEY `otp_code` (`otp_code`),
  KEY `expiry_time` (`expiry_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
