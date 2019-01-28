

-- create/recreate database
DROP DATABASE IF EXISTS serious_project_1;
CREATE DATABASE serious_project_1;
USE serious_project_1;

CREATE TABLE supplier (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    address VARCHAR(256) NOT NULL,
    phone VARCHAR(10) NOT NULL
);


CREATE TABLE item (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    supplier_id INT NOT NULL,
    cost DECIMAL NOT NULL,
    CONSTRAINT item_fk_supplier FOREIGN KEY (supplier_id)
        REFERENCES supplier (id)
);


CREATE TABLE inventory (
    item_id INT NOT NULL,
    supplier_id INT NOT NULL,
    count INT NOT NULL,
    PRIMARY KEY (item_id , supplier_id),
    CONSTRAINT inventory_fk_item FOREIGN KEY (item_id)
        REFERENCES item (id),
    CONSTRAINT inventory_fk_supplier FOREIGN KEY (supplier_id)
        REFERENCES supplier (id)
);

-- add suppliers
insert into supplier (name, address, phone)
values 
("Big 5",          "2140 Cleveland Ave #104, Madera, CA 93637", "5596742159"),
("Target",         "3280 R St, Merced, CA 95348",               "2097253482"),
("CVS",            "4077 W Clinton Ave, Fresno, CA 93722",      "5592713177"),
("AutoZone",       "3785 W Shields Ave, Fresno, CA 93722",      "5592773744"),
("Party City",     "4320 W Shaw Ave, Fresno, CA 93722",         "5592757767"),
("Barnes & Noble", "1720 W Olive Ave, Merced, CA 95348",        "2093860571");


-- add items
insert into item (name, supplier_id, cost)
values
("Soccer Ball",          1,   15.00),
("Boonie Hat",           1,   19.99),
("LED TV",               2,  399.99),
("Centrum Multivitamin", 3,   10.49),
("Oil Filter",           4,    9.99),
("Red Balloons",         5,    4.99);


-- add inventory
