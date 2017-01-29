import pandas as pd
import os
import concurrent.futures

from .zefix_scraper import zefix_search_raw, zefix_search, scrape_company

def async_series_lookup(f, input_series, number_parallel_tasks=None):
    """
    Asynchronous lookup for Pandas Series
    
    The argument is simply a list, and the result is a DataFrame containing the interest as 
    a key and a value unique field called `findings_count`. 
    
    Output: f(input_series) asynchronously
    
    f -- function to apply
    input_series -- Series to apply the function on
    """
    results = pd.Series()
    
    if number_parallel_tasks is not None:
        get_executor = lambda: concurrent.futures.ThreadPoolExecutor(max_workers=number_parallel_tasks)
    else:
        get_executor = lambda: concurrent.futures.ThreadPoolExecutor()

    with get_executor() as executor:
        futures_data = {executor.submit(f, val): key for (key, val) in input_series.iteritems()}

        for future in concurrent.futures.as_completed(futures_data):
            key = futures_data[future]
            try:
                ans = future.result()
            except Exception as e:
                print("{} generated exception: {}".format(key, e))
            else: 
                results.set_value(key, ans)
            
    return results


def cached_call(generator, filename, as_series=False):
    """
    Simple function that try to load from cache or generate data (and cache it)
    
    `generator` must returns a DataFrame (and not a Series) in order to simplify the work.
    """
    path = os.path.join('cache', "{}.json".format(filename))
    try:
        if as_series:
            ans = pd.read_json(path, typ='series', orient='records')
        else:
            ans = pd.read_json(path)
    except Exception as e:
        print("Loading data... ({})".format(e))
        ans = generator()
        ans.to_json(path)
        
    return ans
