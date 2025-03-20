DROP PROCEDURE IF EXISTS mtt_document_viewer.update_upload_file;

DELIMITER $$
$$
CREATE PROCEDURE mtt_document_viewer.update_upload_file(
    IN p_filename VARCHAR(255),
    IN p_new_filepath VARCHAR(255),
    IN p_new_filetype VARCHAR(10),
    IN p_new_filesize VARCHAR(50),
    IN p_updated_by VARCHAR(50)
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

	IF EXISTS (SELECT 1 FROM mtt_file WHERE filename = p_filename) THEN
		-- If the file exists, update the file record
		UPDATE mtt_file
		SET filepath = p_new_filepath,
		    filetype = p_new_filetype,
		    filesize = p_new_filesize,
		    updated_by = p_updated_by,
		    updated_date = NOW()
		WHERE filename = p_filename;

		-- Return sucess ststus
		SELECT 'Update File Sucessful' AS status;
	ELSE
		-- If file not found return, File Not Founf
		SELECT 'File not found' AS ststus;
	END IF;
END$$
DELIMITER ;
