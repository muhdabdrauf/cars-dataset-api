CREATE TABLE brands(
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE models(
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    brand_id INT NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE
);

CREATE TABLE colors(
    color_id SERIAL PRIMARY KEY,
    color_name VARCHAR(30) NOT NULL
);

CREATE TABLE cars(
    car_id INT PRIMARY KEY,
    model_id INT NOT NULL,
    color_id INT NOT NULL,
    purchased_date DATE NOT NULL,
    FOREIGN KEY (model_id) REFERENCES models(model_id) ON DELETE CASCADE,
    FOREIGN KEY (color_id) REFERENCES colors(color_id) ON DELETE CASCADE
);

CREATE INDEX idx_models_brand_id ON models(brand_id);
CREATE INDEX idx_cars_model_id ON cars(model_id);
CREATE INDEX idx_colors_color_id ON colors(color_id);