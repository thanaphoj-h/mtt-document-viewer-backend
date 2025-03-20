CREATE TABLE IF NOT EXISTS mtt_file (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    filetype VARCHAR(10) NOT NULL,
    filesize VARCHAR(50) NOT NULL,
    created_date DATETIME NOT NULL,
    created_by VARCHAR(50) NOT NULL,
    updated_date DATETIME,
    updated_by VARCHAR(50)
);
