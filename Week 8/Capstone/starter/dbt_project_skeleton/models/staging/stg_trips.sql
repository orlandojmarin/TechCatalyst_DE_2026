-- Starting point for your staging model. Adapt it to your question.
--
-- What this does: unions Yellow and Green onto one grain, resolves the column
-- name differences, and adds the derived time columns almost every analysis
-- needs. It deliberately does NOT filter out bad records. Decide that yourself
-- and document it, because the decision belongs to you and to your data
-- quality report.

with yellow as (

    select
        'yellow'                    as taxi_type,
        vendorid                    as vendor_id,
        tpep_pickup_datetime        as pickup_at,
        tpep_dropoff_datetime       as dropoff_at,
        passenger_count,
        trip_distance,
        ratecodeid                  as rate_code_id,
        pulocationid                as pickup_zone_id,
        dolocationid                as dropoff_zone_id,
        payment_type,
        fare_amount,
        tip_amount,
        tolls_amount,
        congestion_surcharge,
        cbd_congestion_fee,
        total_amount
    from {{ source('bronze', 'yellow_raw') }}

),

green as (

    select
        'green'                     as taxi_type,
        vendorid                    as vendor_id,
        lpep_pickup_datetime        as pickup_at,
        lpep_dropoff_datetime       as dropoff_at,
        passenger_count,
        trip_distance,
        ratecodeid                  as rate_code_id,
        pulocationid                as pickup_zone_id,
        dolocationid                as dropoff_zone_id,
        payment_type,
        fare_amount,
        tip_amount,
        tolls_amount,
        congestion_surcharge,
        cbd_congestion_fee,
        total_amount
    from {{ source('bronze', 'green_raw') }}

),

combined as (

    select * from yellow
    union all
    select * from green

)

select
    *,
    datediff('minute', pickup_at, dropoff_at)   as trip_duration_minutes,
    year(pickup_at)                             as pickup_year,
    month(pickup_at)                            as pickup_month,
    dayofweek(pickup_at)                        as pickup_dayofweek,
    hour(pickup_at)                             as pickup_hour
from combined

-- Things to decide before you build on this:
--
-- 1. Green has ehail_fee and trip_type; Yellow has airport_fee. This model
--    drops all three to make the union work. Is that right for your question?
--    If either matters to you, carry it through as a nullable column instead.
--
-- 2. No filtering is applied here. Records with negative fares, zero distance,
--    dropoff before pickup, and pickup dates outside the source month are all
--    still present. Filter deliberately, in a named layer, and record the
--    counts. Do not bury a WHERE clause in a mart and forget it exists.
--
-- 3. pickup_year comes from the data, not the filename. Records with corrupt
--    timestamps will produce years you did not expect. Check before you
--    partition or group by it.
