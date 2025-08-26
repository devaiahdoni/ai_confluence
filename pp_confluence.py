from atlassian import Confluence
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Setup authentication and Confluence connection
confluence = Confluence(
    url='https://your-confluence-url',
    username='your-username',
    password='your-api-token'
)
space = 'SPACEKEY'
title = 'PAGE TITLE'

# Get page ID
page_id = confluence.get_page_id(space, title)

# Get the page and extract the table HTML
page = confluence.get_page_by_id(page_id, expand='body.storage')
html = page['body']['storage']['value']
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table')  # get first table

# Convert table HTML to pandas dataframe
df = pd.read_html(str(table))

# Get current day column name (e.g., Aug 25 2025)
today_col = datetime.now().strftime('%b %d %Y')
if today_col not in df.columns:
    df[today_col] = ''  # Add new column for today

# Update the message in the current day's column for all rows or a specific row
# For example, update the first row
df.at[0, today_col] = 'Updated message for today!'

# Convert DataFrame to HTML table (with Confluence formatting)
df_html = df.to_html(index=False, escape=False)
soup.table.replace_with(BeautifulSoup(df_html, 'html.parser'))

# Update page with new table
new_html = str(soup)
new_ver = page['version']['number'] + 1

confluence.update_page(
    page_id=page_id,
    title=title,
    body=new_html,
    representation='storage',
    minor_edit=True,
    version_comment=f"Added column {today_col} and updated message."
)

print("Confluence page updated successfully.")
