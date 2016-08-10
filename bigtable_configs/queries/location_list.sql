SELECT
  parent_location_id,
  child_location_name,

  -- metadata
  type,
  client_region,
  client_region_code,
  client_country,
  client_country_code,
  client_continent,
  client_continent_code,

  -- data: last_week
  last_week_test_count,
  last_week_download_speed_mbps_median,
  last_week_upload_speed_mbps_median,
  last_week_download_speed_mbps_avg,
  last_week_upload_speed_mbps_avg,
  last_week_download_speed_mbps_min,
  last_week_download_speed_mbps_max,
  last_week_upload_speed_mbps_min,
  last_week_upload_speed_mbps_max,
  last_week_download_speed_mbps_stddev,
  last_week_upload_speed_mbps_stddev,

  -- data: last month
  last_month_test_count,
  last_month_download_speed_mbps_median,
  last_month_upload_speed_mbps_median,
  last_month_download_speed_mbps_avg,
  last_month_upload_speed_mbps_avg,
  last_month_download_speed_mbps_min,
  last_month_download_speed_mbps_max,
  last_month_upload_speed_mbps_min,
  last_month_upload_speed_mbps_max,
  last_month_download_speed_mbps_stddev,
  last_month_upload_speed_mbps_stddev,

  -- data: last year
  last_year_test_count,
  last_year_download_speed_mbps_median,
  last_year_upload_speed_mbps_median,
  last_year_download_speed_mbps_avg,
  last_year_upload_speed_mbps_avg,
  last_year_download_speed_mbps_min,
  last_year_download_speed_mbps_max,
  last_year_upload_speed_mbps_min,
  last_year_upload_speed_mbps_max,
  last_year_download_speed_mbps_stddev,
  last_year_upload_speed_mbps_stddev

from

-- ============
-- Cities
-- ============
(select
  REPLACE(LOWER(CONCAT(
    IFNULL(client_continent_code, ""),
    IFNULL(client_country_code, ""), "",
    IFNULL(client_region_code, ""), ""
  )), " ", "") as parent_location_id,

  all.client_city as child_location_name,

  "city" as type,

  all.client_city as client_city,
  all.client_region as client_region,
  all.client_country as client_country,
  all.client_continent as client_continent,

  all.client_region_code as client_region_code,
  all.client_country_code as client_country_code,
  all.client_continent_code as client_continent_code,

  -- last week measurements
  lastweek.last_week_test_count as last_week_test_count,
  lastweek.download_speed_mbps_median as last_week_download_speed_mbps_median,
  lastweek.upload_speed_mbps_median as last_week_upload_speed_mbps_median,
  lastweek.download_speed_mbps_avg as last_week_download_speed_mbps_avg,
  lastweek.upload_speed_mbps_avg as last_week_upload_speed_mbps_avg,
  lastweek.download_speed_mbps_min as last_week_download_speed_mbps_min,
  lastweek.download_speed_mbps_max as last_week_download_speed_mbps_max,
  lastweek.upload_speed_mbps_min as last_week_upload_speed_mbps_min,
  lastweek.upload_speed_mbps_max as last_week_upload_speed_mbps_max,
  lastweek.download_speed_mbps_stddev as last_week_download_speed_mbps_stddev,
  lastweek.upload_speed_mbps_stddev as last_week_upload_speed_mbps_stddev,

  -- last month measurements
  lastmonth.last_month_test_count as last_month_test_count,
  lastmonth.download_speed_mbps_median as last_month_download_speed_mbps_median,
  lastmonth.upload_speed_mbps_median as last_month_upload_speed_mbps_median,
  lastmonth.download_speed_mbps_avg as last_month_download_speed_mbps_avg,
  lastmonth.upload_speed_mbps_avg as last_month_upload_speed_mbps_avg,
  lastmonth.download_speed_mbps_min as last_month_download_speed_mbps_min,
  lastmonth.download_speed_mbps_max as last_month_download_speed_mbps_max,
  lastmonth.upload_speed_mbps_min as last_month_upload_speed_mbps_min,
  lastmonth.upload_speed_mbps_max as last_month_upload_speed_mbps_max,
  lastmonth.download_speed_mbps_stddev as last_month_download_speed_mbps_stddev,
  lastmonth.upload_speed_mbps_stddev as last_month_upload_speed_mbps_stddev,

  -- last year measurements
  lastyear.last_year_test_count as last_year_test_count,
  lastyear.download_speed_mbps_median as last_year_download_speed_mbps_median,
  lastyear.upload_speed_mbps_median as last_year_upload_speed_mbps_median,
  lastyear.download_speed_mbps_avg as last_year_download_speed_mbps_avg,
  lastyear.upload_speed_mbps_avg as last_year_upload_speed_mbps_avg,
  lastyear.download_speed_mbps_min as last_year_download_speed_mbps_min,
  lastyear.download_speed_mbps_max as last_year_download_speed_mbps_max,
  lastyear.upload_speed_mbps_min as last_year_upload_speed_mbps_min,
  lastyear.upload_speed_mbps_max as last_year_upload_speed_mbps_max,
  lastyear.download_speed_mbps_stddev as last_year_download_speed_mbps_stddev,
  lastyear.upload_speed_mbps_stddev as last_year_upload_speed_mbps_stddev

  FROM {0} all

  -- Compute metrics for the last week
  left join
  (
    SELECT
      count(*) as last_week_test_count,
      client_city,
      client_region,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev,

    from {0}
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -7, "DAY") and
      client_city is not null
    group by
      client_city,
      client_region,
      client_country,
      client_continent
  ) lastweek on
    all.client_city = lastweek.client_city and
    all.client_region = lastweek.client_region and
    all.client_country = lastweek.client_country and
    all.client_continent = lastweek.client_continent

  -- Compute metrics for the current month
  left join
  (
    SELECT
      count(*) as last_month_test_count,
      client_city,
      client_region,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev

    from {0}
    -- current month:
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, "MONTH") and
      client_city is not null

    group by
      client_city,
      client_region,
      client_country,
      client_continent
  ) lastmonth on
    all.client_city = lastmonth.client_city and
    all.client_region = lastmonth.client_region and
    all.client_country = lastmonth.client_country and
    all.client_continent = lastmonth.client_continent

  -- Compute metrics for the current year
  left join
  (
    SELECT
      count(*) as last_year_test_count,
      client_city,
      client_region,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev

    from {0}
    -- current year:
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, "YEAR") and
      client_city is not null
    group by
      client_city,
      client_region,
      client_country,
      client_continent

  ) lastyear on
    all.client_city = lastyear.client_city and
    all.client_region = lastyear.client_region and
    all.client_country = lastyear.client_country and
    all.client_continent = lastyear.client_continent

  GROUP BY
    -- meta fields:
    parent_location_id,
    child_location_name,
    client_city,
    client_region,
    client_region_code,
    client_country,
    client_country_code,
    client_continent,
    client_continent_code,

    -- last week:
    last_week_test_count,
    last_week_download_speed_mbps_median,
    last_week_upload_speed_mbps_median,
    last_week_download_speed_mbps_avg,
    last_week_upload_speed_mbps_avg,
    last_week_download_speed_mbps_min,
    last_week_download_speed_mbps_max,
    last_week_upload_speed_mbps_min,
    last_week_upload_speed_mbps_max,
    last_week_download_speed_mbps_stddev,
    last_week_upload_speed_mbps_stddev,

    -- last month:
    last_month_test_count,
    last_month_download_speed_mbps_median,
    last_month_upload_speed_mbps_median,
    last_month_download_speed_mbps_avg,
    last_month_upload_speed_mbps_avg,
    last_month_download_speed_mbps_min,
    last_month_download_speed_mbps_max,
    last_month_upload_speed_mbps_min,
    last_month_upload_speed_mbps_max,
    last_month_download_speed_mbps_stddev,
    last_month_upload_speed_mbps_stddev,

    -- last year:
    last_year_test_count,
    last_year_download_speed_mbps_median,
    last_year_upload_speed_mbps_median,
    last_year_download_speed_mbps_avg,
    last_year_upload_speed_mbps_avg,
    last_year_download_speed_mbps_min,
    last_year_download_speed_mbps_max,
    last_year_upload_speed_mbps_min,
    last_year_upload_speed_mbps_max,
    last_year_download_speed_mbps_stddev,
    last_year_upload_speed_mbps_stddev
),

-- ============
-- Regions
-- ============
(select
  REPLACE(LOWER(CONCAT(
    IFNULL(client_continent_code, ""),
    IFNULL(client_country_code, ""), ""
  )), " ", "") as parent_location_id,

  all.client_region as child_location_name,

  "region" as type,

  all.client_region as client_region,
  all.client_country as client_country,
  all.client_continent as client_continent,

  all.client_region_code as client_region_code,
  all.client_country_code as client_country_code,
  all.client_continent_code as client_continent_code,

  -- last week measurements
  lastweek.last_week_test_count as last_week_test_count,
  lastweek.download_speed_mbps_median as last_week_download_speed_mbps_median,
  lastweek.upload_speed_mbps_median as last_week_upload_speed_mbps_median,
  lastweek.download_speed_mbps_avg as last_week_download_speed_mbps_avg,
  lastweek.upload_speed_mbps_avg as last_week_upload_speed_mbps_avg,
  lastweek.download_speed_mbps_min as last_week_download_speed_mbps_min,
  lastweek.download_speed_mbps_max as last_week_download_speed_mbps_max,
  lastweek.upload_speed_mbps_min as last_week_upload_speed_mbps_min,
  lastweek.upload_speed_mbps_max as last_week_upload_speed_mbps_max,
  lastweek.download_speed_mbps_stddev as last_week_download_speed_mbps_stddev,
  lastweek.upload_speed_mbps_stddev as last_week_upload_speed_mbps_stddev,

  -- last month measurements
  lastmonth.last_month_test_count as last_month_test_count,
  lastmonth.download_speed_mbps_median as last_month_download_speed_mbps_median,
  lastmonth.upload_speed_mbps_median as last_month_upload_speed_mbps_median,
  lastmonth.download_speed_mbps_avg as last_month_download_speed_mbps_avg,
  lastmonth.upload_speed_mbps_avg as last_month_upload_speed_mbps_avg,
  lastmonth.download_speed_mbps_min as last_month_download_speed_mbps_min,
  lastmonth.download_speed_mbps_max as last_month_download_speed_mbps_max,
  lastmonth.upload_speed_mbps_min as last_month_upload_speed_mbps_min,
  lastmonth.upload_speed_mbps_max as last_month_upload_speed_mbps_max,
  lastmonth.download_speed_mbps_stddev as last_month_download_speed_mbps_stddev,
  lastmonth.upload_speed_mbps_stddev as last_month_upload_speed_mbps_stddev,

  -- last year measurements
  lastyear.last_year_test_count as last_year_test_count,
  lastyear.download_speed_mbps_median as last_year_download_speed_mbps_median,
  lastyear.upload_speed_mbps_median as last_year_upload_speed_mbps_median,
  lastyear.download_speed_mbps_avg as last_year_download_speed_mbps_avg,
  lastyear.upload_speed_mbps_avg as last_year_upload_speed_mbps_avg,
  lastyear.download_speed_mbps_min as last_year_download_speed_mbps_min,
  lastyear.download_speed_mbps_max as last_year_download_speed_mbps_max,
  lastyear.upload_speed_mbps_min as last_year_upload_speed_mbps_min,
  lastyear.upload_speed_mbps_max as last_year_upload_speed_mbps_max,
  lastyear.download_speed_mbps_stddev as last_year_download_speed_mbps_stddev,
  lastyear.upload_speed_mbps_stddev as last_year_upload_speed_mbps_stddev

  FROM {0} all

  -- Compute metrics for the last week
  left join
  (
    SELECT
      count(*) as last_week_test_count,
      client_region,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev,

    from {0}
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -7, "DAY") and
      client_region is not null
    group by
      client_region,
      client_country,
      client_continent
  ) lastweek on
    all.client_region = lastweek.client_region and
    all.client_country = lastweek.client_country and
    all.client_continent = lastweek.client_continent

  -- Compute metrics for the current month
  left join
  (
    SELECT
      count(*) as last_month_test_count,
      client_region,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev

    from {0}
    -- current month:
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, "MONTH") and
      client_region is not null
    group by
      client_region,
      client_country,
      client_continent
  ) lastmonth on
    all.client_region = lastmonth.client_region and
    all.client_country = lastmonth.client_country and
    all.client_continent = lastmonth.client_continent

  -- Compute metrics for the current year
  left join
  (
    SELECT
      count(*) as last_year_test_count,
      client_region,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev

    from {0}
    -- current year:
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, "YEAR") and
      client_region is not null
    group by
      client_region,
      client_country,
      client_continent

  ) lastyear on
    all.client_region = lastyear.client_region and
    all.client_country = lastyear.client_country and
    all.client_continent = lastyear.client_continent

  GROUP BY
    -- meta fields:
    parent_location_id,
    child_location_name,
    client_region,
    client_region_code,
    client_country,
    client_country_code,
    client_continent,
    client_continent_code,

    -- last week:
    last_week_test_count,
    last_week_download_speed_mbps_median,
    last_week_upload_speed_mbps_median,
    last_week_download_speed_mbps_avg,
    last_week_upload_speed_mbps_avg,
    last_week_download_speed_mbps_min,
    last_week_download_speed_mbps_max,
    last_week_upload_speed_mbps_min,
    last_week_upload_speed_mbps_max,
    last_week_download_speed_mbps_stddev,
    last_week_upload_speed_mbps_stddev,

    -- last month:
    last_month_test_count,
    last_month_download_speed_mbps_median,
    last_month_upload_speed_mbps_median,
    last_month_download_speed_mbps_avg,
    last_month_upload_speed_mbps_avg,
    last_month_download_speed_mbps_min,
    last_month_download_speed_mbps_max,
    last_month_upload_speed_mbps_min,
    last_month_upload_speed_mbps_max,
    last_month_download_speed_mbps_stddev,
    last_month_upload_speed_mbps_stddev,

    -- last year:
    last_year_test_count,
    last_year_download_speed_mbps_median,
    last_year_upload_speed_mbps_median,
    last_year_download_speed_mbps_avg,
    last_year_upload_speed_mbps_avg,
    last_year_download_speed_mbps_min,
    last_year_download_speed_mbps_max,
    last_year_upload_speed_mbps_min,
    last_year_upload_speed_mbps_max,
    last_year_download_speed_mbps_stddev,
    last_year_upload_speed_mbps_stddev
),

-- ============
-- Countries
-- ============
(select

  IFNULL(client_continent_code, "") as parent_location_id,

  all.client_country as child_location_name,

  "country" as type,

  all.client_country as client_country,
  all.client_continent as client_continent,

  all.client_country_code as client_country_code,
  all.client_continent_code as client_continent_code,

  -- last week measurements
  lastweek.last_week_test_count as last_week_test_count,
  lastweek.download_speed_mbps_median as last_week_download_speed_mbps_median,
  lastweek.upload_speed_mbps_median as last_week_upload_speed_mbps_median,
  lastweek.download_speed_mbps_avg as last_week_download_speed_mbps_avg,
  lastweek.upload_speed_mbps_avg as last_week_upload_speed_mbps_avg,
  lastweek.download_speed_mbps_min as last_week_download_speed_mbps_min,
  lastweek.download_speed_mbps_max as last_week_download_speed_mbps_max,
  lastweek.upload_speed_mbps_min as last_week_upload_speed_mbps_min,
  lastweek.upload_speed_mbps_max as last_week_upload_speed_mbps_max,
  lastweek.download_speed_mbps_stddev as last_week_download_speed_mbps_stddev,
  lastweek.upload_speed_mbps_stddev as last_week_upload_speed_mbps_stddev,

  -- last month measurements
  lastmonth.last_month_test_count as last_month_test_count,
  lastmonth.download_speed_mbps_median as last_month_download_speed_mbps_median,
  lastmonth.upload_speed_mbps_median as last_month_upload_speed_mbps_median,
  lastmonth.download_speed_mbps_avg as last_month_download_speed_mbps_avg,
  lastmonth.upload_speed_mbps_avg as last_month_upload_speed_mbps_avg,
  lastmonth.download_speed_mbps_min as last_month_download_speed_mbps_min,
  lastmonth.download_speed_mbps_max as last_month_download_speed_mbps_max,
  lastmonth.upload_speed_mbps_min as last_month_upload_speed_mbps_min,
  lastmonth.upload_speed_mbps_max as last_month_upload_speed_mbps_max,
  lastmonth.download_speed_mbps_stddev as last_month_download_speed_mbps_stddev,
  lastmonth.upload_speed_mbps_stddev as last_month_upload_speed_mbps_stddev,

  -- last year measurements
  lastyear.last_year_test_count as last_year_test_count,
  lastyear.download_speed_mbps_median as last_year_download_speed_mbps_median,
  lastyear.upload_speed_mbps_median as last_year_upload_speed_mbps_median,
  lastyear.download_speed_mbps_avg as last_year_download_speed_mbps_avg,
  lastyear.upload_speed_mbps_avg as last_year_upload_speed_mbps_avg,
  lastyear.download_speed_mbps_min as last_year_download_speed_mbps_min,
  lastyear.download_speed_mbps_max as last_year_download_speed_mbps_max,
  lastyear.upload_speed_mbps_min as last_year_upload_speed_mbps_min,
  lastyear.upload_speed_mbps_max as last_year_upload_speed_mbps_max,
  lastyear.download_speed_mbps_stddev as last_year_download_speed_mbps_stddev,
  lastyear.upload_speed_mbps_stddev as last_year_upload_speed_mbps_stddev

  FROM {0} all

  -- Compute metrics for the last week
  left join
  (
    SELECT
      count(*) as last_week_test_count,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev,

    from {0}
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -7, "DAY") and
      client_country is not null
    group by
      client_country,
      client_continent
  ) lastweek on
    all.client_country = lastweek.client_country and
    all.client_continent = lastweek.client_continent

  -- Compute metrics for the current month
  left join
  (
    SELECT
      count(*) as last_month_test_count,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev

    from {0}
    -- current month:
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, "MONTH") and
      client_country is not null
    group by
      client_country,
      client_continent
  ) lastmonth on
    all.client_country = lastmonth.client_country and
    all.client_continent = lastmonth.client_continent

  -- Compute metrics for the current year
  left join
  (
    SELECT
      count(*) as last_year_test_count,
      client_country,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev

    from {0}
    -- current year:
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, "YEAR") and
      client_country is not null
    group by
      client_country,
      client_continent

  ) lastyear on
    all.client_country = lastyear.client_country and
    all.client_continent = lastyear.client_continent

  GROUP BY
    -- meta fields:
    parent_location_id,
    child_location_name,
    client_country,
    client_country_code,
    client_continent,
    client_continent_code,

    -- last week:
    last_week_test_count,
    last_week_download_speed_mbps_median,
    last_week_upload_speed_mbps_median,
    last_week_download_speed_mbps_avg,
    last_week_upload_speed_mbps_avg,
    last_week_download_speed_mbps_min,
    last_week_download_speed_mbps_max,
    last_week_upload_speed_mbps_min,
    last_week_upload_speed_mbps_max,
    last_week_download_speed_mbps_stddev,
    last_week_upload_speed_mbps_stddev,

    -- last month:
    last_month_test_count,
    last_month_download_speed_mbps_median,
    last_month_upload_speed_mbps_median,
    last_month_download_speed_mbps_avg,
    last_month_upload_speed_mbps_avg,
    last_month_download_speed_mbps_min,
    last_month_download_speed_mbps_max,
    last_month_upload_speed_mbps_min,
    last_month_upload_speed_mbps_max,
    last_month_download_speed_mbps_stddev,
    last_month_upload_speed_mbps_stddev,

    -- last year:
    last_year_test_count,
    last_year_download_speed_mbps_median,
    last_year_upload_speed_mbps_median,
    last_year_download_speed_mbps_avg,
    last_year_upload_speed_mbps_avg,
    last_year_download_speed_mbps_min,
    last_year_download_speed_mbps_max,
    last_year_upload_speed_mbps_min,
    last_year_upload_speed_mbps_max,
    last_year_download_speed_mbps_stddev,
    last_year_upload_speed_mbps_stddev
),

-- ============
-- Continent
-- ============
(select
  "" as parent_location_id,

  all.client_continent as child_location_name,

  "continent" as type,

  all.client_continent as client_continent,
  all.client_continent_code as client_continent_code,

  -- last week measurements
  lastweek.last_week_test_count as last_week_test_count,
  lastweek.download_speed_mbps_median as last_week_download_speed_mbps_median,
  lastweek.upload_speed_mbps_median as last_week_upload_speed_mbps_median,
  lastweek.download_speed_mbps_avg as last_week_download_speed_mbps_avg,
  lastweek.upload_speed_mbps_avg as last_week_upload_speed_mbps_avg,
  lastweek.download_speed_mbps_min as last_week_download_speed_mbps_min,
  lastweek.download_speed_mbps_max as last_week_download_speed_mbps_max,
  lastweek.upload_speed_mbps_min as last_week_upload_speed_mbps_min,
  lastweek.upload_speed_mbps_max as last_week_upload_speed_mbps_max,
  lastweek.download_speed_mbps_stddev as last_week_download_speed_mbps_stddev,
  lastweek.upload_speed_mbps_stddev as last_week_upload_speed_mbps_stddev,

  -- last month measurements
  lastmonth.last_month_test_count as last_month_test_count,
  lastmonth.download_speed_mbps_median as last_month_download_speed_mbps_median,
  lastmonth.upload_speed_mbps_median as last_month_upload_speed_mbps_median,
  lastmonth.download_speed_mbps_avg as last_month_download_speed_mbps_avg,
  lastmonth.upload_speed_mbps_avg as last_month_upload_speed_mbps_avg,
  lastmonth.download_speed_mbps_min as last_month_download_speed_mbps_min,
  lastmonth.download_speed_mbps_max as last_month_download_speed_mbps_max,
  lastmonth.upload_speed_mbps_min as last_month_upload_speed_mbps_min,
  lastmonth.upload_speed_mbps_max as last_month_upload_speed_mbps_max,
  lastmonth.download_speed_mbps_stddev as last_month_download_speed_mbps_stddev,
  lastmonth.upload_speed_mbps_stddev as last_month_upload_speed_mbps_stddev,

  -- last year measurements
  lastyear.last_year_test_count as last_year_test_count,
  lastyear.download_speed_mbps_median as last_year_download_speed_mbps_median,
  lastyear.upload_speed_mbps_median as last_year_upload_speed_mbps_median,
  lastyear.download_speed_mbps_avg as last_year_download_speed_mbps_avg,
  lastyear.upload_speed_mbps_avg as last_year_upload_speed_mbps_avg,
  lastyear.download_speed_mbps_min as last_year_download_speed_mbps_min,
  lastyear.download_speed_mbps_max as last_year_download_speed_mbps_max,
  lastyear.upload_speed_mbps_min as last_year_upload_speed_mbps_min,
  lastyear.upload_speed_mbps_max as last_year_upload_speed_mbps_max,
  lastyear.download_speed_mbps_stddev as last_year_download_speed_mbps_stddev,
  lastyear.upload_speed_mbps_stddev as last_year_upload_speed_mbps_stddev

  FROM {0} all

  -- Compute metrics for the last week
  left join
  (
    SELECT
      count(*) as last_week_test_count,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev,

    from {0}
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -7, "DAY") and
      client_continent is not null
    group by
      client_continent
  ) lastweek on
    all.client_continent = lastweek.client_continent

  -- Compute metrics for the current month
  left join
  (
    SELECT
      count(*) as last_month_test_count,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev

    from {0}
    -- current month:
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, "MONTH") and
      client_continent is not null
    group by
      client_continent
  ) lastmonth on
    all.client_continent = lastmonth.client_continent

  -- Compute metrics for the current year
  left join
  (
    SELECT
      count(*) as last_year_test_count,
      client_continent,

      -- measurements:
      nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
      nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

      AVG(download_speed_mbps) AS download_speed_mbps_avg,
      AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

      MIN(download_speed_mbps) AS download_speed_mbps_min,
      MAX(download_speed_mbps) AS download_speed_mbps_max,

      MIN(upload_speed_mbps) AS upload_speed_mbps_min,
      MAX(upload_speed_mbps) AS upload_speed_mbps_max,

      STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
      STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev

    from {0}
    -- current year:
    where
      test_date >= DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, "YEAR") and
      client_continent is not null
    group by
      client_continent

  ) lastyear on
    all.client_continent = lastyear.client_continent

  GROUP BY
    -- meta fields:
    parent_location_id,
    child_location_name,
    client_continent,
    client_continent_code,

    -- last week:
    last_week_test_count,
    last_week_download_speed_mbps_median,
    last_week_upload_speed_mbps_median,
    last_week_download_speed_mbps_avg,
    last_week_upload_speed_mbps_avg,
    last_week_download_speed_mbps_min,
    last_week_download_speed_mbps_max,
    last_week_upload_speed_mbps_min,
    last_week_upload_speed_mbps_max,
    last_week_download_speed_mbps_stddev,
    last_week_upload_speed_mbps_stddev,

    -- last month:
    last_month_test_count,
    last_month_download_speed_mbps_median,
    last_month_upload_speed_mbps_median,
    last_month_download_speed_mbps_avg,
    last_month_upload_speed_mbps_avg,
    last_month_download_speed_mbps_min,
    last_month_download_speed_mbps_max,
    last_month_upload_speed_mbps_min,
    last_month_upload_speed_mbps_max,
    last_month_download_speed_mbps_stddev,
    last_month_upload_speed_mbps_stddev,

    -- last year:
    last_year_test_count,
    last_year_download_speed_mbps_median,
    last_year_upload_speed_mbps_median,
    last_year_download_speed_mbps_avg,
    last_year_upload_speed_mbps_avg,
    last_year_download_speed_mbps_min,
    last_year_download_speed_mbps_max,
    last_year_upload_speed_mbps_min,
    last_year_upload_speed_mbps_max,
    last_year_download_speed_mbps_stddev,
    last_year_upload_speed_mbps_stddev
);
