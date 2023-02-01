-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;

SET
    @OLD_FOREIGN_KEY_CHECKS = @ @FOREIGN_KEY_CHECKS,
    FOREIGN_KEY_CHECKS = 0;

SET
    @OLD_SQL_MODE = @ @SQL_MODE,
    SQL_MODE = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------

-- Schema mydb

-- -----------------------------------------------------

-- -----------------------------------------------------

-- Schema first_test

-- -----------------------------------------------------

DROP SCHEMA IF EXISTS `first_test` ;

-- -----------------------------------------------------

-- Schema first_test

-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `first_test` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE `first_test` ;

-- -----------------------------------------------------

-- Table `first_test`.`PRODUCT`

-- -----------------------------------------------------

DROP TABLE IF EXISTS `first_test`.`PRODUCT` ;

CREATE TABLE
    IF NOT EXISTS `first_test`.`PRODUCT` (
        `SN` INT NOT NULL AUTO_INCREMENT,
        `ProductName` VARCHAR(45) NOT NULL,
        `Inventory` INT NOT NULL,
        `Price` INT NOT NULL,
        `ProductDescription` VARCHAR(1000) NOT NULL,
        `Image` VARCHAR(200) NOT NULL,
        PRIMARY KEY (`SN`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 42 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE UNIQUE INDEX `SN_UNIQUE` ON `first_test`.`PRODUCT` (`SN` ASC) VISIBLE;

-- -----------------------------------------------------

-- Table `first_test`.`USER`

-- -----------------------------------------------------

DROP TABLE IF EXISTS `first_test`.`USER` ;

CREATE TABLE
    IF NOT EXISTS `first_test`.`USER` (
        `Email` VARCHAR(45) NOT NULL,
        `UserName` VARCHAR(45) NOT NULL,
        `Password` VARCHAR(1000) NOT NULL,
        `Name` VARCHAR(45) NOT NULL,
        `Surname` VARCHAR(45) NOT NULL,
        `Role` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`Email`)
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------

-- Table `first_test`.`BASKET`

-- -----------------------------------------------------

DROP TABLE IF EXISTS `first_test`.`BASKET` ;

CREATE TABLE
    IF NOT EXISTS `first_test`.`BASKET` (
        `SN` INT NOT NULL,
        `Amount` INT NOT NULL,
        `Email` VARCHAR(45) NOT NULL,
        CONSTRAINT `fk_BASKET_PRODUCT` FOREIGN KEY (`SN`) REFERENCES `first_test`.`PRODUCT` (`SN`) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT `fk_BASKET_USER1` FOREIGN KEY (`Email`) REFERENCES `first_test`.`USER` (`Email`)
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX
    `fk_BASKET_PRODUCT_idx` ON `first_test`.`BASKET` (`SN` ASC) VISIBLE;

CREATE INDEX
    `fk_BASKET_USER1` ON `first_test`.`BASKET` (`Email` ASC) VISIBLE;

-- -----------------------------------------------------

-- Table `first_test`.`SUPERCATEGORY`

-- -----------------------------------------------------

DROP TABLE IF EXISTS `first_test`.`SUPERCATEGORY` ;

CREATE TABLE
    IF NOT EXISTS `first_test`.`SUPERCATEGORY` (
        `Name` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`Name`)
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------

-- Table `first_test`.`CATEGORY`

-- -----------------------------------------------------

DROP TABLE IF EXISTS `first_test`.`CATEGORY` ;

CREATE TABLE
    IF NOT EXISTS `first_test`.`CATEGORY` (
        `Name` VARCHAR(45) NOT NULL,
        `Super` VARCHAR(45) NULL DEFAULT NULL,
        PRIMARY KEY (`Name`),
        CONSTRAINT `fk_CATEGORY_SUPERCATEGORY1` FOREIGN KEY (`Super`) REFERENCES `first_test`.`SUPERCATEGORY` (`Name`)
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX
    `fk_CATEGORY_SUPERCATEGORY1_idx` ON `first_test`.`CATEGORY` (`Super` ASC) VISIBLE;

-- -----------------------------------------------------

-- Table `first_test`.`CATEGORY_ASSIGN`

-- -----------------------------------------------------

DROP TABLE IF EXISTS `first_test`.`CATEGORY_ASSIGN` ;

CREATE TABLE
    IF NOT EXISTS `first_test`.`CATEGORY_ASSIGN` (
        `Category` VARCHAR(45) NOT NULL,
        `SN` INT NOT NULL,
        CONSTRAINT `fk_CATERGORY_ASSIGN_CATEGORY1` FOREIGN KEY (`Category`) REFERENCES `first_test`.`CATEGORY` (`Name`),
        CONSTRAINT `fk_CATERGORY_ASSIGN_PRODUCT1` FOREIGN KEY (`SN`) REFERENCES `first_test`.`PRODUCT` (`SN`)
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX
    `fk_CATERGORY_ASSIGN_CATEGORY1_idx` ON `first_test`.`CATEGORY_ASSIGN` (`Category` ASC) VISIBLE;

CREATE INDEX
    `fk_CATERGORY_ASSIGN_PRODUCT1` ON `first_test`.`CATEGORY_ASSIGN` (`SN` ASC) VISIBLE;

-- -----------------------------------------------------

-- Table `first_test`.`ORDER`

-- -----------------------------------------------------

DROP TABLE IF EXISTS `first_test`.`ORDER` ;

CREATE TABLE
    IF NOT EXISTS `first_test`.`ORDER` (
        `Email` VARCHAR(45) NOT NULL,
        `SN` INT NOT NULL,
        `Amount` INT NOT NULL,
        `NR` INT NOT NULL AUTO_INCREMENT,
        `Address` VARCHAR(100) NOT NULL,
        `ZipCode` INT NOT NULL,
        `Status` INT NOT NULL DEFAULT 0,
        PRIMARY KEY (`NR`),
        CONSTRAINT `fk_ORDER_PRODUCT1` FOREIGN KEY (`SN`) REFERENCES `first_test`.`PRODUCT` (`SN`),
        CONSTRAINT `fk_ORDER_USER1` FOREIGN KEY (`Email`) REFERENCES `first_test`.`USER` (`Email`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX
    `fk_ORDER_USER1_idx` ON `first_test`.`ORDER` (`Email` ASC) VISIBLE;

CREATE INDEX
    `fk_ORDER_PRODUCT1_idx` ON `first_test`.`ORDER` (`SN` ASC) VISIBLE;

-- -----------------------------------------------------

-- Table `first_test`.`REVIEW`

-- -----------------------------------------------------

DROP TABLE IF EXISTS `first_test`.`REVIEW` ;

CREATE TABLE
    IF NOT EXISTS `first_test`.`REVIEW` (
        `SN` INT NOT NULL,
        `Email` VARCHAR(45) NOT NULL,
        `Rating` INT NOT NULL,
        `Text` VARCHAR(1000) NOT NULL,
        PRIMARY KEY (`SN`, `Email`),
        CONSTRAINT `fk_REVIEW_PRODUCT1` FOREIGN KEY (`SN`) REFERENCES `first_test`.`PRODUCT` (`SN`) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT `fk_REVIEW_USER1` FOREIGN KEY (`Email`) REFERENCES `first_test`.`USER` (`Email`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX
    `fk_REVIEW_USER1_idx` ON `first_test`.`REVIEW` (`Email` ASC) VISIBLE;

CREATE INDEX
    `fk_REVIEW_PRODUCT1` ON `first_test`.`REVIEW` (`SN` ASC) VISIBLE;

SET SQL_MODE=@OLD_SQL_MODE;

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;

SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;