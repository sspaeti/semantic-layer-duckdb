# semantic-layer-duckdb

Trying [boring semantic layer](https://github.com/boringdata/boring-semantic-layer/) with DuckDB.

## Quick Start

Install [uv](https://docs.astral.sh/uv/) then run:
```bash
make install  # Install dependencies  | Or use `uv sync` directly
make run      # Run NYC taxi analysis | Or use `uv run python nyc_taxi.py` directly
```


## Output example


```
❯ make run                                                                                                 8s
uv run python nyc_taxi.py
Available dimensions (taxi_zones): ['location_id', 'borough', 'zone', 'service_zone']
Available measures (taxi_zones): ['zone_count']

Available dimensions (fhvhv_trips): ['hvfhs_license_num', 'dispatching_base_num', 'originating_base_num', 'request_datetime', 'pickup_datetime', 'dropoff_datetime', 'trip_miles', 'trip_time', 'base_passenger_fare', 'tolls', 'bcf', 'sales_tax', 'congestion_surcharge', 'airport_fee', 'tips', 'driver_pay', 'shared_request_flag', 'shared_match_flag', 'access_a_ride_flag', 'wav_request_flag', 'wav_match_flag', 'pickup_zone.location_id', 'pickup_zone.borough', 'pickup_zone.zone', 'pickup_zone.service_zone', 'dropoff_zone.location_id', 'dropoff_zone.borough', 'dropoff_zone.zone', 'dropoff_zone.service_zone']
Available measures (fhvhv_trips): ['trip_count', 'avg_trip_miles', 'avg_trip_time', 'avg_base_fare', 'total_revenue', 'avg_tips', 'avg_driver_pay', 'shared_trip_rate', 'wheelchair_request_rate', 'pickup_zone.zone_count', 'dropoff_zone.zone_count']

=== Trip Volume by Pickup Borough ===
Top 5 boroughs by trip volume:
  pickup_zone_borough  trip_count  avg_trip_miles  avg_base_fare
0           Manhattan     7122571        5.296985      33.575738
1            Brooklyn     5433158        4.215820      23.280429
2              Queens     4453220        6.379047      29.778835
3               Bronx     2541614        4.400500      20.313596
4       Staten Island      316533        5.262288      22.200712

=== Popular Pickup Zones ===
Top 10 pickup zones by trip count:
            pickup_zone_zone pickup_zone_borough  trip_count  avg_trip_miles  total_revenue
0          LaGuardia Airport              Queens      436708       11.948670    27430520.84
1                JFK Airport              Queens      344323       17.605666    25737628.22
2        Crown Heights North            Brooklyn      262172        3.770218     5804554.54
3  Times Sq/Theatre District           Manhattan      234675        6.549750    10573271.77
4             Bushwick South            Brooklyn      228584        4.138090     5419196.40
5             Midtown Center           Manhattan      225063        5.580742     9746426.13
6               East Village           Manhattan      222519        4.800763     6720649.62
7              East New York            Brooklyn      221220        3.829781     4122720.29
8       TriBeCa/Civic Center           Manhattan      212781        5.304404     7865380.79
9  Williamsburg (North Side)            Brooklyn      204630        4.609138     6006392.54

=== Service Zone Analysis ===
Trip metrics by service zone:
  pickup_zone_service_zone  trip_count  avg_base_fare  avg_tips  shared_trip_rate
0                Boro Zone    13066427      22.231723  0.717455          0.022743
1              Yellow Zone     6019638      35.424518  1.924227          0.011609
2                 Airports      781031      68.074313  4.613058          0.000003
3                      N/A         913      26.176429  0.539934          0.014239

=== Revenue Analysis by Trip Distance ===
Revenue by service zone:
  pickup_zone_service_zone  trip_count  total_revenue  avg_driver_pay  avg_trip_miles
0                Boro Zone    13066427   2.904892e+08       18.569082        4.458598
1              Yellow Zone     6019638   2.132428e+08       24.515914        5.374520
2                 Airports      781031   5.316815e+07       50.774571       14.442597
3                      N/A         913   2.389908e+04       22.145104        6.200545

=== Accessibility Metrics ===
Accessibility metrics by pickup borough:
  pickup_zone_borough  trip_count  wheelchair_request_rate  shared_trip_rate
0                 N/A         913                 0.005476          0.014239
1               Bronx     2541614                 0.003761          0.021734
2       Staten Island      316533                 0.003409          0.014520
3            Brooklyn     5433158                 0.003331          0.023856
4           Manhattan     7122571                 0.002980          0.013039
5              Queens     4453220                 0.002683          0.019028
```
