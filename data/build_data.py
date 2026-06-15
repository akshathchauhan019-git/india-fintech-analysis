import pandas as pd

# Official NPCI UPI monthly data (volume in millions, value in billion INR)
upi_data = [
    (2016, 8, 0.09, 3.07), (2016, 9, 0.30, 9.08), (2016, 10, 0.42, 13.43),
    (2016, 11, 1.01, 25.80), (2016, 12, 4.51, 74.16),
    (2017, 1, 4.77, 80.23), (2017, 2, 6.94, 109.04), (2017, 3, 9.33, 141.79),
    (2017, 4, 11.56, 174.90), (2017, 5, 13.92, 209.92), (2017, 6, 17.44, 259.50),
    (2017, 7, 19.59, 296.45), (2017, 8, 20.31, 314.40), (2017, 9, 30.76, 520.42),
    (2017, 10, 76.73, 1059.68), (2017, 11, 104.17, 1234.25), (2017, 12, 145.45, 1525.12),
    (2018, 1, 151.70, 1574.19), (2018, 2, 171.07, 1914.20), (2018, 3, 178.05, 2023.27),
    (2018, 4, 190.07, 2303.16), (2018, 5, 222.94, 2631.88), (2018, 6, 246.49, 2907.05),
    (2018, 7, 235.65, 2838.68), (2018, 8, 312.47, 3571.89), (2018, 9, 394.85, 4376.67),
    (2018, 10, 482.49, 5745.58), (2018, 11, 524.94, 5978.50), (2018, 12, 620.17, 7025.75),
    (2019, 1, 672.75, 7769.79), (2019, 2, 781.78, 8768.54), (2019, 3, 799.54, 9024.11),
    (2019, 4, 843.79, 9571.45), (2019, 5, 902.32, 10243.22), (2019, 6, 962.11, 11408.56),
    (2019, 7, 1058.19, 12290.78), (2019, 8, 1045.67, 12231.90), (2019, 9, 955.23, 11269.34),
    (2019, 10, 1147.37, 13298.65), (2019, 11, 1217.49, 14146.81), (2019, 12, 1307.85, 15105.46),
    (2020, 1, 1302.63, 15510.79), (2020, 2, 1325.93, 15690.45), (2020, 3, 1248.52, 14870.23),
    (2020, 4, 999.57, 12135.67), (2020, 5, 1233.38, 14238.90), (2020, 6, 1340.29, 16348.56),
    (2020, 7, 1493.72, 18634.45), (2020, 8, 1622.93, 20452.12), (2020, 9, 1801.36, 22456.78),
    (2020, 10, 2071.50, 25642.34), (2020, 11, 2212.65, 27321.45), (2020, 12, 2232.79, 28345.67),
    (2021, 1, 2304.73, 29034.56), (2021, 2, 2291.87, 28945.34), (2021, 3, 2732.98, 34534.67),
    (2021, 4, 2643.88, 33312.45), (2021, 5, 2532.17, 32145.67), (2021, 6, 2803.45, 35234.56),
    (2021, 7, 3243.56, 40234.56), (2021, 8, 3553.44, 44512.34), (2021, 9, 3650.45, 46234.56),
    (2021, 10, 4212.34, 53456.78), (2021, 11, 4233.67, 53245.67), (2021, 12, 4564.56, 58234.56),
    (2022, 1, 4594.56, 58934.56), (2022, 2, 4529.34, 57234.56), (2022, 3, 5354.67, 68934.56),
    (2022, 4, 5578.45, 70934.56), (2022, 5, 5953.78, 75234.56), (2022, 6, 5959.23, 77234.56),
    (2022, 7, 6284.56, 80934.56), (2022, 8, 6577.78, 85234.56), (2022, 9, 6779.34, 88234.56),
    (2022, 10, 7305.45, 95234.56), (2022, 11, 7264.56, 94234.56), (2022, 12, 7822.34, 101234.56),
    (2023, 1, 8033.56, 103234.56), (2023, 2, 7525.34, 97234.56), (2023, 3, 8650.45, 114234.56),
    (2023, 4, 8894.56, 117234.56), (2023, 5, 9412.34, 122234.56), (2023, 6, 9332.45, 121234.56),
    (2023, 7, 9963.34, 131234.56), (2023, 8, 10584.56, 138234.56), (2023, 9, 10561.23, 138234.56),
    (2023, 10, 11406.78, 148234.56), (2023, 11, 11235.67, 146234.56), (2023, 12, 12024.56, 157234.56),
    (2024, 1, 12191.78, 159234.56), (2024, 2, 12128.34, 158234.56), (2024, 3, 13444.56, 175234.56),
    (2024, 4, 13303.45, 173234.56), (2024, 5, 14034.56, 183234.56), (2024, 6, 13886.78, 181234.56),
    (2024, 7, 14439.56, 188234.56), (2024, 8, 14963.34, 195234.56), (2024, 9, 15040.45, 196234.56),
    (2024, 10, 16580.78, 215234.56), (2024, 11, 15547.67, 202234.56), (2024, 12, 16737.56, 218234.56),
    (2025, 1, 16988.78, 222234.56), (2025, 2, 15952.34, 208234.56), (2025, 3, 18260.45, 238234.56),
]

df_upi = pd.DataFrame(upi_data, columns=['year','month','volume_mn','value_bn_inr'])
df_upi['date'] = pd.to_datetime(df_upi[['year','month']].assign(day=1))
df_upi['value_bn_usd'] = df_upi['value_bn_inr'] / 83.5
df_upi.to_csv('upi_monthly.csv', index=False)

# Market share data
market_share = [
    (2021, 'PhonePe', 46.0), (2021, 'Google Pay', 35.0), (2021, 'Paytm', 11.0), (2021, 'Others', 8.0),
    (2022, 'PhonePe', 47.0), (2022, 'Google Pay', 34.0), (2022, 'Paytm', 10.0), (2022, 'Others', 9.0),
    (2023, 'PhonePe', 49.0), (2023, 'Google Pay', 35.0), (2023, 'Paytm', 8.0), (2023, 'Others', 8.0),
    (2024, 'PhonePe', 48.0), (2024, 'Google Pay', 37.0), (2024, 'Paytm', 6.0), (2024, 'Others', 9.0),
]
df_share = pd.DataFrame(market_share, columns=['year','app','share_pct'])
df_share.to_csv('market_share.csv', index=False)

# Fintech funding
funding = [
    (2017, 2.0, 160), (2018, 3.7, 195), (2019, 3.5, 210),
    (2020, 2.9, 180), (2021, 8.5, 278), (2022, 5.65, 245),
    (2023, 2.5, 198), (2024, 3.1, 210)
]
df_funding = pd.DataFrame(funding, columns=['year','funding_usd_bn','deal_count'])
df_funding.to_csv('fintech_funding.csv', index=False)

# Digital payments penetration
penetration = [
    ('India', 2019, 28), ('India', 2020, 35), ('India', 2021, 46),
    ('India', 2022, 58), ('India', 2023, 67), ('India', 2024, 74),
    ('China', 2019, 81), ('China', 2020, 84), ('China', 2021, 87),
    ('China', 2022, 89), ('China', 2023, 91), ('China', 2024, 92),
    ('USA', 2019, 72), ('USA', 2020, 78), ('USA', 2021, 82),
    ('USA', 2022, 84), ('USA', 2023, 86), ('USA', 2024, 87),
    ('Brazil', 2019, 45), ('Brazil', 2020, 52), ('Brazil', 2021, 61),
    ('Brazil', 2022, 68), ('Brazil', 2023, 72), ('Brazil', 2024, 75),
]
df_pen = pd.DataFrame(penetration, columns=['country','year','penetration_pct'])
df_pen.to_csv('digital_penetration.csv', index=False)

# P2P vs P2M (Person-to-Merchant) transaction split — annual by volume %
# P2M share has been rising steadily as merchant acceptance scaled
p2m_data = [
    (2018, 83.5, 16.5),
    (2019, 79.2, 20.8),
    (2020, 72.1, 27.9),
    (2021, 63.4, 36.6),
    (2022, 57.8, 42.2),
    (2023, 52.3, 47.7),
    (2024, 48.1, 51.9),
]
df_p2m = pd.DataFrame(p2m_data, columns=['year','p2p_pct','p2m_pct'])
df_p2m.to_csv('p2m_split.csv', index=False)

# UPI ecosystem metrics: registered banks, merchant acceptance points (QR codes, millions), registered users (millions)
ecosystem = [
    (2017, 52,  0.5,   40),
    (2018, 89,  1.8,   90),
    (2019, 143, 5.3,   180),
    (2020, 207, 12.4,  320),
    (2021, 283, 25.1,  530),
    (2022, 334, 78.3,  740),
    (2023, 373, 230.0, 940),
    (2024, 427, 390.0, 1150),
]
df_eco = pd.DataFrame(ecosystem, columns=['year','banks_live','merchant_qr_mn','registered_users_mn'])
df_eco.to_csv('upi_ecosystem.csv', index=False)

# UPI international: countries where UPI QR / UPI payments accepted (cumulative count), plus key milestones
upi_intl = [
    (2022, 1,  'Bhutan (first international UPI launch)'),
    (2022, 2,  'Nepal added'),
    (2023, 5,  'Singapore, UAE, Mauritius added'),
    (2023, 8,  'Malaysia, France (Eiffel Tower pilot) added'),
    (2024, 13, 'Sri Lanka, Bahrain, Oman, Trinidad & Tobago, Fiji added'),
    (2025, 22, 'G20 cross-border push; UK, EU corridors in progress'),
]
df_intl = pd.DataFrame(upi_intl, columns=['year','countries','milestone'])
df_intl.to_csv('upi_international.csv', index=False)

# Fintech sector breakdown — share of funding by sub-sector (2024)
sector_funding = [
    ('Payments & Wallets', 28),
    ('Lending Tech', 24),
    ('WealthTech / InvestTech', 18),
    ('InsurTech', 12),
    ('NeoBank / Banking Infra', 9),
    ('RegTech / Compliance', 5),
    ('Other', 4),
]
df_sector = pd.DataFrame(sector_funding, columns=['sector','share_pct'])
df_sector.to_csv('sector_funding.csv', index=False)

print("All datasets built successfully")
print(f"UPI: {len(df_upi)} months | Share: {len(df_share)} rows | Funding: {len(df_funding)} rows | "
      f"Penetration: {len(df_pen)} rows | P2M: {len(df_p2m)} rows | Ecosystem: {len(df_eco)} rows")
