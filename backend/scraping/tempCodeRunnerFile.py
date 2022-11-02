for i in range(len(list_of_times)):
#     if (datetime.strptime(current_time,'%H:%M').second - datetime.strptime(list_of_times[i],'%H:%M').second < 0):
#         continue
#     else:
        
#         url = "https://www.airports-worldwide.info/search/los angeles/arrivals/los angeles?time="+datetime.today().strftime('%Y-%m-%d')+"+"+list_of_times[i][:-3]+"%3A00"
#         print(url)
#         url = url.encode('ascii', errors='ignore')
#         url = url.decode('ascii', errors='ignore')
        
#         for dfs in list_of_dataframes:
#             print(dfs)
#             list_of_dataframes.append(pd.read_html(url.replace(" ","%20"), header=0))

# df = pd.concat(list_of_dataframes)
# print(df)
# # removes all flights that do not contain "scheduled" in "Status" column
# df = df[df["Status"].str.contains('scheduled', regex=False)]

# #remove flights with no flight number
# df = df.dropna(axis=0, subset=['Flight'])

# #remove unammed columns
# df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# #remove flight loop
# discard = ["Calgary"]
# df = df[df["Destination"].str.contains('|'.join(discard))==False]
# # print(df)