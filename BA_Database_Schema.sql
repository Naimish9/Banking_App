USE Bank_Sch;
drop table acc_info;
CREATE TABLE `Bank_Sch`.`acc_info` (
  `acc_no` INT NOT NULL,
  `user_name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `aadhar_no` BIGINT(16) NOT NULL,
  `mobile_no` INT(10) NOT NULL,
  `acc_pwd` VARCHAR(45) NOT NULL,
  `acc_balance` DECIMAL(9.2) NOT NULL,
  PRIMARY KEY (`user_name`),  
  UNIQUE INDEX `acc_no_UNIQUE` (`acc_no` ASC) VISIBLE,
  UNIQUE INDEX `aadhar_no_UNIQUE` (`aadhar_no` ASC) VISIBLE,
  UNIQUE INDEX `mobile_no_UNIQUE` (`mobile_no` ASC) VISIBLE,
  UNIQUE INDEX `acc_pwd_UNIQUE` (`acc_pwd` ASC) VISIBLE);

-- DROP table acc_info;

DESC acc_info;

drop table Benf;

CREATE TABLE `Bank_Sch`.`Benf` (
  `user_name` VARCHAR(45) NOT NULL,
  `benf_name` VARCHAR(45) NOT NULL,
  `Benf_acc_no` INT NOT NULL,
  `Benf_ifsc` VARCHAR(45) NOT NULL,
  INDEX `fk_Benf_1_idx` (`user_name` ASC) VISIBLE,
  CONSTRAINT `fk_user_name`
    FOREIGN KEY (`user_name`)
    REFERENCES `Bank_Sch`.`acc_info` (`user_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- DESC Benf;

drop table card;

CREATE TABLE `Bank_Sch`.`card` (
  `user_name` VARCHAR(45) NOT NULL,
  `card_no` BIGINT(16) NOT NULL,
  `card_type` VARCHAR(45) NOT NULL,
  `pin` INT(4) NOT NULL,
  `cvv` INT(3) NOT NULL,
  UNIQUE INDEX `card_no_UNIQUE` (`card_no` ASC) VISIBLE,
  UNIQUE INDEX `pin_UNIQUE` (`pin` ASC) VISIBLE,
  UNIQUE INDEX `cvv_UNIQUE` (`cvv` ASC) VISIBLE,
  INDEX `fk_user_name_idx` (`user_name` ASC) VISIBLE,
  CONSTRAINT `fk_user_name_card`
    FOREIGN KEY (`user_name`)
    REFERENCES `Bank_Sch`.`acc_info` (`user_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- DESC card;