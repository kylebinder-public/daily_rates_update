import datetime
import pandas as pd
import os
import matplotlib
import rates_helper_functions_v1b as rhf

# Global variables:
print('hi_1a')
cwd = os.getcwd()
print(cwd)
now = datetime.datetime.now()
dtime_string = now.strftime("%Y-%m-%d---%H-%M-%S")
today_str = datetime.datetime.today().strftime('%Y-%m-%d')
today_dtime = datetime.datetime.today()
dir_to_send = cwd + str('\\_TO_SEND_\\') + dtime_string + str('\\')
print('hi_2x')
print(dir_to_send)
os.mkdir(dir_to_send)
print('hi_2y')

# Useful metadata for nominal rates:
first_day_with_1m_series = '07/31/01'
first_day_with_2m_series = '10/16/18'
first_day_with_3m_series = '09/01/81'
first_day_with_6m_series = '09/01/81'
first_day_with_2y_series = '06/01/76'
first_day_with_7y_series = '07/01/69'
first_day_with_30y_series = '02/15/77'

# Useful metadata for real rates:
first_day_with_20y_real_series = '07/27/04'
first_day_with_30y_real_series = '02/22/10'

# Parse today's date into "MM/DD/YY":
most_recent_day = datetime.datetime.today()
today_m = datetime.datetime.today().strftime('%m')
today_d = datetime.datetime.today().strftime('%d')
today_y = datetime.datetime.today().strftime('%y')
date_string_to_search = str(today_m) + str('/') + str(today_d) + str('/') + str(today_y)

# Use "YY" from above to determine URL of treasury.gov to scrape:
base_url_nom_OLD = str('https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx'
                       '?data '
                       '=yieldYear&year=20')
base_url_nom = str('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type'
                   '=daily_treasury_yield_curve&field_tdr_date_value=20')
url_nom = base_url_nom + str(today_y)
list_of_tables_nom = pd.read_html(url_nom, index_col=0)
df_html_nom_rates_table = list_of_tables_nom[0]
df_html_nom_rates = df_html_nom_rates_table.iloc[:, [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

# Use "YY" from above to determine URL of treasury.gov REAL RATES to scrape:
base_url_real_OLD = str(
    'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data'
    '=realyieldYear&year=20')
base_url_real = str('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type'
                    '=daily_treasury_real_yield_curve&field_tdr_date_value=20')
url_real = base_url_real + str(today_y)
list_of_tables_real = pd.read_html(url_real, index_col=0)
df_html_real_rates_table = list_of_tables_real[0]
df_html_real_rates = df_html_real_rates_table.loc[:, ['5 YR', '7 YR', '10 YR', '20 YR', '30 YR']]

# Load CSVs of pre-2022 rates (to be concatenated to what we just pulled) -
cwd = os.getcwd()
file_loc_reals = cwd + str('\\CSV_of_History\\real_rates_history.csv')
file_loc_noms = cwd + str('\\CSV_of_History\\yield_curve_history.csv')
df_csv_real_rates = pd.read_csv(file_loc_reals, index_col=0)
df_csv_nom_rates = pd.read_csv(file_loc_noms, index_col=0)

# Concatenate HTML DF (2022+) and CSV DF (pre-2022):
df_reals = pd.concat([df_csv_real_rates, df_html_real_rates])
df_noms = pd.concat([df_csv_nom_rates, df_html_nom_rates])

# Prepare labels for plots of nominal yields:
maturities = pd.DataFrame(columns=['YRS'],
                          data=[0.08, 0.16, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30],
                          index=['1 Mo', '2 Mo', '3 Mo', '6 Mo',
                                 '1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr', '20 Yr', '30 Yr'])
df2 = df_noms.iloc[[-21, -6, -2, -1], :]
df3 = df2.transpose()
df4 = pd.concat([df3, maturities], axis=1)
df5 = df4.set_index('YRS')

df12 = df_noms.iloc[[-505, -252, -63, -1], :]
df13 = df12.transpose()
df14 = pd.concat([df13, maturities], axis=1)
df15 = df14.set_index('YRS')

# Prepare labels for plots of real yields:
maturities_real = pd.DataFrame(columns=['YRS'],
                               data=[5, 7, 10, 20, 30],
                               index=['5 YR', '7 YR', '10 YR', '20 YR', '30 YR'])
df2r = df_reals.iloc[[-21, -6, -2, -1], :]
df3r = df2r.transpose()
df4r = pd.concat([df3r, maturities_real], axis=1)
df5r = df4r.set_index('YRS')

df12r = df_reals.iloc[[-505, -252, -63, -1], :]
df13r = df12r.transpose()
df14r = pd.concat([df13r, maturities_real], axis=1)
df15r = df14r.set_index('YRS')

# Plot 1: Full Yield Curve of Nominal Rates: up to past month
plotD1 = df5.plot(color=['red', 'orange', 'green', 'blue'],
                  style=['o-', 'o-', 'o-', 'o-']);
plotD1.set_ylabel("Nominal Yields (%) - Full Curve");
figD1 = plotD1.get_figure();
figD1_str = str(dir_to_send) + str('01_NomYields_') + str(dtime_string) + str('.png')
figD1.savefig(figD1_str);
matplotlib.pyplot.close(figD1);

# Plot 2: Full Yield Curve of Real Rates: up to past month
plotR1 = df5r.plot(color=['red', 'orange', 'green', 'blue'],
                   style=['o-', 'o-', 'o-', 'o-']);
plotR1.set_ylabel("Real Yields (%) - Full Curve");
figR1 = plotR1.get_figure();
figR1_str = str(dir_to_send) + str('02_RealYields_') + str(dtime_string) + str('.png')
figR1.savefig(figR1_str);
matplotlib.pyplot.close(figR1);

# Plot 3: Full Yield Curve of Nominal Rates: {Today, 3 months ago, 1 yr, 2 yr}
plotD2 = df15.plot(color=['red', 'orange', 'green', 'blue'],
                   style=['o-', 'o-', 'o-', 'o-']);
plotD2.set_ylabel("Nominal Yields (%) - Full Curve");
figD2 = plotD2.get_figure();
figD2_str = str(dir_to_send) + str('03_NomYields_') + str(dtime_string) + str('.png')
figD2.savefig(figD2_str);
matplotlib.pyplot.close(figD2);

# Plot 4: Full Yield Curve of Real Rates: {Today, 3 months ago, 1 yr, 2 yr}
plotR2 = df15r.plot(color=['red', 'orange', 'green', 'blue'],
                    style=['o-', 'o-', 'o-', 'o-']);
plotR2.set_ylabel("Real Yields (%) - Full Curve");
figR2 = plotR2.get_figure();
figR2_str = str(dir_to_send) + str('04_RealYields_') + str(dtime_string) + str('.png')
figR2.savefig(figR2_str);
matplotlib.pyplot.close(figR2);

# Plot 5: Front of Curve (up to 7YR) of Nominal Rates: {Today, yesterday, last week, last month}
plotD5 = df5.iloc[:-3, :].plot(color=['red', 'orange', 'green', 'blue'],
                               style=['o-', 'o-', 'o-', 'o-']);
plotD5.set_ylabel("Nominal Yields (%) - Front of Curve");
figD5 = plotD5.get_figure();
figD5_str = str(dir_to_send) + str('05_NomYields_') + str(dtime_string) + str('.png')
figD5.savefig(figD5_str);
matplotlib.pyplot.close(figD5);

# Plot 6: Front of Curve (up to 7YR) of Nominal Rates: {Today, 6 months ago, 1 yr, 2 yr}
plotD6 = df15.iloc[:-3, :].plot(color=['red', 'orange', 'green', 'blue'],
                                style=['o-', 'o-', 'o-', 'o-']);
plotD6.set_ylabel("Nominal Yields (%) - Front of Curve");
figD6 = plotD6.get_figure();
figD6_str = str(dir_to_send) + str('06_NomYields_') + str(dtime_string) + str('.png')
figD6.savefig(figD6_str);
matplotlib.pyplot.close(figD6);
print('hi_3a')

# Load email credentials from separate directory:
cred_dir = cwd + str('\\Credentials\\gmail_credentials.csv')
csv_credentials = pd.read_csv(cred_dir, header=None)
gmail_username = csv_credentials.iloc[0, 0]
gmail_pw = csv_credentials.iloc[1, 0]
to_address_list = []  # fill this in from txt/csv to be loaded

# Load email recipients from separate directory:
recipient_dir = cwd + str('\\Recipient_List\\email_addresses_to_spam.csv')
csv_recipients = pd.read_csv(recipient_dir, header=None)
recipient_address_list = csv_recipients.iloc[:, 0]  # fill this in from txt/csv to be loaded

# Format string of text to be included in email message:
str1 = str(df_noms.iloc[-1])
str2 = str1.replace('\n', '<br>')
str3 = str(df_noms.iloc[-2])
str4 = str3.replace('\n', '<br>')
str5 = str(df_noms.iloc[-21])
str6 = str5.replace('\n', '<br>')
str7 = str(df_noms.iloc[-252])
str8 = str7.replace('\n', '<br>')
str91 = str(df_noms.iloc[-505])
str92 = str91.replace('\n', '<br>')
str93 = str(df_noms.iloc[-1260])
str94 = str93.replace('\n', '<br>')
str7 = str(df_noms.iloc[-252])
str8 = str7.replace('\n', '<br>')
str1r = str(df_reals.iloc[-1])
str2r = str1r.replace('\n', '<br>')
str3r = str(df_reals.iloc[-2])
str4r = str3r.replace('\n', '<br>')
str5r = str(df_reals.iloc[-21])
str6r = str5r.replace('\n', '<br>')
str7r = str(df_reals.iloc[-252])
str8r = str7r.replace('\n', '<br>')
str91r = str(df_reals.iloc[-505])
str92r = str91r.replace('\n', '<br>')
str93r = str(df_reals.iloc[-1260])
str94r = str93r.replace('\n', '<br>')
stats_text_B = \
    'Nominal Yields: Most Recent: ' + \
    str('<br>') + str('<br>') + \
    str(str2) + \
    str('<br>') + str('<br>') + \
    'Nominal Yields: Previous Day: ' + \
    str('<br>') + str('<br>') + \
    str(str4) + \
    str('<br>') + str('<br>') + \
    'Nominal Yields: Previous Month: ' + \
    str('<br>') + str('<br>') + \
    str(str6) + \
    str('<br>') + str('<br>') + \
    'Nominal Yields: Previous Year: ' + \
    str('<br>') + str('<br>') + \
    str(str8) + \
    str('<br>') + str('<br>') + \
    'Nominal Yields: 2 Years Ago: ' + \
    str('<br>') + str('<br>') + \
    str(str92) + \
    str('<br>') + str('<br>') + \
    'Nominal Yields: 5 Years Ago: ' + \
    str('<br>') + str('<br>') + \
    str(str94) + \
    str('<br>') + str('<br>') + \
    'Real Yields: Most Recent: ' + \
    str('<br>') + str('<br>') + \
    str(str2r) + \
    str('<br>') + str('<br>') + \
    'Real Yields: Previous Day: ' + \
    str('<br>') + str('<br>') + \
    str(str4r) + \
    str('<br>') + str('<br>') + \
    'Real Yields: Previous Month: ' + \
    str('<br>') + str('<br>') + \
    str(str6r) + \
    str('<br>') + str('<br>') + \
    'Real Yields: Previous Year: ' + \
    str('<br>') + str('<br>') + \
    str(str8r) + \
    str('<br>') + str('<br>') + \
    'Real Yields: 2 Years Ago: ' + \
    str('<br>') + str('<br>') + \
    str(str92r) + \
    str('<br>') + str('<br>') + \
    'Real Yields: 5 Years Ago: ' + \
    str('<br>') + str('<br>') + \
    str(str94r) + \
    str('<br>') + str('<br>')

# Send as email:
subj_string = str('Daily Rates Update: [') + str(dtime_string) + str(']')
msg_text_01 = str('Daily Rates Update:') + \
                str('<br>') + str('<br>') + \
                stats_text_B
rhf.send_mail_gmail(username=gmail_username, password=gmail_pw,\
                toaddrs_list=recipient_address_list,\
                msg_text = msg_text_01, fromaddr='JOSIAH BARTLET', \
                subject = subj_string,
                attachment_path_list = dir_to_send)
print('hi_4a')
