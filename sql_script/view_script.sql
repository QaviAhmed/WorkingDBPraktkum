CREATE VIEW OrderHistoryView AS 
SELECT 
    oh.history_id,
    oh.order_id,
    u.name AS user_name,
    oh.action_type,
    oh.action_date,
    oh.old_status,
    oh.new_status,
    oh.old_price,
    oh.new_price
FROM 
    OrderHistory oh
JOIN 
    Users u ON oh.user_ID = u.user_id
ORDER BY 
    oh.action_date DESC;


CREATE VIEW UserWishlist AS
SELECT 
    w.user_id,
    u.name AS user_name,
    p.product_id,
    p.name AS product_name,
    p.price
FROM 
    Wishlist w
JOIN Users u ON w.user_id = u.user_id
JOIN Product p ON w.product_id = p.product_id;
 
 

CREATE VIEW ProductFeedbackDetails AS
SELECT 
    p.product_id,
    p.name,
    p.description,
    p.price,
    AVG(f.rating) AS average_rating,
    COUNT(DISTINCT f.feedback_ID) AS review_count
FROM 
    Product p
LEFT JOIN Feedback f ON p.product_id = f.product_id
GROUP BY 
    p.product_id,
    p.name,
    p.description,
    p.price;