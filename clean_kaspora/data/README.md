# Facebook Ads Data

This directory contains the Facebook advertising performance data used for analysis.

## Dataset: `synthetic_fb_ads_undergarments.csv`

### Description
Synthetic Facebook ads performance data for an undergarments campaign spanning January - March 2025.

### Schema

| Column | Type | Description |
|--------|------|-------------|
| `campaign_name` | string | Name of the advertising campaign |
| `adset_name` | string | Name of the ad set |
| `date` | date | Date of the ad performance (YYYY-MM-DD) |
| `spend` | float | Amount spent on ads ($) |
| `impressions` | int | Number of times ads were shown |
| `clicks` | int | Number of clicks on ads |
| `ctr` | float | Click-through rate (clicks/impressions) |
| `purchases` | int | Number of purchases attributed to ads |
| `revenue` | float | Revenue generated ($) |
| `roas` | float | Return on ad spend (revenue/spend) |
| `creative_type` | string | Type of creative (Image, Video, UGC, Carousel) |
| `creative_message` | string | Ad copy/messaging |
| `audience_type` | string | Targeting type (Broad, Lookalike, Retargeting) |
| `platform` | string | Platform (Facebook, Instagram) |
| `country` | string | Target country (US, UK, IN) |

### Stats
- **Total Rows:** ~700+ entries
- **Date Range:** 2025-01-01 to 2025-03-31 (3 months)
- **Campaigns:** Men ComfortMax Launch, Women Seamless Everyday
- **Products:** Men's and Women's undergarments

### Data Quality Notes
- Some `spend` and `revenue` values may be null
- Campaign names have slight variations (spacing, typos) - intentional for testing data cleaning
- ROAS values range from 0 to 100+ indicating highly variable performance

### Usage
Load this data using the `data_loader.py` utility:
```python
from src.utils.data_loader import load_facebook_ads_data
df = load_facebook_ads_data('data/synthetic_fb_ads_undergarments.csv')
```
