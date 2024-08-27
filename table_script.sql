-- Table: 

CREATE TABLE `User` (
    user_ID INT PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(255),
    birthdate DATE,
    email VARCHAR(255) UNIQUE,
    `password` VARCHAR(255)
);

-- Table: Shop
CREATE TABLE Shop (
    shop_ID INT PRIMARY KEY,
    name VARCHAR(255)
);

-- Table: Seller (subclass of User)
CREATE TABLE Seller (
    user_ID INT PRIMARY KEY,
    shop_ID INT,
    FOREIGN KEY (user_ID) REFERENCES `User`(user_ID),
    FOREIGN KEY (shop_ID) REFERENCES Shop(shop_ID)
);

-- Table: Visitor
CREATE TABLE Visitor (
    temp_ID INT PRIMARY KEY
);

-- Table: Payment
CREATE TABLE Payment (
    transaction_ID INT PRIMARY KEY,
    PPemail VARCHAR(255)
);

-- Table: HasChat
CREATE TABLE HasChat (
    user_1 INT,
    user_2 INT,
    PRIMARY KEY (user_1, user_2),
    FOREIGN KEY (user_1) REFERENCES `User`(user_ID),
    FOREIGN KEY (user_2) REFERENCES `User`(user_ID)
);

-- Table: Product
CREATE TABLE Product (
    product_ID INT PRIMARY KEY,
    description TEXT,
    image LONGBLOB,
    name VARCHAR(255),
    price DECIMAL(10, 2)
);

-- Table: ProductShoe (subclass of Product)
CREATE TABLE ProductShoe (
    product_ID INT PRIMARY KEY,
    color VARCHAR(50),
    size DECIMAL(5, 2),
    material VARCHAR(255),
    gender VARCHAR(10),
    FOREIGN KEY (product_ID) REFERENCES Product(product_ID)
);

-- Table: ProductAccessories (subclass of Product)
CREATE TABLE ProductAccessories (
    product_ID INT PRIMARY KEY,
    type VARCHAR(50),
    gender VARCHAR(10),
    `usage` VARCHAR(255),
    FOREIGN KEY (product_ID) REFERENCES Product(product_ID)
);

-- Table: Wishlist
CREATE TABLE Wishlist (
    user_ID INT,
    product_ID INT,
    PRIMARY KEY (user_ID, product_ID),
    FOREIGN KEY (user_ID) REFERENCES `User`(user_ID),
    FOREIGN KEY (product_ID) REFERENCES Product(product_ID)
);

-- Table: `Order`
CREATE TABLE `Order` (
    order_ID INT PRIMARY KEY,
    status VARCHAR(50),
    date DATE,
    price DECIMAL(10, 2),
    user_ID INT,
    transaction_ID INT,
    FOREIGN KEY (user_ID) REFERENCES `User`(user_ID),
    FOREIGN KEY (transaction_ID) REFERENCES Payment(transaction_ID)
);

-- Table: Contains
CREATE TABLE Contains (
    order_ID INT,
    product_ID INT,
	quantity INT,
    PRIMARY KEY (order_ID, product_ID),
    FOREIGN KEY (order_ID) REFERENCES `Order`(order_ID),
    FOREIGN KEY (product_ID) REFERENCES Product(product_ID)
);

-- Table: Category
CREATE TABLE Category (
    category_ID INT PRIMARY KEY,
    name VARCHAR(255)
);

-- Table: BelongsTo
CREATE TABLE BelongsTo (
    category_ID INT,
    product_ID INT,
    PRIMARY KEY (category_ID, product_ID),
    FOREIGN KEY (category_ID) REFERENCES Category(category_ID),
    FOREIGN KEY (product_ID) REFERENCES Product(product_ID)
);

-- Table: Feedback
CREATE TABLE Feedback (
    feedback_ID INT PRIMARY KEY,
    user_ID INT,
    product_ID INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    FOREIGN KEY (user_ID) REFERENCES `User`(user_ID),
    FOREIGN KEY (product_ID) REFERENCES Product(product_ID)
);


