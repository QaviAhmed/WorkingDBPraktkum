INSERT INTO Address (street, house_number, postal_code, city, country) VALUES
('Main St', '123', '10001', 'New York', 'USA'),
('Sunset Blvd', '456', '90028', 'Los Angeles', 'USA'),
('Baker St', '221B', 'NW16XE', 'London', 'UK'),
('Champs-Élysées', '12', '75008', 'Paris', 'France'),
('Unter den Linden', '101', '10117', 'Berlin', 'Germany');


INSERT INTO Users (user_id, name, birthdate, email, password, role, address_id) VALUES
(1, 'John Doe', '1990-05-15', 'john@example.com', 'hashed_password1', 'normal_user', 1),
(2, 'Jane Doe', '1992-07-10', 'jane@example.com', 'hashed_password2', 'seller', 2),
(3, 'Sherlock Holmes', '1985-01-06', 'sherlock@example.com', 'hashed_password3', 'normal_user', 3),
(4, 'Jacques Cousteau', '1980-06-11', 'jacques@example.com', 'hashed_password4', 'seller', 4),
(5, 'Hans Müller', '1988-03-22', 'hans@example.com', 'hashed_password5', 'normal_user', 5);

INSERT INTO Shop (shop_id, name) VALUES
(1, 'Janes Boutique'),
(2, 'Parisian Elegance');

INSERT INTO Seller (user_id, shop_id) VALUES
(2, 1),
(4, 2);

INSERT INTO Payment (transaction_id, pp_email) VALUES
(1, 'john.paypal@example.com'),
(2, 'sherlock.paypal@example.com'),
(3, 'hans.paypal@example.com');

INSERT INTO Product (product_id, name, description, price, image, accessory_type, accessory_gender, accessory_usage, shoe_color, shoe_size, shoe_material, shoe_gender) VALUES
(1, 'Running Shoes', 'Comfortable running shoes', 59.99, NULL, NULL, NULL, NULL, 'Red', '10', 'Mesh', 'Unisex'),
(2, 'Leather Belt', 'Genuine leather belt', 24.99, NULL, 'Belt', 'Male', 'Formal', NULL, NULL, NULL, NULL),
(3, 'Sunglasses', 'Stylish sunglasses', 19.99, NULL, 'Sunglasses', 'Unisex', 'Casual', NULL, NULL, NULL, NULL),
(4, 'High Heels', 'Elegant high heels', 89.99, NULL, NULL, NULL, NULL, 'Black', '8', 'Leather', 'Female');

INSERT INTO Wishlist (user_id, product_id) VALUES
(1, 1),
(1, 2),
(3, 3),
(5, 4);

INSERT INTO `Order` (order_id, status, date, price, user_id, transaction_id) VALUES
(1, 'Shipped', '2023-08-01', 59.99, 1, 1),
(2, 'Delivered', '2023-08-05', 24.99, 1, 1),
(3, 'Processing', '2023-08-03', 19.99, 3, 2);

INSERT INTO Category (category_id, name) VALUES
(1, 'Footwear'),
(2, 'Accessories'),
(3, 'Formal Wear');

INSERT INTO BelongsTo (category_id, product_id) VALUES
(1, 1), -- Running Shoes belong to Footwear
(2, 2), -- Leather Belt belongs to Accessories
(2, 3), -- Sunglasses belong to Accessories
(1, 4); -- High Heels belong to Footwear

INSERT INTO Feedback (feedback_ID, user_ID, product_ID, rating, comment) VALUES
(1, 1, 1, 5, 'Great shoes, very comfortable!'),
(2, 3, 3, 4, 'Stylish sunglasses, good value for money.'),
(3, 5, 4, 3, 'High heels look great but are a bit tight.');