from package.statistics import to_json_file, RunData
s = "finished n=3, d=2, k=2: 6.0\nfinished n=3, d=3, k=2: 15.3\nfinished n=3, d=4, k=2: 42.9\nfinished n=3, d=5, k=2: 121.0\nfinished n=3, d=6, k=2: 326.6\nfinished n=3, d=7, k=2: 967.3\nfinished n=3, d=8, k=2: 2804.3"
# s = "finished n=3, d=2, k=2: 6.0\nfinished n=3, d=3, k=2: 15.3\nfinished n=3, d=4, k=2: 42.9\nfinished n=3, d=5, k=2: 121.0\nfinished n=3, d=6, k=2: 326.6\nfinished n=3, d=7, k=2: 967.3"
lines = s.split('\n')
Data: list[RunData] = []
list[RunData]
for line in lines:
    fields = line.split(': ')
    settings = fields[0].split('=')
    # print(settings)
    n = settings[1].split(',')[0]
    d = settings[2].split(',')[0]
    k = settings[3]
    
    # d = map(int, fields[0].split(',')[0].split('=')[1])
    # print(d)
    # data['n'], data['d'], data['k'] = map(int, fields[0].split(',')[0].split('=')[1])
    # print(data['n'], data['d'], data['k'])
    # data['avg_points'] = 
    # data['total_runs'] = 10
    # print(data)
    res: RunData = {"n": n, "d": d, "k": k, "avg_points": float(fields[1]), "total_runs": 10}
    Data.append(res)
    # print(res)
# print(Data)
to_json_file(file_path="Data", new_data=Data, alg="min_conflict")
