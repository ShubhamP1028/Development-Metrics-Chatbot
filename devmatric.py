# -*- coding: utf-8 -*-

import re
import difflib

# Metrics mapping (natural language to values inside 'metric' column)
metrics = {
    "hdi": "hdi",  # Human Development Index
    "hdi rank difference": "rankdiff_hdi_phdi",
    "phdi": "phdi",  # Planetary pressures-adjusted HDI
    "hdi-phdi difference": "diff_hdi_phdi",
    "mean years of schooling male": "mys_m",
    "mean years of schooling female": "mys_f",
    "mean years of schooling": "mys",  # General mean years of schooling
    "expected years of schooling male": "eys_m",
    "expected years of schooling female": "eys_f",
    "expected years of schooling": "eys",  # General expected years of schooling
    "life expectancy male": "le_m",
    "life expectancy female": "le_f",
    "life expectancy": "le",  # General life expectancy
    "gender inequality index": "gii",
    "gii rank": "gii_rank",
    "labour force participation male": "lfpr_m",
    "labour force participation female": "lfpr_f",
    "population ratio male": "pr_m",
    "population ratio female": "pr_f",
    "school enrollment male": "se_m",
    "school enrollment female": "se_f",
    "adolescent birth rate": "abr",  # Adolescent birth rate
    "birth rate": "abr",  # Proxy for general birth rate
    "maternal mortality rate": "mmr",
    "infant mortality rate": "mmr",  # Proxy (imperfect, as mmr is maternal)
    "income inequality": "ineq_inc",
    "education inequality": "ineq_edu",
    "life expectancy inequality": "ineq_le",
    "inequality adjusted hdi": "ihdi",
    "loss due to inequality": "loss",
    "gender development index": "mf",
    "coefficient of inequality": "coef_ineq",
    "gni per capita male": "gni_pc_m",
    "gni per capita female": "gni_pc_f",
    "gross national income per capita": "gnipc",
    "gdp per capita": "gnipc",  # Proxy for GDP per capita
    "gdp": "gnipc",  # Proxy for GDP (per capita as closest match)
    "production": "_prod",
    "hdi male": "hdi_m",
    "hdi female": "hdi_f"
}

# Country aliases mapping (common variations to canonical names in country_list)
country_aliases = {
    "usa": "United States",
    "uk": "United Kingdom",
    "korea": "Korea (Republic of)",
    "russia": "Russian Federation",
    "uae": "United Arab Emirates",
    "iran": "Iran (Islamic Republic of)",
    "congo": "Congo",
    "drc": "Congo (Democratic Republic of the)",
    "north korea": "Korea (Democratic People's Rep. of)",
    "south korea": "Korea (Republic of)",
    "ivory coast": "Côte d'Ivoire",
    "bolivia": "Bolivia (Plurinational State of)",
    "venezuela": "Venezuela (Bolivarian Republic of)",
    "moldova": "Moldova (Republic of)",
    "tanzania": "Tanzania (United Republic of)",
    "syria": "Syrian Arab Republic",
    "laos": "Lao People's Democratic Republic",
    "vietnam": "Viet Nam",
    "hong kong": "Hong Kong, China (SAR)"
}
country_list = [
    "United States",
    "China",
    "India",
    "Brazil",
    "Nigeria",
    "Germany",
    "Japan",
    "Spain",
    "Australia",
    "France",
    "United Kingdom",
    "Indonesia",
    "Pakistan",
    "Bangladesh",
    "Russian Federation",
    "Mexico",
    "Philippines",
    "Egypt",
    "Viet Nam",
    "Ethiopia",
    "Iran (Islamic Republic of)",
    "Turkey",
    "Thailand",
    "Italy",
    "South Africa",
    "Korea (Republic of)",
    "Colombia",
    "Argentina",
    "Ukraine",
    "Algeria",
    "Sudan",
    "Iraq",
    "Afghanistan",
    "Poland",
    "Canada",
    "Morocco",
    "Saudi Arabia",
    "Uzbekistan",
    "Malaysia",
    "Peru",
    "Angola",
    "Ghana",
    "Mozambique",
    "Yemen",
    "Nepal",
    "Madagascar",
    "Cameroon",
    "Côte d'Ivoire",
    "Netherlands",
    "Kenya"
]


def match_country(query):
    query = query.lower()
    # Check if query matches an alias first
    if query in country_aliases:
        return country_aliases[query]
    # Otherwise, proceed with fuzzy matching
    matches = difflib.get_close_matches(query, [c.lower() for c in country_list], n=1, cutoff=0.8)
    if matches:
        return next((c for c in country_list if c.lower() == matches[0]), None)
    return None


def match_metric(query):
    matches = difflib.get_close_matches(query, list(metrics.keys()), n=1, cutoff=0.7)
    return metrics[matches[0]] if matches else None


def extract_info(query):
    query = query.lower()
    # Year (single or range)
    years = list(map(int, re.findall(r'\b(?:19|20)\d{2}\b', query)))
    year = years[0] if len(years) == 1 else None
    year_range = (years[0], years[1]) if len(years) == 2 else None
    # Country
    country = match_country(query)
    # Metric
    metric_value = match_metric(query)

    # Aggregation
    aggregation = None
    if any(word in query for word in ["average", "mean"]):
        aggregation = "AVG"
    elif "maximum" in query or "max" in query:
        aggregation = "MAX"
    elif "minimum" in query or "min" in query:
        aggregation = "MIN"
    elif "total" in query:
        aggregation = "SUM"
    elif "median" in query:
        aggregation = "MEDIAN"
    elif "std deviation" in query or "standard deviation" in query:
        aggregation = "STDDEV"
    # Comparison (e.g., greater than 80%, above 50, below 1000)
    comparison_match = re.search(r'(above|over|greater than|more than|below|under|less than)\s+([\d,]+)', query)
    comparison = None
    if comparison_match:
        op_word = comparison_match.group(1)
        number = comparison_match.group(2).replace(",", "")
        if any(op in op_word for op in ["above", "greater", "over", "more"]):
            comparison = f"> {number}"
        elif any(op in op_word for op in ["below", "less", "under"]):
            comparison = f"< {number}"
    # Range detection (e.g., between 60 and 70)
    range_match = re.search(r'between\s+(\d+)\s+(and|to)\s+(\d+)', query)
    value_range = (int(range_match.group(1)), int(range_match.group(3))) if range_match else None
    # Top/bottom N detection
    top_bottom_match = re.search(r'(top|bottom)\s+(\d+)', query)
    top_bottom = None
    if top_bottom_match and metric_value:
        direction = "DESC" if top_bottom_match.group(1) == "top" else "ASC"
        limit = int(top_bottom_match.group(2))
        top_bottom = (direction, limit)

    return {
        "country": country,
        "metric": metric_value,
        "year": year,
        "year_range": year_range,
        "aggregation": aggregation,
        "comparison": comparison,
        "value_range": value_range,
        "top_bottom": top_bottom
    }


def build_sql(info):
    if not info["metric"]:
        return "Sorry, I couldn't determine the metric you asked about."

    select_clause = f"SELECT {info['aggregation']}(value)" if info["aggregation"] else "SELECT value"
    base = f"{select_clause} FROM development_metrics"
    # Conditions
    conditions = [f"metric = '{info['metric']}'"]
    if info["country"]:
        conditions.append(f"country = '{info['country']}'")
    if info["year"]:
        conditions.append(f"year = {info['year']}")
    if info["year_range"]:
        conditions.append(f"year BETWEEN {info['year_range'][0]} AND {info['year_range'][1]}")
    if info["comparison"]:
        conditions.append(f"value {info['comparison']}")
    if info["value_range"]:
        conditions.append(f"value BETWEEN {info['value_range'][0]} AND {info['value_range'][1]}")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    order_clause = ""
    limit_clause = ""

    if info["top_bottom"]:
        order_clause = f" ORDER BY value {info['top_bottom'][0]}"
        limit_clause = f" LIMIT {info['top_bottom'][1]}"

    return base + where_clause + order_clause + limit_clause + ";"
