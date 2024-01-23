-- creates a stored procedure AddBonus that adds a new correction for 
-- a student

DELIMITER $$

CREATE PROCEDURE AddBonus(
	In user_id INT,
	IN project_name VARCHAR(255),
	IN score INT
)
BEGIN
	IF NOT EXISTS (SELECT name fROM projects WHERE name=project_name) THEN
		INSERT INTO projects (name) VALUES (project_name);
	END IF;

	INSERT INTO corrections (user_id, project_id, score)
	VALUES (user_id, (SELECT id FROM projects WHERE name=project_name), score);
END;
$$
DELIMITER ;