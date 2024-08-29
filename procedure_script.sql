DELIMITER $$

CREATE PROCEDURE GetProductsByCategory(
    IN p_category_id INT
)
BEGIN
    SELECT 
        p.product_id,
        p.name AS product_name,
        p.description,
        p.price,
        p.image,
        p.accessory_type,
        p.accessory_gender,
        p.accessory_usage,
        p.shoe_color,
        p.shoe_size,
        p.shoe_material,
        p.shoe_gender,
        c.category_id,
        c.name AS category_name
    FROM 
        Product p
    JOIN 
        BelongsTo b ON p.product_id = b.product_id
    JOIN 
        Category c ON b.category_id = c.category_id
    WHERE 
        (p_category_id IS NULL OR c.category_id = p_category_id)
    GROUP BY 
        c.category_id, p.product_id
    HAVING 
        p.price > 0
    ORDER BY 
        p.price ASC;
END $$a

CREATE PROCEDURE SearchProductsByName(
    IN p_search_query VARCHAR(255)
)
BEGIN
    SELECT 
        p.product_id,
        p.name AS product_name,
        p.description,
        p.price,
        p.image,
        p.accessory_type,
        p.accessory_gender,
        p.accessory_usage,
        p.shoe_color,
        p.shoe_size,
        p.shoe_material,
        p.shoe_gender,
        c.category_id,
        c.name AS category_name
    FROM 
        Product p
    JOIN 
        BelongsTo b ON p.product_id = b.product_id
    JOIN 
        Category c ON b.category_id = c.category_id
    WHERE 
        (p_search_query IS NULL OR p.name LIKE CONCAT('%', p_search_query, '%'))
    GROUP BY 
        c.category_id, p.product_id
    HAVING 
        p.price > 0
    ORDER BY 
        p.price ASC;
END $$

DELIMITER ;
