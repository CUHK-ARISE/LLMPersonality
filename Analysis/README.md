# Visualization

## Execution Process

### Specify the Projection Matrix
Construct all grids ranging from the minimum to maximum score of the questionnaire as a standard reference frame
```py
construct_reference("<questionnaire_name>", "<save_name>")
```

### Visualize data points
1. Create a Visualize instance with PCA projection matrix using the standard reference frame
```py
# Extract the reference frame from JSON
reference = extract_reference('<reference_path>')
# Create the instance
vis = Visualize('<questionnaire_name>', reference)
```

2. Add the data points on the constructed plane
```py
# Extract the data from JSON
data, _ = extract_data('<data_path>')

# Add the data
vis.add(data, "<color>", "<label>")

# Add the filtered data using DataFrame operations
vis.add(data["<aspect>"], "<color>", "<label>")
```

3. Visualize the current constructed plane
```py
vis.plot()

# Save the figure
vis.plot(savename="<fig_name>")

# Visualize the data with randomized z-order
vis.plot(random_zorder=True)
```

4. Clear the plane
```py
vis.clean()
```
