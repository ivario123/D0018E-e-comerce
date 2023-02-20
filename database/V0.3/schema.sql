-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema first_test
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema first_test
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `first_test` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `first_test` ;

-- -----------------------------------------------------
-- Table `first_test`.`PRODUCT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`PRODUCT` (
  `SN` INT NOT NULL AUTO_INCREMENT,
  `ProductName` VARCHAR(45) NOT NULL,
  `Inventory` INT NOT NULL,
  `Price` INT NOT NULL,
  `ProductDescription` VARCHAR(1000) NOT NULL,
  `Image` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`SN`),
  UNIQUE INDEX `SN_UNIQUE` (`SN` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 53
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `first_test`.`USER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`USER` (
  `Email` VARCHAR(45) NOT NULL,
  `UserName` VARCHAR(45) NOT NULL,
  `Password` VARCHAR(1000) NOT NULL,
  `Name` VARCHAR(45) NOT NULL,
  `Surname` VARCHAR(45) NOT NULL,
  `Role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Email`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `first_test`.`BASKET`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`BASKET` (
  `SN` INT NOT NULL,
  `Amount` INT NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `Email` (`Email` ASC, `SN` ASC) VISIBLE,
  INDEX `fk_BASKET_PRODUCT_idx` (`SN` ASC) VISIBLE,
  INDEX `fk_BASKET_USER1` (`Email` ASC) VISIBLE,
  CONSTRAINT `fk_BASKET_PRODUCT`
    FOREIGN KEY (`SN`)
    REFERENCES `first_test`.`PRODUCT` (`SN`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_BASKET_USER1`
    FOREIGN KEY (`Email`)
    REFERENCES `first_test`.`USER` (`Email`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `first_test`.`SUPERCATEGORY`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`SUPERCATEGORY` (
  `Name` VARCHAR(45) NOT NULL,
  `Color` VARCHAR(45) NOT NULL DEFAULT 'primary',
  PRIMARY KEY (`Name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `first_test`.`CATEGORY`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`CATEGORY` (
  `Name` VARCHAR(45) NOT NULL,
  `Super` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`Name`),
  INDEX `fk_CATEGORY_SUPERCATEGORY1_idx` (`Super` ASC) VISIBLE,
  CONSTRAINT `fk_CATEGORY_SUPERCATEGORY1`
    FOREIGN KEY (`Super`)
    REFERENCES `first_test`.`SUPERCATEGORY` (`Name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `first_test`.`CATEGORY_ASSIGN`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`CATEGORY_ASSIGN` (
  `Category` VARCHAR(45) NOT NULL,
  `SN` INT NOT NULL,
  INDEX `fk_CATERGORY_ASSIGN_CATEGORY1_idx` (`Category` ASC) VISIBLE,
  INDEX `fk_CATERGORY_ASSIGN_PRODUCT1` (`SN` ASC) VISIBLE,
  CONSTRAINT `fk_CATERGORY_ASSIGN_CATEGORY1`
    FOREIGN KEY (`Category`)
    REFERENCES `first_test`.`CATEGORY` (`Name`),
  CONSTRAINT `fk_CATERGORY_ASSIGN_PRODUCT1`
    FOREIGN KEY (`SN`)
    REFERENCES `first_test`.`PRODUCT` (`SN`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `first_test`.`PARCEL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`PARCEL` (
  `NR` INT NOT NULL AUTO_INCREMENT,
  `Status` INT NOT NULL DEFAULT '0',
  `Address` VARCHAR(45) NOT NULL,
  `Zip` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`NR`))
ENGINE = InnoDB
AUTO_INCREMENT = 23
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `first_test`.`REVIEW`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`REVIEW` (
  `SN` INT NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Rating` INT NOT NULL,
  `Text` VARCHAR(1000) NOT NULL,
  PRIMARY KEY (`SN`, `Email`),
  INDEX `fk_REVIEW_USER1_idx` (`Email` ASC) VISIBLE,
  INDEX `fk_REVIEW_PRODUCT1` (`SN` ASC) VISIBLE,
  CONSTRAINT `fk_REVIEW_PRODUCT1`
    FOREIGN KEY (`SN`)
    REFERENCES `first_test`.`PRODUCT` (`SN`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_REVIEW_USER1`
    FOREIGN KEY (`Email`)
    REFERENCES `first_test`.`USER` (`Email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `first_test`.`USERORDER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `first_test`.`USERORDER` (
  `Email` VARCHAR(45) NOT NULL,
  `SN` INT NOT NULL,
  `Amount` INT NOT NULL,
  `NR` INT NOT NULL AUTO_INCREMENT,
  `PARCEL` INT NOT NULL,
  `Price` INT NOT NULL,
  PRIMARY KEY (`NR`),
  INDEX `fk_ORDER_USER1_idx` (`Email` ASC) VISIBLE,
  INDEX `fk_ORDER_PRODUCT1_idx` (`SN` ASC) VISIBLE,
  INDEX `fk_USERORDER_PARCEL1_idx` (`PARCEL` ASC) VISIBLE,
  CONSTRAINT `fk_ORDER_PRODUCT1`
    FOREIGN KEY (`SN`)
    REFERENCES `first_test`.`PRODUCT` (`SN`),
  CONSTRAINT `fk_ORDER_USER1`
    FOREIGN KEY (`Email`)
    REFERENCES `first_test`.`USER` (`Email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_USERORDER_PARCEL1`
    FOREIGN KEY (`PARCEL`)
    REFERENCES `first_test`.`PARCEL` (`NR`))
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
