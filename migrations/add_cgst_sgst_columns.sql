-- Migration script to add cgst_rate and sgst_rate columns to the database

-- Add columns to product table if they don't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='product' AND column_name='cgst_rate') THEN
        ALTER TABLE product ADD COLUMN cgst_rate NUMERIC(5,2) NOT NULL DEFAULT 9.0;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='product' AND column_name='sgst_rate') THEN
        ALTER TABLE product ADD COLUMN sgst_rate NUMERIC(5,2) NOT NULL DEFAULT 9.0;
    END IF;
END $$;

-- Update values based on existing gst_rate
UPDATE product 
SET cgst_rate = gst_rate / 2,
    sgst_rate = gst_rate / 2
WHERE cgst_rate = 9.0 AND sgst_rate = 9.0;

-- Add columns to bill_item table if they don't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='bill_item' AND column_name='cgst_rate') THEN
        ALTER TABLE bill_item ADD COLUMN cgst_rate NUMERIC(5,2) NOT NULL DEFAULT 0;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='bill_item' AND column_name='sgst_rate') THEN
        ALTER TABLE bill_item ADD COLUMN sgst_rate NUMERIC(5,2) NOT NULL DEFAULT 0;
    END IF;
END $$;

-- Update values based on existing gst_rate
UPDATE bill_item 
SET cgst_rate = gst_rate / 2,
    sgst_rate = gst_rate / 2
WHERE cgst_rate = 0 AND sgst_rate = 0;
