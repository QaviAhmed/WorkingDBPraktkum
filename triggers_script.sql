-- Triggers track interaction on orders
DELIMITER //

CREATE TRIGGER order_audit_trigger
AFTER UPDATE ON `Order`
FOR EACH ROW
BEGIN
    INSERT INTO OrderHistory (order_id, user_id, action_type, old_status, new_status, old_price, new_price)
    VALUES (NEW.order_id, NEW.user_id, 'UPDATE', OLD.status, NEW.status, OLD.price, NEW.price);
END;//

CREATE TRIGGER order_insert_trigger
AFTER INSERT ON `Order`
FOR EACH ROW
BEGIN
    INSERT INTO OrderHistory (order_id, user_id, action_type, new_status, new_price)
    VALUES (NEW.order_ID, NEW.user_ID, 'CREATE', NEW.status, NEW.price);
END;//

CREATE TRIGGER order_delete_trigger
BEFORE DELETE ON `Order`
FOR EACH ROW
BEGIN
    INSERT INTO OrderHistory (order_id, user_id, action_type, old_status, old_price)
    VALUES (OLD.order_ID, OLD.user_ID, 'DELETE', OLD.status, OLD.price);
END;//

DELIMITER ;


--  Trigger (gets triggered by transactions) for update order_price

DELIMITER //
 
CREATE TRIGGER update_order_price

AFTER INSERT ON Contains

FOR EACH ROW

BEGIN

    DECLARE total_price DECIMAL(10, 2);
 
    -- Calculate the total price of the order

    SELECT SUM(p.price * c.quantity) INTO total_price

    FROM Contains c

    JOIN Product p ON c.product_id = p.product_id

    WHERE c.order_id = NEW.order_id;
 
    -- Update the order price

    UPDATE `Order`

    SET price = total_price

    WHERE order_id = NEW.order_id;

END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER after_user_insert
AFTER INSERT ON Users
FOR EACH ROW
BEGIN
    DECLARE new_shop_id INT;
    
    -- Check if the new user is a seller
    IF NEW.role = 'seller' THEN
        -- Generate a new shop_id
        SELECT IFNULL(MAX(shop_id), 0) + 1 INTO new_shop_id FROM Shop;
        
        -- Insert a new shop
        INSERT INTO Shop (shop_id, name) 
        VALUES (new_shop_id, CONCAT(NEW.name, '''s Shop'));
        
        -- Insert the user into the Seller table
        INSERT INTO Seller (user_id, shop_id)
        VALUES (NEW.user_id, new_shop_id);
    END IF;
END//

DELIMITER ;

 