#Database Design For Cars Dataset

A Dataset of **10,000** car purchase records with columns
_id, car_brand, car_model, car_color,_ and _purchased_date_
The goal is to normalize this into a relational schema that supports efficient querying and data consistency

**Primary Keys:**

- Each table uses a numeric auto-increment key (SERIAL) for simplicity.
- The existing id field in the dataset is unique, so it will be reused as car_id.
- Surrogate keys (brand_id, model_id) improve relational integrity.

**Foreign Keys:**

- models.brand_id references brands.brand_id.
- cars.model_id references models.model_id.

**Indexing:**

- Implicit indexes on all PKs.
- Additional index may be added on purchased_date for time-based queries.

**Nullability:**

- All key columns and descriptive attributes are marked NOT NULL.
- No nullable fields required, since the dataset has no missing data.
