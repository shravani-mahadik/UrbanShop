-- ===========================
-- PROFILES TABLE
-- ===========================

CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===========================
-- CATEGORIES TABLE
-- ===========================

CREATE TABLE IF NOT EXISTS categories (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- ===========================
-- PRODUCTS TABLE
-- ===========================

CREATE TABLE IF NOT EXISTS products (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10,2),
    category_id BIGINT REFERENCES categories(id),
    location TEXT,
    images JSONB,
    reseller_link TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES profiles(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===========================
-- WISHLIST TABLE
-- ===========================

CREATE TABLE IF NOT EXISTS wishlist (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES profiles(id),
    product_id BIGINT REFERENCES products(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===========================
-- ADDRESSES TABLE
-- ===========================

CREATE TABLE IF NOT EXISTS addresses (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES profiles(id),
    line1 TEXT NOT NULL,
    line2 TEXT,
    city TEXT,
    state TEXT,
    pincode TEXT,
    is_default BOOLEAN DEFAULT FALSE
);

-- ===========================
-- ANALYTICS EVENTS TABLE
-- ===========================

CREATE TABLE IF NOT EXISTS analytics_events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_type TEXT NOT NULL,
    product_id BIGINT REFERENCES products(id),
    user_id UUID REFERENCES profiles(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);