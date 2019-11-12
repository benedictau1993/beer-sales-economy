-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema beer
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema beer
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `beer` DEFAULT CHARACTER SET utf8 ;
USE `beer` ;

-- -----------------------------------------------------
-- Table `beer`.`beer_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`beer_type` (
  `beer_type_cat` VARCHAR(45) NULL DEFAULT NULL,
  `beer_type_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`beer_type_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`week`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`week` (
  `date` DATE NOT NULL,
  `week_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`week_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`econ`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`econ` (
  `date` DATE NULL DEFAULT NULL,
  `IRLTLT01USM156N` DOUBLE NULL DEFAULT NULL,
  `CSUSHPISA` DOUBLE NULL DEFAULT NULL,
  `GDPC1` DOUBLE NULL DEFAULT NULL,
  `CPIAUCSL` DOUBLE NULL DEFAULT NULL,
  `USRECP` DOUBLE NULL DEFAULT NULL,
  `UNRATE` DOUBLE NULL DEFAULT NULL,
  `AKUR` DOUBLE NULL DEFAULT NULL,
  `AZUR` DOUBLE NULL DEFAULT NULL,
  `ARUR` DOUBLE NULL DEFAULT NULL,
  `CAUR` DOUBLE NULL DEFAULT NULL,
  `COUR` DOUBLE NULL DEFAULT NULL,
  `CTUR` DOUBLE NULL DEFAULT NULL,
  `DEUR` DOUBLE NULL DEFAULT NULL,
  `FLUR` DOUBLE NULL DEFAULT NULL,
  `GAUR` DOUBLE NULL DEFAULT NULL,
  `HIUR` DOUBLE NULL DEFAULT NULL,
  `IDUR` DOUBLE NULL DEFAULT NULL,
  `ILUR` DOUBLE NULL DEFAULT NULL,
  `INUR` DOUBLE NULL DEFAULT NULL,
  `IAUR` DOUBLE NULL DEFAULT NULL,
  `KSUR` DOUBLE NULL DEFAULT NULL,
  `KYUR` DOUBLE NULL DEFAULT NULL,
  `LAUR` DOUBLE NULL DEFAULT NULL,
  `MEUR` DOUBLE NULL DEFAULT NULL,
  `MDUR` DOUBLE NULL DEFAULT NULL,
  `MAUR` DOUBLE NULL DEFAULT NULL,
  `MIUR` DOUBLE NULL DEFAULT NULL,
  `MNUR` DOUBLE NULL DEFAULT NULL,
  `MSUR` DOUBLE NULL DEFAULT NULL,
  `MOUR` DOUBLE NULL DEFAULT NULL,
  `MTUR` DOUBLE NULL DEFAULT NULL,
  `NEUR` DOUBLE NULL DEFAULT NULL,
  `NVUR` DOUBLE NULL DEFAULT NULL,
  `NHUR` DOUBLE NULL DEFAULT NULL,
  `NJUR` DOUBLE NULL DEFAULT NULL,
  `NMUR` DOUBLE NULL DEFAULT NULL,
  `NYUR` DOUBLE NULL DEFAULT NULL,
  `NCUR` DOUBLE NULL DEFAULT NULL,
  `NDUR` DOUBLE NULL DEFAULT NULL,
  `OHUR` DOUBLE NULL DEFAULT NULL,
  `OKUR` DOUBLE NULL DEFAULT NULL,
  `ORUR` DOUBLE NULL DEFAULT NULL,
  `PAUR` DOUBLE NULL DEFAULT NULL,
  `RIUR` DOUBLE NULL DEFAULT NULL,
  `SCUR` DOUBLE NULL DEFAULT NULL,
  `SDUR` DOUBLE NULL DEFAULT NULL,
  `TNUR` DOUBLE NULL DEFAULT NULL,
  `TXUR` DOUBLE NULL DEFAULT NULL,
  `UTUR` DOUBLE NULL DEFAULT NULL,
  `VTUR` DOUBLE NULL DEFAULT NULL,
  `VAUR` DOUBLE NULL DEFAULT NULL,
  `WAUR` DOUBLE NULL DEFAULT NULL,
  `WVUR` DOUBLE NULL DEFAULT NULL,
  `WIUR` DOUBLE NULL DEFAULT NULL,
  `WYUR` DOUBLE NULL DEFAULT NULL,
  `econ_week_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`econ_week_id`),
  CONSTRAINT `econ_week_id`
    FOREIGN KEY (`econ_week_id`)
    REFERENCES `beer`.`week` (`week_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`flavor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`flavor` (
  `flavor_cat` VARCHAR(45) NULL DEFAULT NULL,
  `flavor_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`flavor_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`market`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`market` (
  `market_name` VARCHAR(45) NULL DEFAULT NULL,
  `region` VARCHAR(45) NULL DEFAULT NULL,
  `state` VARCHAR(45) NULL DEFAULT NULL,
  `city` VARCHAR(45) NULL DEFAULT NULL,
  `market_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`market_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`outlet_cat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`outlet_cat` (
  `outlet_cat_name` VARCHAR(45) NULL DEFAULT NULL,
  `outlet_cat_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`outlet_cat_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`packaging`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`packaging` (
  `packaging_cat` VARCHAR(45) NULL DEFAULT NULL,
  `packaging_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`packaging_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`store` (
  `store_id` BIGINT(20) NOT NULL,
  `outlet_cat_id` BIGINT(20) NOT NULL,
  `market_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`store_id`),
  INDEX `outlet_cat_id_idx` (`outlet_cat_id` ASC) VISIBLE,
  INDEX `market_id_idx` (`market_id` ASC) VISIBLE,
  CONSTRAINT `market_id`
    FOREIGN KEY (`market_id`)
    REFERENCES `beer`.`market` (`market_id`),
  CONSTRAINT `outlet_cat_id`
    FOREIGN KEY (`outlet_cat_id`)
    REFERENCES `beer`.`outlet_cat` (`outlet_cat_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`vendor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`vendor` (
  `vendor_name` VARCHAR(45) NULL DEFAULT NULL,
  `vendor_id` BIGINT(20) NOT NULL,
  PRIMARY KEY (`vendor_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`upc`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`upc` (
  `UPC` VARCHAR(45) NULL DEFAULT NULL,
  `SY` BIGINT(20) NULL DEFAULT NULL,
  `GE` BIGINT(20) NULL DEFAULT NULL,
  `VEND` BIGINT(20) NULL DEFAULT NULL,
  `ITEM` BIGINT(20) NULL DEFAULT NULL,
  `domestic` BIGINT(20) NULL DEFAULT NULL,
  `vendor_id` BIGINT(20) NULL DEFAULT NULL,
  `VOL_EQ` DOUBLE NULL DEFAULT NULL,
  `beer_type_id` BIGINT(20) NULL DEFAULT NULL,
  `packaging_id` BIGINT(20) NULL DEFAULT NULL,
  `flavor_id` BIGINT(20) NULL DEFAULT NULL,
  `UPC_id` BIGINT(20) NOT NULL,
  `total_vol_oz` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`UPC_id`),
  INDEX `vendor_id_idx` (`vendor_id` ASC) VISIBLE,
  INDEX `packaging_id_idx` (`packaging_id` ASC) VISIBLE,
  INDEX `flavor_id_idx` (`flavor_id` ASC) VISIBLE,
  INDEX `beer_type_id_idx` (`beer_type_id` ASC) VISIBLE,
  CONSTRAINT `beer_type_id`
    FOREIGN KEY (`beer_type_id`)
    REFERENCES `beer`.`beer_type` (`beer_type_id`),
  CONSTRAINT `flavor_id`
    FOREIGN KEY (`flavor_id`)
    REFERENCES `beer`.`flavor` (`flavor_id`),
  CONSTRAINT `packaging_id`
    FOREIGN KEY (`packaging_id`)
    REFERENCES `beer`.`packaging` (`packaging_id`),
  CONSTRAINT `vendor_id`
    FOREIGN KEY (`vendor_id`)
    REFERENCES `beer`.`vendor` (`vendor_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beer`.`sales`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beer`.`sales` (
  `store_id` BIGINT(20) NOT NULL,
  `week_id` BIGINT(20) NOT NULL,
  `UNITS` BIGINT(20) NOT NULL,
  `DOLLARS` DOUBLE NOT NULL,
  `upc_id` BIGINT(20) NOT NULL,
  `sales_id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`sales_id`),
  INDEX `store_id_idx` (`store_id` ASC) VISIBLE,
  INDEX `week_id_idx` (`week_id` ASC) VISIBLE,
  INDEX `upc_id_idx` (`upc_id` ASC) VISIBLE,
  CONSTRAINT `store_id`
    FOREIGN KEY (`store_id`)
    REFERENCES `beer`.`store` (`store_id`),
  CONSTRAINT `upc_id`
    FOREIGN KEY (`upc_id`)
    REFERENCES `beer`.`upc` (`UPC_id`),
  CONSTRAINT `week_id`
    FOREIGN KEY (`week_id`)
    REFERENCES `beer`.`week` (`week_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 660047
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
