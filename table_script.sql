-- Table: Address
-- this is BCNF
CREATE TABLE Address (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    street VARCHAR(255) NOT NULL,
    house_number VARCHAR(20) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- Table: Users
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    name VARCHAR(255),
    birthdate DATE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    address_id INT,
    role ENUM('normal_user', 'seller') NOT NULL DEFAULT 'normal_user',
    FOREIGN KEY (address_id) REFERENCES Address(address_id)
);

-- Table: Shop
CREATE TABLE Shop (
    shop_id INT PRIMARY KEY,
    name VARCHAR(255)
);

-- Table: Seller (subclass of User)
CREATE TABLE Seller (
    user_id INT PRIMARY KEY,
    shop_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (shop_id) REFERENCES Shop(shop_id)
);

-- Table: Payment
CREATE TABLE Payment (
    transaction_id INT PRIMARY KEY,
    pp_email VARCHAR(255)
);

-- Table: HasChat
CREATE TABLE IF NOT EXISTS HasChat (
    user_1 INT,
    user_2 INT,
    PRIMARY KEY (user_1, user_2),
    FOREIGN KEY (user_1) REFERENCES Users(user_id),
    FOREIGN KEY (user_2) REFERENCES Users(user_id)
);

-- Table: Product
-- 3NF
CREATE TABLE Product (
    product_id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    image LONGBLOB,
    accessory_type VARCHAR(100),
    accessory_gender VARCHAR(50),
    accessory_usage VARCHAR(100),
    shoe_color VARCHAR(50),
    shoe_size VARCHAR(20),
    shoe_material VARCHAR(100),
    shoe_gender VARCHAR(50)
);

-- Table: Wishlist
CREATE TABLE Wishlist (
    user_id INT,
    product_id INT,
    PRIMARY KEY (user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Table: `Order`
CREATE TABLE `Order` (
    order_id INT PRIMARY KEY,
    status VARCHAR(50),
    date DATE,
    price DECIMAL(10, 2),
    user_id INT,
    transaction_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (transaction_id) REFERENCES Payment(transaction_id)
);

-- Table: Contains
CREATE TABLE Contains (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Table: Category
CREATE TABLE Category (
    category_id INT PRIMARY KEY,
    name VARCHAR(255)
);

-- Table: BelongsTo
CREATE TABLE BelongsTo (
    category_id INT,
    product_id INT,
    PRIMARY KEY (category_id, product_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Table: Feedback
CREATE TABLE Feedback (
    feedback_ID INT PRIMARY KEY,
    user_ID INT,
    product_ID INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    FOREIGN KEY (user_ID) REFERENCES Users(user_ID),
    FOREIGN KEY (product_ID) REFERENCES Product(product_ID)
);
