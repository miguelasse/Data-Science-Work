if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("data/CRDC2013_14.csv", encoding="Latin-1")
    juvenile_yes = data["JJ"] == "YES"
    magnet_yes = data["SCH_STATUS_MAGNET"] == "YES"
    
    juvenile_counts = data[juvenile_yes]["JJ"].value_counts
    magnet_counts = data[magnet_yes]["SCH_STATUS_MAGNET"].value_counts

   # print(juvenile_counts)
   # print(magnet_counts)
    jj_pivot =  pd.pivot_table(data, values=["TOT_ENR_M", "TOT_ENR_F"], index="JJ", aggfunc="sum")

    magnet_pivot = pd.pivot_table(data, values=["TOT_ENR_M", "TOT_ENR_F"], index="SCH_STATUS_MAGNET", aggfunc="sum")


    print(jj_pivot)
    print(magnet_pivot)
