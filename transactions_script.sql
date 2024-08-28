-- Order Creation Transaction (starting with one product) 
-- also use add product_to_order Transaction for multiple products)
 
START TRANSACTION;
-- Declare variables for the order
SET @user_id = 1;
SET @product_id = 100;
SET @quantity = 2;
SET @transaction_id = 1001;
 
BEGIN TRY
    -- Insert a new order into the Order table
    INSERT INTO `Order` (order_id, status, date, price, user_id, transaction_id)
    VALUES (NULL, 'Pending', CURDATE(), 0, @user_id, @transaction_id);
    SET @new_order_id = LAST_INSERT_ID();
    -- Add the product to the order in the Contains table
    -- This will trigger update_order_price
    INSERT INTO Contains (order_id, product_id, quantity)
    VALUES (@new_order_id, @product_id, @quantity);
    -- No need to manually update the price, the trigger handles it
    COMMIT;
    SELECT 'Order created successfully' AS message;
END TRY
BEGIN CATCH
    ROLLBACK;
    SELECT CONCAT('Error creating order: ', ERROR_MESSAGE()) AS message;
END CATCH;
 
 
-- Add Product to Order Transaction (one by one for multiple products)
 
START TRANSACTION;
-- Declare variables
SET @order_id = 1;
SET @product_id = 100;
SET @quantity = 2;
 
BEGIN TRY
    -- Check if the order exists
    IF NOT EXISTS (SELECT 1 FROM `Order` WHERE order_id = @order_id) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Order does not exist';
    END IF;
 
    -- Check if the product exists
    IF NOT EXISTS (SELECT 1 FROM Product WHERE product_id = @product_id) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Product does not exist';
    END IF;
 
    -- Check if the product is already in the order
    IF EXISTS (SELECT 1 FROM Contains WHERE order_id = @order_id AND product_id = @product_id) THEN
        -- If it exists, delete the old entry and insert a new one
        -- Triggers the update_order_price 
        DELETE FROM Contains 
        WHERE order_id = @order_id AND product_id = @product_id;
    END IF;
 
    -- Insert (or re-insert) the product
    INSERT INTO Contains (order_id, product_id, quantity)
    VALUES (@order_id, @product_id, @quantity);
 
    COMMIT;
    SELECT 'Product added to order successfully' AS message;
END TRY
BEGIN CATCH
    ROLLBACK;
    SELECT CONCAT('Error adding product to order: ', ERROR_MESSAGE()) AS message;
END CATCH;