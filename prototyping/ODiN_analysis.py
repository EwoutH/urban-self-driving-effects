#%% md
# ## ODIN EDA
# 
# https://ssh.datastations.nl/dataset.xhtml?persistentId=doi:10.17026/SS/BXIK2X
#%% md
# ### Imports and reading data
#%%
import pandas as pd
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
#%%
# Read ODiN2023_Databestand.sav. Decimal separator is comma.
reload = False
if reload:
    df = pd.read_spss("data/ODiN2023_Databestand.sav", convert_categoricals=False)
    print(len(df))
    
    # Convert all columns that only contain integers to integers.
    for col in df.columns:
        col_type = df[col].dtype
        if col_type == 'object':
            # Convert 'object' columns to 'string'
            df[col] = df[col].astype('string')
        elif col_type == 'float64':
            if df[col].dropna().apply(lambda x: x.is_integer()).all():
                min_val, max_val = df[col].min(), df[col].max()
                if df[col].isnull().any():
                    for dtype in ['Int8', 'Int16', 'Int32', 'Int64']:
                        if np.iinfo(dtype.lower()).min <= min_val and np.iinfo(dtype.lower()).max >= max_val:
                            df[col] = df[col].astype(dtype)
                            break
                else:
                    for dtype in ['int8', 'int16', 'int32', 'int64']:
                        if np.iinfo(dtype).min <= min_val and np.iinfo(dtype).max >= max_val:
                            df[col] = df[col].astype(dtype)
                            break
    # Save as parquet
    pq.write_table(pa.Table.from_pandas(df), 'data/ODiN2023.parquet', compression='snappy')
else:
    df = pd.read_parquet('data/ODiN2023.parquet')
print(df.info())
df.head()
#%%
# Filter the OPIDs that are most present in the dataset
df["OPID"].value_counts().head(5)
#%%
# Filter OPID == 272797165969
df[df["OPID"] == 272797165969].head()
#%%
df['KRvm'].value_counts()
#%%
bike_over_100km = df[(df['Reisduur'] > 100) & (df['KRvm'] == 4)]
print("Unexpected bike trips over 100km:", len(bike_over_100km))

# Total share of bikes in trips over 100km
over_100km = df[df['Reisduur'] > 100]
print("Total trips over 100km:", len(over_100km))
print("Share of bikes in trips over 100km:", len(bike_over_100km) / len(over_100km))
#%%
# Combine 'Jaar', 'Maand' and 'Dag' to a single Datum column.
df["Datum"] = pd.to_datetime(df[["Jaar", "Maand", "Dag"]].astype(str).agg('-'.join, axis=1))
#%% md
# ### Exploration
#%%
# Read codebook Excel
codebook = pd.read_excel("data/ODiN2023_Codeboek_v1.0.xlsx", usecols=["Variabele_naam_ODiN_2023", "Variabele_label_ODiN_2023"])
# Drop rows with NaN
codebook = codebook.dropna()
codebook.head()
#%%
codebook_dict = codebook.set_index("Variabele_naam_ODiN_2023")["Variabele_label_ODiN_2023"].to_dict()
#%%
# Load the Excel file
excel_path = 'data/ODiN2023_Codeboek_v1.0.xlsx'
df_codebook = pd.read_excel(excel_path)

# Initialize the nested dictionary
codebook_labels = {}

# Initialize a variable to keep track of the current variable name
current_var_name = None

# Iterate over the DataFrame rows
for _, row in df_codebook.iterrows():
    # Check if the row contains a new variable name
    if pd.notna(row['Variabele_naam_ODiN_2023']):
        current_var_name = row['Variabele_naam_ODiN_2023']
        codebook_labels[current_var_name] = {}

    # If the row contains a code, add it to the current variable's dictionary
    if pd.notna(row['Code_ODiN_2023']) and pd.notna(row['Code_label_ODiN_2023']):
        codebook_labels[current_var_name][row['Code_ODiN_2023']] = row['Code_label_ODiN_2023']

codebook_labels["Doel"]
#%% md
# #### How many trips does a single person make?
#%%
# Lookup the VertLoc
var = "Toer"
print(f"{var}: {codebook_dict[var]}\n* Categories: {codebook_labels[var]}")
# Get normalized percentages of the variable
normalized_counts = df[var].value_counts(normalize=True, sort=False, dropna=False).to_dict()
normalized_counts_nonnan = df[var].value_counts(normalize=True, sort=False, dropna=True).to_dict()
# Use the codebook dict to add the var name to the keys
normalized_counts = {k: f"{v:.1%}" for k, v in normalized_counts.items()}
normalized_counts_nonnan = {k: f"{v:.1%}" for k, v in normalized_counts_nonnan.items()}
# if k in codebook_labels[var], replace k with codebook_labels[var][k]
normalized_counts = {f"{k}_{codebook_labels[var].get(k, "")}": v for k, v in normalized_counts.items()}
normalized_counts_nonnan = {f"{k}_{codebook_labels[var].get(k, "")}": v for k, v in normalized_counts_nonnan.items()}
print(f"* Normalized counts: {normalized_counts}")
print(f"* Normalized counts without NaN: {normalized_counts_nonnan}")

# Plot unique value histogram of var. Figure size 4x3.
fig = plt.figure(figsize=(4, 2))
sns.histplot(df[var])
#%%
# Select 5 random OPIDs
random_OPIDs = df["OPID"].sample(7)
random_trips = df[df["OPID"].isin(random_OPIDs)]
random_trips
#%%
# Value counts when both OPID and datum are both identical
trip_counts = (df["OPID"].astype(str) + "_" + df["Datum"].astype(str)).value_counts()

# Create a historgram of the trip counts
sns.histplot(trip_counts, kde=False, binwidth=1)
# Add title and labels
plt.title('Number of trips per person')
plt.xlabel('Number of trips')
plt.ylabel('Number of people')
# Save the plot as a PNG file
plt.savefig("img/trip_counts_histogram.png", dpi=300, bbox_inches='tight')
#%%
trip_counts
#%%
# Average and median number of trips
print(f"Average number of trips: {trip_counts.mean()}")
print(f"Median number of trips: {trip_counts.median()}")
#%%
# Save the trip counts distribution as a pickle file
trip_counts_distribution = trip_counts.value_counts().sort_index()
trip_counts_distribution = trip_counts_distribution / trip_counts_distribution.sum()
trip_counts_distribution.to_pickle("../data/trip_counts_distribution.pickle")
#%% md
# #### How many trips are made in each movement?
#%%
# 
#%% md
# #### How long are trips for each mode of transport?
#%%
# Create a histogram of the trip durations
sns.histplot(df["Reisduur"], kde=False, binwidth=5, binrange=(0, 120))
# Add title and labels
plt.title(f'Distribution of trip durations for reisduur')
plt.xlabel('Trip duration (minutes)')
plt.ylabel('Number of trips')
plt.savefig("img/trip_durations_histogram.png", dpi=300, bbox_inches='tight')
#%%
codebook_labels["KRvm"]
#%%
# 1. Determine unique bin edges based on quantiles
num_bins = 50
quantile_edges = np.linspace(0, 1, num_bins+1)
bin_edges = df['Reisduur'].quantile(quantile_edges).unique()
bin_edges = np.sort(bin_edges)  # Ensure the edges are sorted after dropping duplicates

# Extend the last bin edge to include the maximum value
bin_edges = np.append(bin_edges, df['Reisduur'].max() + 1)

# Create bin labels showing the range without duplicate numbers on the edges
bin_labels = [f"{int(bin_edges[i])}-{int(bin_edges[i+1]-1)}" for i in range(len(bin_edges)-2)]
bin_labels.append(f"{int(bin_edges[-2])}-{int(bin_edges[-1]-1)}")  # For the last bin, include the max value

df['binned'] = pd.cut(df['Reisduur'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# 2. Calculate percentages
grouped = df.groupby(['binned', 'KRvm'], observed=True).size().reset_index(name='count')

# Pivot the data for percentage calculation
pivot_df = grouped.pivot(index='binned', columns='KRvm', values='count').fillna(0)

# Drop any bins that do not contain any data
pivot_df = pivot_df.loc[pivot_df.sum(axis=1) > 0]

# Replace the numeric 'KRvm' categories with the actual labels
pivot_df.columns = pivot_df.columns.map(codebook_labels['KRvm'])

# Flip the order of the columns, but keep the last one in place
pivot_df = pivot_df[pivot_df.columns[::-1]]

# Calculate the percentages
percentages = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# 3. Plot
percentages.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.xticks(rotation=45)
plt.ylabel('Percentage van de trips (%)')
plt.xlabel('Reisduur (minuten)')
plt.title('Aandeel vervoersmethodes over verschillende reisduren')
plt.legend(title='Vervoersmethode', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig("img/trips_by_mode_and_duration_stacked.png", dpi=300, bbox_inches='tight')
#%%
# Create a histogram of the trip distances
sns.histplot(df["AfstR"], kde=False, binwidth=10, binrange=(0, 120))
# Add title and labels
plt.title("Distribution of trip distances")
plt.xlabel("Trip distance (km)")
plt.ylabel("Number of trips")
plt.savefig("img/trip_distances_histogram.png", dpi=300, bbox_inches='tight')
#%%
# 1. Determine unique bin edges based on quantiles
num_bins = 40
quantile_edges = np.linspace(0, 1, num_bins+1)
bin_edges = df['AfstR'].quantile(quantile_edges).unique()
bin_edges = np.sort(bin_edges)  # Ensure the edges are sorted after dropping duplicates

# Extend the last bin edge to include the maximum value
bin_edges = np.append(bin_edges, df['AfstR'].max() + 1)

# Create bin labels showing the range without duplicate numbers on the edges
bin_labels = [f"{int(bin_edges[i])}-{int(bin_edges[i+1]-1)}" for i in range(len(bin_edges)-2)]
bin_labels.append(f"{int(bin_edges[-2])}-{int(bin_edges[-1]-1)}")  # For the last bin, include the max value

df['binned'] = pd.cut(df['AfstR'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# 2. Calculate percentages
grouped = df.groupby(['binned', 'KRvm'], observed=True).size().reset_index(name='count')

# Pivot the data for percentage calculation
pivot_df = grouped.pivot(index='binned', columns='KRvm', values='count').fillna(0)

# Drop any bins that do not contain any data
pivot_df = pivot_df.loc[pivot_df.sum(axis=1) > 0]

# Replace the numeric 'KRvm' categories with the actual labels
pivot_df.columns = pivot_df.columns.map(codebook_labels['KRvm'])

# Flip the order of the columns, but keep the last one in place
pivot_df = pivot_df[pivot_df.columns[::-1]]

# Calculate the percentages
percentages = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# 3. Plot
percentages.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.xticks(rotation=45)
plt.ylabel('Percentage van de trips (%)')
plt.xlabel('Afstand (kilometer)')
plt.title('Aandeel vervoersmethodes over verschillende afstanden')
plt.legend(title='Vervoersmethode', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig("img/trips_by_mode_and_distance_stacked.png", dpi=300, bbox_inches='tight')
#%%
# Create a heatmap of trip distances by mode of transport
pivot_table = df.pivot_table(index="KRvm", columns="KAfstR", values="OPID", aggfunc="count")
# Replace the mode codes with the mode labels (from the codebook)
pivot_table.index = pivot_table.index.map(codebook_labels["KRvm"])
pivot_table.columns = pivot_table.columns.map(codebook_labels["KAfstR"])
pivot_table.drop("Geen rit in Nederland", axis=1)
# Create a heatmap
sns.heatmap(pivot_table, cmap="magma")
# Add title and labels
plt.title("Number of trips by mode of transport and trip distance")
plt.xlabel("Trip distance class (km)")
plt.ylabel("Mode of transport")
# Save the plot as a PNG file
plt.savefig("img/trips_by_mode_and_distance_heatmap.png", dpi=300, bbox_inches='tight')
#%% md
# #### How many trips are made during the week?
#%%
# Calculate the number of trips by hour in the week
df["Hour"] = df["VertUur"]
df["Weekday"] = df["Datum"].dt.dayofweek
df["Weekend"] = df["Weekday"] >= 5

# Create a pivot table with the number of trips by hour and day of the week
trips_by_hour = df.pivot_table(index="Hour", columns="Weekday", values="OPID", aggfunc="count")

# Plot the pivot table as a heatmap
sns.heatmap(trips_by_hour, cmap="magma")
plt.title('Number of trips by hour and day of the week')
plt.xlabel('Weekday')
plt.ylabel('Hour')
# Align the x-axis labels centered
plt.xticks(ticks=range(7), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rotation=30, ha="left")
plt.savefig("../img/trips_by_weekday_and_hour_heatmap.svg", bbox_inches='tight')
#%%
df["HourFloat"] = df["VertUur"] + df["VertMin"] / 60
# Round down to the nearest quarter, using modular division
df["HourQuarter"] = (df["HourFloat"] // 0.25) * 0.25

# Create a pivot table with the number of trips by quarter hour and day of the week
trips_by_quarter_hour = df.pivot_table(index="HourQuarter", columns="Weekday", values="OPID", aggfunc="count")

# Plot the pivot table as a heatmap
sns.heatmap(trips_by_quarter_hour, cmap="magma")
plt.title('Number of trips by quarter hour and day of the week')
plt.xlabel('Weekday')
plt.ylabel('Hour')
# Align the x-axis labels centered
plt.xticks(ticks=range(7), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rotation=30, ha="left")
plt.savefig("img/trips_by_weekday_and_quarter_hour_heatmap.png", dpi=300, bbox_inches='tight')
#%% md
# As can be seen, quarterly hours shows issues with people rounding to the nearest hour, which makes it not useful for analysis.
#%%
# Create a pivot table with the chance that someone starts a trip at a certain hour on a certain day
trips_by_hour = df.pivot_table(index="Hour", columns="Weekday", values="OPID", aggfunc="count")

# Filter the df to only include trips with a valid VertUur
df_vert = df.dropna(subset=["VertUur", "Weekday"])
print(f"Number of rows before filtering: {len(df)}, after filtering: {len(df_vert)}")
OPID_count_per_day_of_week = df_vert.groupby("Weekday")["OPID"].nunique()
print(OPID_count_per_day_of_week)

# Normalize the pivot table to show the chance that someone starts a trip at a certain hour on a certain day
trips_by_hour_normalized = trips_by_hour.div(OPID_count_per_day_of_week, axis=1)
# Print the total of each row
trips_by_hour_normalized.loc["Total"] = trips_by_hour_normalized.sum()
# Save as pickle to ../data
trips_by_hour_normalized.to_pickle("../data/trips_by_hour_chances.pickle")
# Format numbers as percentages (without multiplying by 100)
trips_by_hour_normalized.map("{:.2%}".format)
#%%
# Create a plot of the chance that someone starts a trip at a certain hour using the average of Monday-Thursday
trips_by_hour_normalized_average = trips_by_hour_normalized.loc[:, :4].mean(axis=1)
# Drop the first 5 rows and the last row (Total)
trips_by_hour_normalized_average = trips_by_hour_normalized_average.iloc[5:-1]
# Create a barplot using seaborn. Format in percentages.
plt.figure(figsize=(10, 6))
sns.barplot(x=trips_by_hour_normalized_average.index, y=trips_by_hour_normalized_average)
# Add the number of trips to the bars
for i, v in enumerate(trips_by_hour_normalized_average):
    plt.text(i, v, f"{v:.1%}", ha="center", va="bottom")
# Format the y-axis as percentages
plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
# Add title and labels
plt.title("Chance that someone starts a trip at a certain hour (average of Monday-Thursday)")
plt.xlabel("Hour")
plt.ylabel("Chance")
# Save as svg to ../img
plt.savefig("../img/chance_of_starting_trip_by_hour.svg", bbox_inches='tight')
#%% md
# #### How many trips are made by each mode of transport?
#%%
# Create a function to create a circle plot from a variable name
def create_circle_plot(variable_name, title):
    # Create a circle plot of the number of trips by mode of transport
    counts = df[variable_name].value_counts()
    # Replace the mode codes with the mode labels (from the codebook)
    counts.index = counts.index.map(codebook_labels[variable_name])

    # Plot the circle plot with seaborn
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
    plt.title(title)
#%%
# Create a circle plot of the number of trips by mode of transport
create_circle_plot("KRvm", "Number of trips by mode of transport")
plt.savefig("img/trips_by_mode_circle_plot.png", dpi=300, bbox_inches='tight')
#%%
# Doel and Motive
create_circle_plot("Doel", "Number of trips by purpose")
plt.savefig("img/trips_by_purpose_circle_plot.png", dpi=300, bbox_inches='tight')
#%%
create_circle_plot("MotiefV", "Number of trips by motive")
plt.savefig("img/trips_by_motive_circle_plot.png", dpi=300, bbox_inches='tight')
#%%
# Create a heatmap of the number of trips by mode of transport and purpose
pivot_table = df.pivot_table(index="KRvm", columns="MotiefV", values="OPID", aggfunc="count")
# Replace the mode codes with the mode labels (from the codebook)
pivot_table.index = pivot_table.index.map(codebook_labels["KRvm"])
pivot_table.columns = pivot_table.columns.map(codebook_labels["MotiefV"])
# Create a heatmap
sns.heatmap(pivot_table, cmap="magma")
# Add title and labels
plt.title("Number of trips by mode of transport and purpose")
plt.xlabel("Purpose")
plt.ylabel("Mode of transport")
# Save the plot as a PNG file
plt.savefig("img/trips_by_mode_and_purpose_heatmap.png", dpi=300, bbox_inches='tight')
#%%
# Plot the share of bike trips by month
bike_trips = df[df["KRvm"] == 5]
bike_trips_by_month = bike_trips["Maand"].value_counts().sort_index()
# Share of bike trips by month
share_bike_trips = bike_trips_by_month / df["Maand"].value_counts().sort_index()
# Plot the share of bike trips by month
share_bike_trips.plot(kind="bar")
plt.title("Share of bike trips by month")
plt.xlabel("Month")
plt.ylabel("Share of bike trips")
plt.xticks(rotation=30)
# ylabels as percentages
plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
# xlabels as month names
plt.gca().set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
plt.savefig("img/share_of_bike_trips_by_month.png", dpi=300, bbox_inches='tight')
#%%
# Get the unique values of the 'VertLoc' column
df["WoGem"].unique()
#%%
# Create a table of the number of trips by postal code (as index) and mode of transport (each mode as a column)
trips_by_postal_code = df.pivot_table(index="WoGem", columns="KRvm", values="OPID", aggfunc="count")
# Replace the mode codes with the mode labels (from the codebook)
trips_by_postal_code.columns = trips_by_postal_code.columns.map(codebook_labels["KRvm"])
# Replace the NaN values with 0
trips_by_postal_code = trips_by_postal_code.fillna(0)
# Save as pickle
trips_by_postal_code.to_pickle("data/trips_by_postal_code.pickle")
trips_by_postal_code.head()
#%%
# Filter the trips by WoGE 1667
trips_reusel = df[df["WoGem"] == 1667]

# Get the unique number of OPID
unique_OPID = trips_reusel["OPID"].nunique()

# Get the number of trips by mode of transport per OPID (group by OPID and KRvm)
trips_by_mode = trips_reusel.groupby(["OPID", "KRvm"]).size().unstack(fill_value=0)

# Replace the column codes with the mode labels (from the codebook)
trips_by_mode.columns = trips_by_mode.columns.map(codebook_labels["KRvm"])

# reset the index
trips_by_mode = trips_by_mode.reset_index().drop("OPID", axis=1)
trips_by_mode.head()
#%% md
# ### EDA
#%%
# Drop all rows that have a missing value in the KRvm column
print(f"Number of rows before dropping missing values: {len(df)}")
df = df.dropna(subset=["KRvm"])
print(f"Number of rows after dropping missing values: {len(df)}")
#%%
# From ODiN 2022 to 2023, the Herkomst column was replaced with HerkLand
variables_to_include = ["KRvm", "Sted", "GemGr", "Doel", "MotiefV", "AfstR", "Reisduur", "VertUur", "Weekdag", "Maand", "Feestdag", "Prov", "Geslacht", "Leeftijd", "HerkLand", "Opleiding", "BetWerk", "OnbBez", "HHGestInkG", "HHRijbewijsAu", "OPRijbewijsAu", "HHAuto", "HHAutoL", "BrandstofPa1", "BouwjaarPa1", "HHEFiets", "OVStKaart", "WrkVerg", "VergVast", "AantRit", "Verpl", "Toer", "MeerWink", "VertLoc", "ActDuur", "SDezPlts"]
#%%
# Create a dataframe with the variable code, label, description the codebook_labels dictionary
df_codebook = pd.DataFrame(codebook)
df_codebook = df_codebook[df_codebook["Variabele_naam_ODiN_2023"].isin(variables_to_include)]
df_codebook["options_dict"] = df_codebook["Variabele_naam_ODiN_2023"].map(codebook_labels)
df_codebook
#%%
# Choose a dataframe to use here:
df_to_split = df[variables_to_include].copy()

# Split in input and output variable
X = df_to_split.drop('KRvm', axis=1)
y = df_to_split['KRvm']
#%%
# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Split train set into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.5, random_state=42)
#%%
# Read the variable types from ODiN_variable_types.xlsx to a dict, with Type as key and Variabele_naam_ODiN_2023 as list of values for that type
variable_types = pd.read_excel("data/ODiN_variable_types.xlsx")
variable_types_dict = variable_types.groupby("Type")["Variabele_naam_ODiN_2022"].apply(list).to_dict()
variable_types_dict
#%% md
# ### Model selection and development
#  - Choose appropriate algorithms: Select suitable machine learning algorithms based on your problem type, such as logistic regression, decision trees, random forests, support vector machines, or neural networks.
#  - Train the models: Train the selected algorithms on the training dataset and use the validation dataset to tune hyperparameters and assess performance.
#  - Model evaluation: Compare the performance of the different models using relevant evaluation metrics such as accuracy, precision, recall, F1-score, or AUC-ROC.
# 
# Output: `results_df`
#%%
# Mode dict from codebook
mode_dict = codebook_labels["KRvm"]
mode_dict
#%%
# Imports
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix

from sklearn.naive_bayes import CategoricalNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier

# Create a dictionary combining the methods and method names. Write it out fully.
method_dict = {'Random Forests': RandomForestClassifier(),
               # 'Neural Networks': MLPClassifier(),
               # 'Logistic Regression': LogisticRegression(),
               #'K-Nearest Neighbors': KNeighborsClassifier(),
               #'Support Vector Machines': SVC(),
               'Decision Trees': DecisionTreeClassifier(),
               #'Gradient Boosting': GradientBoostingClassifier(),
               #'AdaBoost': AdaBoostClassifier()
             }

def get_accuracies(method_dict, X_train, y_train, X_val, y_val):
    # Create a dictionary to store the method accuracies
    method_accuracies = {}

    # Loop through the methods and print the accuracy
    for method_name, method in method_dict.items():
        method.fit(X_train, y_train)
        y_pred = method.predict(X_val)

        # Calculate total and balanced accuracy
        accuracy = accuracy_score(y_val, y_pred)
        balanced_accuracy = balanced_accuracy_score(y_val, y_pred)

        # Calculate the accuracies for each of the 3 categories using a from confusion_matrix
        cm = confusion_matrix(y_val, y_pred)
        category_accuracy = cm.diagonal() / cm.sum(axis=1)


        accuracy_list = [accuracy, balanced_accuracy]  + list(category_accuracy)
        method_accuracies[method_name] = accuracy_list

    # Create a dataframe from the dictionary
    return pd.DataFrame.from_dict(method_accuracies, orient='index', columns=['Total accuracy', 'Balanced accuracy'] + [f"{mode_dict[i]} accuracy" for i in range(1, 8)])
#%%
# Create a dataframe from the dictionary
df_accuracies = get_accuracies(method_dict=method_dict, X_train=X_train, y_train=y_train, X_val=X_val, y_val=y_val)
df_accuracies.sort_values("Total accuracy", ascending=False)
#%%
# Gradient boosting
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
model_GB = DecisionTreeClassifier()
model_GB.fit(X_train, y_train)
# make predictions for validation data
y_pred = model_GB.predict(X_val)
predictions = [round(value) for value in y_pred]
# evaluate predictions
accuracy = accuracy_score(y_val, predictions)
print("Accuracy: %.6f%%" % (accuracy * 100.0))

# Kfold
kfold = StratifiedKFold(n_splits=10, random_state=7, shuffle=True)
results = cross_val_score(model_GB, X, y, cv=kfold)
print("Accuracy: %.6f%% (%.6f%%)" % (results.mean()*100, results.std()*100))

# Feature importance
from matplotlib import pyplot
pyplot.bar(range(len(model_GB.feature_importances_)),
model_GB.feature_importances_)

from sklearn import metrics
from sklearn import model_selection
from sklearn.model_selection import cross_val_predict

predicted = model_selection.cross_val_predict(model_GB, X, y, cv=kfold)
print(metrics.accuracy_score(y, predicted))
print(metrics.classification_report(y, predicted))
#%%
# Gradient boosting top 20 important features
first_importances = pd.Series(model_GB.feature_importances_, index = X.columns)
sorted_first = first_importances.sort_values(ascending = False)
top_20_first = sorted_first.head(50)
first_list = top_20_first.index.tolist()
#%%
print(first_list)
#%%
# Create a list of the labels of the top 20 features
feature_labels = {var: codebook_dict[var] for var in first_list}
feature_labels
#%% md
# ### Targeted data extraction
# Data needed:
# - Needs (for what purposes do people travel?)
# - Habituality (how often do they use the same mode of transport?)
# - Destinations (where do they travel to?)
# - Value of time (how much time are they willing to spend on travel?)
# - Weather sensitivity (how sensitive are they to weather conditions?)