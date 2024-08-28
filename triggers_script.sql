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
    VALUES (NEW.order_id, NEW.user_id, 'CREATE', NEW.status, NEW.price);
END;//

CREATE TRIGGER order_delete_trigger
BEFORE DELETE ON `Order`
FOR EACH ROW
BEGIN
    INSERT INTO OrderHistory (order_id, user_id, action_type, old_status, old_price)
    VALUES (OLD.order_id, OLD.user_id, 'DELETE', OLD.status, OLD.price);
END;//

DELIMITER ;

DELIMITER //
 
CREATE TRIGGER update_order_price
AFTER INSERT ON Contains
FOR EACH ROW
BEGIN
    DECLARE product_price DECIMAL(10, 2);
    -- Get the price of the product
    SELECT price INTO product_price
    FROM Product
    WHERE product_id = NEW.product_id;
    -- Update the order price
    UPDATE `Order`
    SET price = price + (product_price * NEW.quantity)
    WHERE order_id = NEW.order_id;
END //
 
DELIMITER ;