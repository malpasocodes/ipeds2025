# Incorporating a New Year in the Streamlit App

After successfully creating and verifying a new parquet file, follow these steps to incorporate it into the Streamlit app.

## 1. Update Config File

Edit `app/config.py` to add the new year to YEAR_OPTIONS:

```python
# Current YEAR_OPTIONS
YEAR_OPTIONS = {
    "2022-23": "2223",
    "2021-22": "2122",
    "2020-21": "2021",
    "2019-20": "2020",
    "2018-19": "2019"
}

# Add new year (2017-18)
YEAR_OPTIONS = {
    "2022-23": "2223",
    "2021-22": "2122",
    "2020-21": "2021",
    "2019-20": "2020",
    "2018-19": "2019",
    "2017-18": "2018"  # new entry
}
```

## 2. Test Data Loading

1. Stop the Streamlit app if it's running
2. Clear Streamlit cache:
   ```bash
   rm -rf ~/.streamlit/cache
   ```
3. Restart the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```

## 3. Verify in App

Check the following:

1. Navigation
   - New year appears in year selection dropdown
   - Year appears in correct order (newest to oldest)

2. Pell Grant Analysis
   - Select new year (2017-18)
   - Verify data loads without errors
   - Check scatter plot displays correctly
   - Confirm summary statistics calculate properly

3. Federal Loan Analysis
   - Select new year
   - Verify data loads
   - Check visualizations
   - Verify calculations

4. Total Aid Analysis
   - Select new year
   - Verify combined calculations
   - Check visualizations
   - Confirm summary statistics

5. Institution Profile
   - Select an institution
   - Verify new year appears in timeline
   - Check all metrics display correctly

## 4. Common Issues and Solutions

If you encounter:

1. **Year not appearing in dropdown**
   - Verify YEAR_OPTIONS updated correctly
   - Check for typos in year format

2. **Data not loading**
   - Confirm parquet file is in correct location
   - Check file permissions
   - Verify file name matches YEAR_OPTIONS mapping

3. **Visualization errors**
   - Check console for error messages
   - Verify numeric columns are properly formatted
   - Confirm required columns present for plots

4. **Cached data issues**
   - Clear Streamlit cache
   - Restart Streamlit app

## 5. Final Checks

Before considering the integration complete:

1. Compare metrics with existing years for consistency
2. Test all filters with new year selected
3. Verify performance/load times are acceptable
4. Check institution counts match expected values

## 6. Backup Recommendation

Before making any changes:
1. Backup existing config.py
2. Note current settings
3. Document any issues encountered for future reference

## 7. Next Steps

If everything works correctly:
1. Document successful incorporation of new year
2. Update any relevant documentation
3. Proceed with next historical year if needed
4. Consider creating a test dataset for future additions