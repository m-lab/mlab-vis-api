SELECT
  nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
  nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

  -- AVG(download_speed_mbps) AS download_speed_mbps_avg,
  -- AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

  -- MIN(download_speed_mbps) AS download_speed_mbps_min,
  -- MAX(download_speed_mbps) AS download_speed_mbps_max,

  -- MIN(upload_speed_mbps) AS upload_speed_mbps_min,
  -- MAX(upload_speed_mbps) AS upload_speed_mbps_max,

  -- STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
  -- STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev,

  COUNT(*) AS count,

client_continent_code,
client_country_code,
client_region_code,
client_asn_number,
server_asn_name,
client_continent,
client_country,
client_region,
client_asn_name,
DATE(test_date) AS date

FROM
  {0}


GROUP BY
client_continent_code,
client_country_code,
client_region_code,
client_asn_number,
server_asn_name,
date,
client_continent,
client_country,
client_region,
client_asn_name

