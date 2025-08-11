"""
NYC Taxi Semantic Layer Example

This example demonstrates a semantic layer for NYC taxi data using:
- taxi_zone_lookup.csv: Zone information including borough, zone name, and service zone
- fhvhv_tripdata_2023-05.parquet: High Volume For-Hire Vehicle trip data

YAML File: `nyc_taxi.yml`
- Defines `taxi_zones` and `fhvhv_trips` models
- Includes joins between trips and pickup/dropoff zones
- Uses Ibis deferred expressions with `_` placeholder

Query Examples:
- Trip volume by borough
- Average trip metrics by zone
- Revenue analysis by service zone
- Shared ride adoption rates

Expected Output Examples:
- Top pickup zones by trip count
- Average trip distance and fare by borough
- Revenue trends by time of day
"""

import ibis
from boring_semantic_layer import SemanticModel

con = ibis.duckdb.connect(":memory:")

#locally:
BASE_PATH = "/home/sspaeti/Documents/datalake/nyc-taxi"
tables = {
    # local:
    # "taxi_zones_tbl": con.read_csv(f"{BASE_PATH_CLOUD_LOOKUP}/taxi_zone_lookup.csv"),
    # "trips_tbl": con.read_parquet(f"{BASE_PATH}/fhvhv_tripdata_2023-05.parquet"),
    #cloud:
    "taxi_zones_tbl": con.read_csv(f"https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"),
    "trips_tbl": con.read_parquet(f"https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2023-05.parquet"),

}


models = SemanticModel.from_yaml(f"nyc_taxi.yml", tables=tables)

taxi_zones_sm = models["taxi_zones"]
trips_sm = models["fhvhv_trips"]

if __name__ == "__main__":
    print("Available dimensions (taxi_zones):", taxi_zones_sm.available_dimensions)
    print("Available measures (taxi_zones):", taxi_zones_sm.available_measures)
    print("\nAvailable dimensions (fhvhv_trips):", trips_sm.available_dimensions)
    print("Available measures (fhvhv_trips):", trips_sm.available_measures)

    print("\n=== Trip Volume by Pickup Borough ===")
    expr = trips_sm.query(
        dimensions=["pickup_zone.borough"],
        measures=["trip_count", "avg_trip_miles", "avg_base_fare"],
        order_by=[("trip_count", "desc")],
        limit=5,
    )
    df = expr.execute()
    print("Top 5 boroughs by trip volume:")
    print(df)

    print("\n=== Popular Pickup Zones ===")
    expr_zones = trips_sm.query(
        dimensions=["pickup_zone.zone", "pickup_zone.borough"],
        measures=["trip_count", "avg_trip_miles", "total_revenue"],
        order_by=[("trip_count", "desc")],
        limit=10,
    )
    df_zones = expr_zones.execute()
    print("Top 10 pickup zones by trip count:")
    print(df_zones)

    print("\n=== Service Zone Analysis ===")
    expr_service = trips_sm.query(
        dimensions=["pickup_zone.service_zone"],
        measures=["trip_count", "avg_base_fare", "avg_tips", "shared_trip_rate"],
        order_by=[("trip_count", "desc")],
    )
    df_service = expr_service.execute()
    print("Trip metrics by service zone:")
    print(df_service)

    print("\n=== Revenue Analysis by Trip Distance ===")
    expr_revenue = trips_sm.query(
        dimensions=["pickup_zone.service_zone"],
        measures=["trip_count", "total_revenue", "avg_driver_pay", "avg_trip_miles"],
        order_by=[("total_revenue", "desc")],
        limit=5,
    )
    df_revenue = expr_revenue.execute()
    print("Revenue by service zone:")
    print(df_revenue)

    print("\n=== Accessibility Metrics ===")
    expr_access = trips_sm.query(
        dimensions=["pickup_zone.borough"],
        measures=["trip_count", "wheelchair_request_rate", "shared_trip_rate"],
        order_by=[("wheelchair_request_rate", "desc")],
    )
    df_access = expr_access.execute()
    print("Accessibility metrics by pickup borough:")
    print(df_access)
