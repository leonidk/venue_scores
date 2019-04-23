import csv
with open('csrankings.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
  
    with open('faculty-affiliations.csv', 'w') as facultyaffs:
        facfieldnames = ['name', 'affiliation']
        facWriter = csv.DictWriter(facultyaffs, fieldnames=facfieldnames)
        facWriter.writeheader()
        for row in reader:
            f = { 'name' : row['name'],
                    'affiliation' : row['affiliation'] }       
            facWriter.writerow(f)
