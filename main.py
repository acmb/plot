import pandas as pd
import pymongo
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["api-performance-test"]
collection = db["localhost"]

pipe = [
  { '$match': { "input.c": 10 } },
  { '$addFields': {
    "n": "$input.n",
    "reqPerSecond": "$output.Requests per second.value",
    "non2xxRes": { "$ifNull": ["$output.Non-2xx responses.value", 0] }
  } },
  { '$project': { "_id": 0, "n": 1, "reqPerSecond": 1, "non2xxRes": 1 } }
]

data = list(collection.aggregate(pipe))

df_mongo = pd.DataFrame(data)

print(df_mongo)

df_mongo.plot(
  x="n",
  y=["reqPerSecond", "non2xxRes"],
  secondary_y="non2xxRes",
  xlabel="Amount of requests (n)",
  ylabel="Requests per second (#/s)",
  figsize=(20,10),
  title="c = 10",
  sharey=False
)

plt.show()
