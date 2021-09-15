import csv

# store data in csv
with open('metadata.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    metadata = ['name', 'min_lon', 'min_lat', 'max_lon', 'max_lat']
    writer.writerow(metadata)
