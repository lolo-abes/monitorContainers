from collections import defaultdict
import json
import csv
import re
jsonFilePath= "./"

with open(jsonFilePath + "data.json") as fp:
  jsonFile = json.load(fp)

containers=[]
headers=['date']
mem_usage=[]
times=[]
datasetObj= {}
for i in jsonFile:
    # if 'GiB' in i['MemUsage'].split("/")[0].strip():
    #     mem_usage_mib = str(float(i['MemUsage'].split("GiB")[0].strip())*1024) + "MiB"
    #     mem_usage.append(mem_usage_mib)
    # else:
    #     mem_usage_mib = i['MemUsage'].split("/")[0].strip()
    #     mem_usage.append(mem_usage_mib)
    # print(i['Name'] + " " + i['CPUPerc'] + " " + mem_usage_mib + " " + i['time'])
    if i['Name'] not in containers:
        containers.append(i['Name'])
        headers.append(i['Name'])
    if i['time'] not in times:
        times.append(i['time'])
for time in times:
    datasetObj.update({time: []})

for time in times:
    for container in containers:
        print(f"Name: {container}")
        for obj in jsonFile:
            if obj['Name'] == container and obj['time'] == time:
                blockio_input = obj['BlockIO'].split("/")[0].strip()
                blockio_output = obj['BlockIO'].split("/")[1].strip()
                netio_input = obj['NetIO'].split("/")[0].strip()
                netio_output = obj['NetIO'].split("/")[1].strip()
                if 'GiB' in obj['MemUsage'].split("/")[0].strip():
                    mem_usage_mib = float(obj['MemUsage'].split("GiB")[0].strip())*1024
                    mem_usage.append(mem_usage_mib)
                else:
                    mem_usage_mib = obj['MemUsage'].split("/")[0].split("MiB")[0].strip()
                    mem_usage.append(mem_usage_mib)
                if re.search(blockio_input, "\\d+B") or blockio_input == "0B":
                    blockio_input = float(blockio_input.split("B")[0]) / 1000 / 1000
                elif 'kB' in  blockio_input:
                    blockio_input = float(blockio_input.split("kB")[0]) / 1000
                elif 'GB' in blockio_input:
                    blockio_input = float(blockio_input.split("GB")[0]) * 1000
                else:
                    blockio_input = blockio_input.split("MB")[0]
                if re.search(blockio_output, "\\d+B") or blockio_output == "0B":
                    blockio_output = float(blockio_output.split("B")[0]) / 1000 / 1000
                elif 'kB' in blockio_output:
                    blockio_output = float(blockio_output.split("kB")[0]) / 1000
                elif 'GB' in blockio_output:
                    blockio_output = float(blockio_output.split("GB")[0]) * 1000
                else:
                    blockio_output = blockio_output.split("MB")[0]
                if re.search(netio_input, "\\d+B"):
                    netio_input = float(netio_input.split("B")[0]) / 1000 / 1000 / 1000
                elif 'kB' in netio_input:
                    netio_input = float(netio_input.split("kB")[0]) / 1000 / 1000
                elif 'MB' in netio_input:
                    netio_input = float(netio_input.split("MB")[0]) / 1000
                elif 'GB' in netio_input:
                    netio_input = float(netio_input.split("GB")[0])
                if re.search(netio_output, "\\d+B"):
                    netio_output = float(netio_output.split("B")[0]) / 1000 / 1000 / 1000
                elif 'kB' in netio_output:
                    netio_output = float(netio_output.split("kB")[0]) / 1000 / 1000
                elif 'MB' in netio_output:
                    netio_output = float(netio_output.split("MB")[0]) / 1000
                elif 'GB' in netio_output:
                    netio_output = float(netio_output.split("GB")[0])
                print("--------------")
                print(f"{time}: - {obj['Name']} - {mem_usage_mib}")
                cpu_perc = obj['CPUPerc'].split("%")[0]
                returned_obj = { 'Name': obj['Name'], 'MemUsage' : mem_usage_mib, 'CPUConsumption' : cpu_perc, 'BlockIO_input' : blockio_input, 'BlockIO_output' : blockio_output, 'NetIO_input': netio_input, 'NetIO_output': netio_output }
                datasetObj[time].append(returned_obj)
                # if not obj['time'] in datasetObj:
    # for dataByContainer in jsonFile['Name'][container]:
    #     print(dataByContainer['Name'])

# print(mem_usage)
print("--------------")
# print(times)
print(json.dumps(datasetObj, indent=4, sort_keys=True))

# for time in times:
#     for container in containers:
#         if time in 
#         print(f"time: {times},container : {container}")

with open('mem_bench.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    dataset = []
    row = []
    for data in datasetObj:
        row = [data]
        print(f"{data} - {datasetObj[data][0]}")
        for item in datasetObj[data]:
            print(item)
            for key, value in item.items():
                print(f"{key} -- {value}")
                if key == "MemUsage":
                    row.append(value)
        dataset.append(row)
        print(f"la row : {row}")
    print(dataset)
    writer.writerows(dataset) 
    # write multiple row

with open('cpu_bench.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    dataset = []
    row = []
    for data in datasetObj:
        row = [data]
        print(f"{data} - {datasetObj[data][0]}")
        for item in datasetObj[data]:
            print(item)
            for key, value in item.items():
                print(f"{key} -- {value}")
                if key == "CPUConsumption":
                    row.append(value)
        dataset.append(row)
        print(f"la row : {row}")
    print(dataset)
    writer.writerows(dataset) 


with open('blockio_input_bench.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    dataset = []
    row = []
    for data in datasetObj:
        row = [data]
        print(f"{data} - {datasetObj[data][0]}")
        for item in datasetObj[data]:
            print(item)
            for key, value in item.items():
                print(f"{key} -- {value}")
                if key == "BlockIO_input":
                    row.append(value)
        dataset.append(row)
        print(f"la row : {row}")
    print(dataset)
    writer.writerows(dataset) 

with open('blockio_output_bench.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    dataset = []
    row = []
    for data in datasetObj:
        row = [data]
        print(f"{data} - {datasetObj[data][0]}")
        for item in datasetObj[data]:
            print(item)
            for key, value in item.items():
                print(f"{key} -- {value}")
                if key == "BlockIO_output":
                    row.append(value)
        dataset.append(row)
        print(f"la row : {row}")
    print(dataset)
    writer.writerows(dataset) 

with open('netio_input_bench.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    dataset = []
    row = []
    for data in datasetObj:
        row = [data]
        print(f"{data} - {datasetObj[data][0]}")
        for item in datasetObj[data]:
            print(item)
            for key, value in item.items():
                print(f"{key} -- {value}")
                if key == "NetIO_input":
                    row.append(value)
        dataset.append(row)
        print(f"la row : {row}")
    print(dataset)
    writer.writerows(dataset) 

with open('netio_output_bench.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    dataset = []
    row = []
    for data in datasetObj:
        row = [data]
        print(f"{data} - {datasetObj[data][0]}")
        for item in datasetObj[data]:
            print(item)
            for key, value in item.items():
                print(f"{key} -- {value}")
                if key == "NetIO_output":
                    row.append(value)
        dataset.append(row)
        print(f"la row : {row}")
    print(dataset)
    writer.writerows(dataset) 
