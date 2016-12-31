import pandas as pd
import json

def gen_temporal_map_data():
  def parse_date(x):
    if x!='':
      year = int(x.split('-')[-1])
    else:
      year = -1

    return year

  base = pd.read_csv('../data/panama/Entities.csv', header=0,
      low_memory=False)
  filtered = base[base.country_codes.str.contains(';')==False]

  filtered['inactivation_year'] = \
    filtered.inactivation_date.fillna('').apply(parse_date)

  min_data = filtered[['inactivation_year', 'name', 'country_codes']]
  min_data = min_data[(min_data.inactivation_year >= 1990) |
          (min_data.inactivation_year == -1)]
  grouped = min_data.groupby(['inactivation_year', 'country_codes']).count()

  #grouped.to_json('../data/number_closing_account_per_year.json')
  ans = {}
  for year, sub_df in grouped.groupby(level=0):
      year = str(year.astype(int))
      clean_df = sub_df.reset_index()[['country_codes',
          'name']].set_index('country_codes').name.to_dict()
    
      locations = list(clean_df)
      values = [int(clean_df[k]) for k in locations]
      ans[year] = {
        'locations': locations,
        'values': values,
      }

      #without_numpy = {k: int(v) for (k,v) in clean_df.items()}
      #ans[year] = without_numpy

  with open('data/number_closing_account_per_year.json', 'w') as f:
    json.dump(ans, f, sort_keys=True)

  #from pprint import PrettyPrinter as PP
  #PP(indent=4).pprint(ans)

if __name__=="__main__":
  gen_temporal_map_data()
