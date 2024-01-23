-- creates a trigger that decreses the quantity of an item
-- after adding a new order
-- the quantity of the table items can be negative

CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders FOR EACH ROW
UPDATE items
SET items.quantity = items.quantity - NEW.number
WHERE items.name = NEW.item_name;
