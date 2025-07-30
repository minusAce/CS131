import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="dark")

df_cost = pd.read_csv("predictions/cost.csv")
df_util = pd.read_csv("predictions/util.csv")

# plot 1: stacked bar chart showing distribution of predictions
ct = pd.crosstab(df_cost["class"], df_cost["predicted_class"], normalize="index")
ct.plot(kind="bar", stacked=True, colormap="tab10")
plt.title("Predicted Class Distribution (Cost Features)")
plt.ylabel("Proportion")
plt.xlabel("True Class")
plt.legend(title="Predicted Evaluation", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig("plots/predicted_vs_actual_eval.png")
plt.clf()

# plot 2: violin plot showing how safety predicts eval class
sns.violinplot(x="safety", y="class", data=df_util, order=["low", "med", "high"])
plt.title("Acceptability by Safety Rating")
plt.xlabel("Safety")
plt.ylabel("Class")
plt.tight_layout()
plt.savefig("plots/safety_vs_eval.png")
plt.clf()
