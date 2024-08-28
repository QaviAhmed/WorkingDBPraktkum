CREATE VIEW OrderHistoryView AS
SELECT 
    oh.history_ID,
    oh.order_ID,
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
    Users u ON oh.user_ID = u.user_ID
ORDER BY 
    oh.action_date DESC;