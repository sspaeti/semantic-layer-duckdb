# NYC Taxi Semantic Layer Guide

This example demonstrates how to use the Boring Semantic Layer with NYC taxi data.

## Key Components

### 1. Data Tables
- **taxi_zone_lookup.csv**: Zone information (LocationID, Borough, Zone, service_zone)
- **fhvhv_tripdata_2023-05.parquet**: Trip data (PULocationID, DOLocationID, fares, times, etc.)

### 2. YAML Configuration (`nyc_taxi.yml`)

#### Model Structure
```yaml
model_name:
  table: table_reference        # Points to table in Python tables dict
  primary_key: column_name      # Required for joins
  time_dimension: column_name   # Optional, for time-based queries
  
  dimensions:
    alias: _.actual_column      # Maps friendly names to table columns
    
  measures:  
    alias: _.column.aggregation()  # Defines calculated metrics
    
  joins:
    alias:
      model: target_model       # Model to join with
      type: one                 # Join type (one, many)
      with: _.local_column      # Joins to target model's primary_key
```

#### Key Patterns
- **Dimensions**: Raw columns accessible for grouping/filtering
- **Measures**: Aggregated calculations (count, sum, mean, etc.)
- **Joins**: Connect models using `with: _.local_column` → `target.primary_key`
- **Boolean Flags**: Convert string flags with `(_.flag_column == 'Y').mean()`

### 3. Python Script (`nyc_taxi.py`)

```python
# 1. Setup connection and tables
con = ibis.duckdb.connect(":memory:")
tables = {
    "taxi_zones_tbl": con.read_csv("taxi_zone_lookup.csv"),
    "trips_tbl": con.read_parquet("fhvhv_tripdata.parquet"),
}

# 2. Load models from YAML
models = SemanticModel.from_yaml("nyc_taxi.yml", tables=tables)
trips_sm = models["fhvhv_trips"]

# 3. Query with semantic layer
expr = trips_sm.query(
    dimensions=["pickup_zone.borough"],      # Use joined dimensions
    measures=["trip_count", "avg_base_fare"], 
    order_by=[("trip_count", "desc")],
    limit=5
)
df = expr.execute()
```

## Working Example Results

The semantic layer enables intuitive queries like:
- Trip volume by borough → `pickup_zone.borough`
- Zone details → `pickup_zone.zone`, `pickup_zone.service_zone`
- Aggregated metrics → `trip_count`, `avg_trip_miles`, `total_revenue`

## Limitations Found

**Dual Joins Issue**: Joining the same table twice (pickup + dropoff zones) creates ambiguous column references in YAML configuration. Current workaround uses only pickup zone joins.

**Alternative**: Use Python API with explicit join conditions for complex multi-table joins.