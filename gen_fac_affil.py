import csv
with open('csrankings.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    with open('industry.csv', mode='r') as infile2:
        reader2 = csv.DictReader(infile2)
        with open('faculty-affiliations.csv', 'w') as facultyaffs:
            facfieldnames = ['name', 'affiliation']
            facWriter = csv.DictWriter(facultyaffs, fieldnames=facfieldnames)
            facWriter.writeheader()
            for row in reader:
                f = { 'name' : row['name'].strip().rstrip(),
                        'affiliation' : row['affiliation'].strip().rstrip() }
                facWriter.writerow(f)
            for row in reader2:
                f = { 'name' : row['name'].strip().rstrip(),
                        'affiliation' : row['affiliation'].strip().rstrip() }
                facWriter.writerow(f)