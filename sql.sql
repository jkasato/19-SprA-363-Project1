-- create/recreate database
DROP DATABASE IF EXISTS serious_project_1;


CREATE DATABASE serious_project_1;
USE serious_project_1;


CREATE TABLE item (
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(64) NOT NULL
);


CREATE TABLE supplier (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(64) NOT NULL,
    `address` VARCHAR(256) NOT NULL,
    `phone` VARCHAR(10) NOT NULL
);



CREATE TABLE catalog (
    `item_id` INT NOT NULL,
    `supplier_id` INT NOT NULL,
    `price` DOUBLE NOT NULL,
    `discontinued` BOOL NOT NULL DEFAULT FALSE,
    PRIMARY KEY (`item_id`, `supplier_id`),
    CONSTRAINT catalog_fk_supplier FOREIGN KEY (`supplier_id`)
        REFERENCES supplier (`id`),
	CONSTRAINT catalog_fk_item FOREIGN KEY (`item_id`)
        REFERENCES item (`id`)
);


CREATE TABLE inventory (
    `item_id` INT NOT NULL PRIMARY KEY,
    `need` INT NOT NULL DEFAULT 0,
    `have` INT NOT NULL DEFAULT 0,
    CONSTRAINT inventory_fk_item FOREIGN KEY (item_id)
        REFERENCES item (id)
);


-- add items
INSERT INTO item (name)
VALUES 
	("Soccer Ball"),
    ("Hat"),
    ("LED TV"),
    ("Multivitamin"),
    ("Oil Filter"),
    ("Red Balloons");


-- add suppliers
INSERT INTO supplier (`name`, `address`, `phone`)
VALUES 
("Big 5",          "2140 Cleveland Ave #104, Madera, CA 93637", "5596742159"),
("Target",         "3280 R St, Merced, CA 95348",               "2097253482"),
("CVS",            "4077 W Clinton Ave, Fresno, CA 93722",      "5592713177"),
("AutoZone",       "3785 W Shields Ave, Fresno, CA 93722",      "5592773744"),
("Party City",     "4320 W Shaw Ave, Fresno, CA 93722",         "5592757767"),
("Barnes & Noble", "1720 W Olive Ave, Merced, CA 95348",        "2093860571");


-- add catalog items
INSERT INTO catalog (`item_id`, `supplier_id`, `price`)
VALUES
(1, 1,  15.00),
(2, 1,  19.99),
(3, 2, 399.99),
(4, 3,  10.49),
(5, 4,   9.99),
(6, 5,   4.99);

-- add inventory
INSERT INTO inventory (`item_id`, `need`)
VALUES
(1,  2),
(3,  1),
(4,  3),
(5,  2),
(6, 99);
