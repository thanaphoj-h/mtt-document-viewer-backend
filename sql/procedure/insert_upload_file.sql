DROP PROCEDURE IF EXISTS mtt_document_viewer.insert_upload_file;

DELIMITER $$
$$
CREATE DEFINER=`thorthai`@`%` PROCEDURE `mtt_document_viewer`.`insert_upload_file`(
	IN p_filename VARCHAR(255),
	IN p_filepath VARCHAR(255),
	IN p_filetype VARCHAR(10),
	In p_filesize VARCHAR(50),
	IN p_create_by VARCHAR(50))
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

	-- Check if the file already exists based on filename
	IF EXISTS (SELECT 1 FROM mtt_file WHERE filename = p_filename) THEN
		SELECT 'File Exists' AS status;
	ELSE
	    -- Insert Data of File into Database
	    INSERT INTO mtt_file (filename, filepath, filetype, filesize, created_date, created_by)
	    VALUES (p_filename, p_filepath, p_filetype, p_filesize, NOW(), p_create_by);

		-- Return Sucess Status
		SELECT 'Insertion Successful' AS status;
	END IF;
END$$
DELIMITER ;
