import urllib2
import json
import os
import csv
import sys

# Set api acess token
api_key = read(open('api_key', 'r'))

# Set api url
url_base = 'https://api.fulcrumapp.com/api/v2/'
append_token = '?token=' + api_key

def loadRecord(record_id):
    record_url = url_base + 'records/' + record_id + '.json' + append_token
    record_json_obj = urllib2.urlopen(record_url)
    print 'Loading record: ' + record_id
    return json.load(record_json_obj)

def dlPhoto(photo_url, local_path):
    print 'downloading: ' + local_path
    jpgfile = urllib2.urlopen(photo_url)
    output = open(local_path,'wb')
    output.write(jpgfile.read())
    output.close()

def detPhotoKey(d):
    if '309d' in d:
        return '309d'
    else:
        return 'a298'

def fetchPhotos(form_values, photo_key, record_row):
    for photo in form_values[photo_key]:
        photo_filename = photo['photo_id'] + '.jpg'
        photo_url = url_base + 'photos/' + photo_filename + append_token
        photo_directory = village + '/' + record_row[1][8:] + '/'
        if not os.path.exists(photo_directory):
            os.makedirs(photo_directory)
        photo_path = photo_directory + photo_filename
        dlPhoto(photo_url, photo_path)

def dlRecordphotos(record_row):
    record_data = loadRecord(record_row[2])
    form_values = record_data['record']['form_values']
    photo_key = detPhotoKey(form_values)
    fetchPhotos(form_values, photo_key, record_row)

ids_tsv = open(sys.argv[1], 'rb') # Import csv from first argument

try:
    reader = csv.reader(ids_tsv, dialect='excel', delimiter='\t')
    for record_row in reader:
        village = record_row[0]
        iom_id = record_row[1]
        fulcrum_id = record_row[2]
        if not os.path.exists(village):
            os.makedirs(village)
        dlRecordphotos(record_row)
finally:
    ids_tsv.close()
