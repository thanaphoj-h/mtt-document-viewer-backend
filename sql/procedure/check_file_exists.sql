DROP PROCEDURE IF EXISTS mtt_document_viewer.check_file_exists;

DELIMITER $$
$$
CREATE PROCEDURE mtt_document_viewer.check_file_exists(
    IN p_filename VARCHAR(255)
)
BEGIN
-- Declare variables for SQLSTATE and SQL error message
    DECLARE v_sqlstate VARCHAR(5);
    DECLARE v_sqlerrmsg VARCHAR(255);

    -- Declare a handler for SQL exceptions
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Capture the SQLSTATE and SQL error message
        GET DIAGNOSTICS CONDITION 1
            v_sqlstate = RETURNED_SQLSTATE,
            v_sqlerrmsg = MESSAGE_TEXT;

        -- Return error status and the detailed error message
        SELECT 'Error' AS status,
               CONCAT('An error occurred: ', v_sqlerrmsg) AS error_message,
               v_sqlstate AS sql_state;
    END;

    -- Check if the file exists based on filename
    IF EXISTS (SELECT 1 FROM mtt_file WHERE filename = p_filename) THEN
        -- If the file exists, return 'File Exists'
        SELECT 'File Exists' AS status;
    ELSE
        -- If the file doesn't exist, return 'File Not Exists'
        SELECT 'File Not Exists' AS status;
    END IF;
END$$
DELIMITER ;
