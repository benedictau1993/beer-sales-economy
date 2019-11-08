USE `beer` ;

ALTER TABLE `beer`.`beer_type` 
CHANGE COLUMN `beer_type_name` `beer_type_name` TEXT NOT NULL ,
CHANGE COLUMN `beer_type_id` `beer_type_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`beer_type_id`);

ALTER TABLE `beer`.`flavor` 
CHANGE COLUMN `flavor_name` `flavor_name` TEXT NOT NULL ,
CHANGE COLUMN `flavor_id` `flavor_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`flavor_id`);

ALTER TABLE `beer`.`market` 
CHANGE COLUMN `market_name` `market_name` TEXT NOT NULL ,
CHANGE COLUMN `market_id` `market_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`market_id`);

ALTER TABLE `beer`.`outlet_cat` 
CHANGE COLUMN `outlet_cat_name` `outlet_cat_name` TEXT NOT NULL ,
CHANGE COLUMN `outlet_cat_id` `outlet_cat_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`outlet_cat_id`);

ALTER TABLE `beer`.`packaging` 
CHANGE COLUMN `packaging_name` `packaging_name` TEXT NOT NULL ,
CHANGE COLUMN `packaging_id` `packaging_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`packaging_id`);

ALTER TABLE `beer`.`vendor` 
CHANGE COLUMN `vendor_name` `vendor_name` TEXT NOT NULL ,
CHANGE COLUMN `vendor_id` `vendor_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`vendor_id`);

ALTER TABLE `beer`.`week` 
CHANGE COLUMN `date` `date` DATETIME NOT NULL ,
CHANGE COLUMN `week_id` `week_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`week_id`);

ALTER TABLE `beer`.`store` 
CHANGE COLUMN `store_id` `store_id` BIGINT(20) NOT NULL ,
CHANGE COLUMN `outlet_cat_name` `outlet_cat_id` BIGINT(20) NOT NULL ,
CHANGE COLUMN `market_name` `market_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`store_id`),
ADD INDEX `outlet_cat_id_idx` (`outlet_cat_id` ASC) VISIBLE,
ADD INDEX `market_id_idx` (`market_id` ASC) VISIBLE;

ALTER TABLE `beer`.`store` 
ADD CONSTRAINT `outlet_cat_id`
  FOREIGN KEY (`outlet_cat_id`)
  REFERENCES `beer`.`outlet_cat` (`outlet_cat_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `market_id`
  FOREIGN KEY (`market_id`)
  REFERENCES `beer`.`market` (`market_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `beer`.`upc` 
CHANGE COLUMN `UPC` `UPC` TEXT NOT NULL ,
CHANGE COLUMN `SY` `SY` BIGINT(20) NOT NULL ,
CHANGE COLUMN `GE` `GE` BIGINT(20) NOT NULL ,
CHANGE COLUMN `VEND` `VEND` BIGINT(20) NOT NULL ,
CHANGE COLUMN `ITEM` `ITEM` BIGINT(20) NOT NULL ,
CHANGE COLUMN `vendor_id` `vendor_id` BIGINT(20) NOT NULL ,
CHANGE COLUMN `UPC_id` `UPC_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`UPC_id`),
ADD INDEX `vendor_id_idx` (`vendor_id` ASC) VISIBLE,
ADD INDEX `beer_type_id_idx` (`beer_type_id` ASC) VISIBLE,
ADD INDEX `packaging_id_idx` (`packaging_id` ASC) VISIBLE,
ADD INDEX `flavor_id_idx` (`flavor_id` ASC) VISIBLE;

ALTER TABLE `beer`.`upc` 
ADD CONSTRAINT `vendor_id`
  FOREIGN KEY (`vendor_id`)
  REFERENCES `beer`.`vendor` (`vendor_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `beer_type_id`
  FOREIGN KEY (`beer_type_id`)
  REFERENCES `beer`.`beer_type` (`beer_type_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `packaging_id`
  FOREIGN KEY (`packaging_id`)
  REFERENCES `beer`.`packaging` (`packaging_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `flavor_id`
  FOREIGN KEY (`flavor_id`)
  REFERENCES `beer`.`flavor` (`flavor_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

####################

ALTER TABLE `beer`.`sales` 
CHANGE COLUMN `store_id` `store_id` BIGINT(20) NOT NULL ,
CHANGE COLUMN `week_id` `week_id` BIGINT(20) NOT NULL ,
CHANGE COLUMN `UNITS` `UNITS` BIGINT(20) NOT NULL ,
CHANGE COLUMN `DOLLARS` `DOLLARS` DOUBLE NOT NULL ,
CHANGE COLUMN `upc_id` `upc_id` BIGINT(20) NOT NULL ;

ALTER TABLE `beer`.`sales` 
ADD INDEX `store_id_idx` (`store_id` ASC) VISIBLE;
;
ALTER TABLE `beer`.`sales` 
ADD CONSTRAINT `store_id`
  FOREIGN KEY (`store_id`)
  REFERENCES `beer`.`store` (`store_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `beer`.`sales` 
ADD INDEX `week_id_idx` (`week_id` ASC) VISIBLE;
;
ALTER TABLE `beer`.`sales` 
ADD CONSTRAINT `week_id`
  FOREIGN KEY (`week_id`)
  REFERENCES `beer`.`week` (`week_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

  ALTER TABLE `beer`.`sales` 
  ADD INDEX `upc_id_idx` (`upc_id` ASC) VISIBLE;
  ;
  ALTER TABLE `beer`.`sales` 
  ADD CONSTRAINT `upc_id`
    FOREIGN KEY (`upc_id`)
    REFERENCES `beer`.`upc` (`UPC_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

