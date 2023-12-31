# %%
import numpy as np
import pandas as pd

edge_table = pd.read_csv(
    "cora.cites", sep="\t", header=None, names=["src", "trg"]
)  # .to_csv("cora.cites", sep=' ', header=None, index=False)

node_table = pd.read_csv(
    "cora.content", sep="\t", header=None
)  # .to_csv("cora.cites", sep=' ', header=None, index=False)
node_features = node_table.iloc[:, 1:-1].values

node_table = (
    node_table.iloc[:, np.array([0, -1])]
    .rename(columns={0: "node_id", 1434: "field"})
    .sort_values(by="node_id")
)

# %%
unode_ids, node_ids = np.unique(node_table["node_id"].values, return_inverse=True)
toNewIndex = dict(zip(unode_ids, node_ids))
edge_table["src"] = edge_table["src"].map(toNewIndex)
edge_table["trg"] = edge_table["trg"].map(toNewIndex)

node_table["node_id"] = node_ids

order = np.argsort(node_ids)
node_features = node_features[order, :]
node_feature_table = pd.DataFrame(
    node_features, columns=[f"feat_{i}" for i in range(node_features.shape[1])]
)
node_feature_table["node_id"] = np.arange(len(node_ids))

# %%
node_table.to_csv("node_table.csv", index=False)
node_feature_table.to_csv("node_features.csv", index=False)
edge_table.to_csv("edge_table.csv", index=False)
