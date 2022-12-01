import pandas as pd
from datescraper import datescraper as ds

scrape = ds()


dates_df = pd.DataFrame(scrape.textExtractor("./data/medical_dataset.txt"), columns = ["raw"])
dates_df = scrape.patternApplier(dates_df)
dates_df = scrape.dataframeColumnCleaner(dates_df)
dates_df = scrape.dataframeFiller(dates_df)
dates_df = scrape.dataframeTextAppender(dates_df)
dates_df = scrape.dataframeMonthFormatter(dates_df)
scrape.exportAs(dates_df)