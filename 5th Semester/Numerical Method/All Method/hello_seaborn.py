import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
print("Setup Complete")

fifa_data = pd.read_csv(r"D:\Languages\Python-Library\All Method\cancer.csv")

# Print the first 5 rows of the data
print(fifa_data.head())

#set the width and height of the figure
plt.figure(figsize=(16,6))

#Line chart showing how FIFA ranking evolved over time
sns.lineplot(data=fifa_data)
plt.show()
