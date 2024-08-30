-- Adding index on Product table for frequently searched columns
CREATE INDEX idx_product_name ON Product(name);
CREATE INDEX idx_product_price ON Product(price);

-- Adding index on Category table for category_id, which is used in filtering and joins
CREATE INDEX idx_category_id ON Category(category_id);

-- Adding index on BelongsTo table for product_id and category_id used in joins
CREATE INDEX idx_belongsto_product_id ON BelongsTo(product_id);
CREATE INDEX idx_belongsto_category_id ON BelongsTo(category_id);
