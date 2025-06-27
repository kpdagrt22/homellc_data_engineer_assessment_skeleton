-- Drop existing tables if any (in dependency order)
DROP TABLE IF EXISTS rehab, hoa, valuation, taxes, leads, property;

-- Main property table
CREATE TABLE property (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_title VARCHAR(255),
    address VARCHAR(255),
    market VARCHAR(100),
    flood VARCHAR(100),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip INT,
    property_type VARCHAR(100),
    highway VARCHAR(100),
    train VARCHAR(100),
    tax_rate DECIMAL(5,2),
    sqft_basement INT,
    htw VARCHAR(50),
    pool VARCHAR(50),
    commercial VARCHAR(50),
    water VARCHAR(100),
    sewage VARCHAR(100),
    year_built INT,
    sqft_mu INT,
    sqft_total INT,
    parking VARCHAR(100),
    bed INT,
    bath INT,
    basement_yes_no VARCHAR(10),
    layout VARCHAR(100),
    rent_restricted VARCHAR(10),
    neighborhood_rating INT,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    subdivision VARCHAR(100),
    school_average DECIMAL(4,2)
);

-- Leads Table
CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    reviewed_status VARCHAR(100),
    most_recent_status VARCHAR(100),
    source VARCHAR(100),
    occupancy VARCHAR(50),
    net_yield DECIMAL(5,2),
    irr DECIMAL(5,2),
    selling_reason VARCHAR(255),
    seller_retained_broker VARCHAR(10),
    final_reviewer VARCHAR(100),
    FOREIGN KEY (property_id) REFERENCES property(id)
);

-- Valuation Table
CREATE TABLE valuation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    previous_rent INT,
    list_price INT,
    zestimate INT,
    arv INT,
    expected_rent INT,
    rent_zestimate INT,
    low_fmr INT,
    high_fmr INT,
    redfin_value INT,
    FOREIGN KEY (property_id) REFERENCES property(id)
);

-- HOA Table
CREATE TABLE hoa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa INT,
    hoa_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES property(id)
);

-- Taxes Table
CREATE TABLE taxes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    taxes INT,
    FOREIGN KEY (property_id) REFERENCES property(id)
);

-- Rehab Table
CREATE TABLE rehab (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    underwriting_rehab INT,
    rehab_calculation INT,
    paint VARCHAR(50),
    flooring_flag VARCHAR(10),
    foundation_flag VARCHAR(10),
    roof_flag VARCHAR(10),
    hvac_flag VARCHAR(10),
    kitchen_flag VARCHAR(10),
    bathroom_flag VARCHAR(10),
    appliances_flag VARCHAR(10),
    windows_flag VARCHAR(10),
    landscaping_flag VARCHAR(10),
    trashout_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES property(id)
);
