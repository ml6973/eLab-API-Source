DROP DATABASE if EXISTS eLabAPI;

CREATE DATABASE eLabAPI;
USE eLabAPI;

DROP TABLE if EXISTS Users;
CREATE TABLE Users (
  userId             int(11) UNIQUE NOT NULL AUTO_INCREMENT,
  userName           varchar (255) UNIQUE NOT NULL COLLATE utf8_unicode_ci,
  authentication     varchar (255) UNIQUE NOT NULL COLLATE utf8_unicode_ci,
  dateCreated        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (userId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE if EXISTS Images;   
CREATE TABLE Images (
  imageId            int(11) UNIQUE NOT NULL,
  description        varchar (255) NOT NULL COLLATE utf8_unicode_ci,
  dateCreated        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (imageId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE if EXISTS Instances;  
CREATE TABLE Instances (
  instanceId         int(11) UNIQUE NOT NULL AUTO_INCREMENT,
  userId             int(11) UNIQUE NOT NULL,
  imageId            int(11) NOT NULL,
  computeId          varchar(255) UNIQUE COLLATE utf8_unicode_ci,
  ipaddr             varchar(255) UNIQUE COLLATE utf8_unicode_ci,
  dateCreated        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (instanceId),
  FOREIGN KEY (userId) REFERENCES Users(userId),
  FOREIGN KEY (imageId) REFERENCES Images(imageId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO Users (userId, userName, authentication) VALUES 
	(1, 'Gonzpaulo', 'valid');

INSERT INTO Images (imageId, description) VALUES
	(1, 'Dummy Image');  
 
INSERT INTO Instances (instanceId, userId,  imageId, computeId, ipaddr) VALUES 
	   (1, 1, 1, 'myComputeId', '127.0.0.1');
