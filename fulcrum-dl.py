import urllib2
import json
import os
import csv
import sys

# Set api acess token
api_key = open('api_key.txt', 'r').readline()

# Set api url
url_base = 'https://api.fulcrumapp.com/api/v2/'
append_token = '?token=' + api_key

def loadRecord(record_id):
    record_url = url_base + 'records/' + record_id + '.json' + append_token
    record_json_obj = urllib2.urlopen(record_url)
    print 'Loading record: ' + record_id
    record_json = json.load(record_json_obj)
    form_values = record_json['record']['form_values']
    return form_values

def dlPhoto(photo_url, local_path):
    print 'downloading: ' + local_path
    jpgfile = urllib2.urlopen(photo_url)
    output = open(local_path,'wb')
    output.write(jpgfile.read())
    output.close()

def detPhotoKey(d):
    if '309d' in d:
        return '309d'
    elif 'a298' in d:
        return 'a298'
    else:
        return False

def fetchPhotos(form_values, photo_key, single_record):
    if photo_key:
        for photo in form_values[photo_key]:
            photo_filename = photo['photo_id'] + '.jpg'
            photo_url = url_base + 'photos/' + photo_filename + append_token
            photo_directory = single_record[0] + '/' + single_record[1][8:] + '/'
            safemkdir(photo_directory)
            photo_path = photo_directory + photo_filename
            dlPhoto(photo_url, photo_path)
    else:
        print 'no photos for record ' + single_record[1][8:]
        report = open("no_photo.txt", 'w')
        report.write(single_record[1][8:] + "\n")
        report.close()

def dlRecordphotos(single_record):
    record_form_values = loadRecord(single_record[2])
    photo_key = detPhotoKey(record_form_values)
    fetchPhotos(record_form_values, photo_key, single_record)

def safemkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Open records list file
ids_tsv = open(sys.argv[1], 'rb') # Import csv from first argument

try:
    record_list = csv.reader(ids_tsv, dialect='excel', delimiter='\t')
    for single_record in record_list:
        safemkdir(single_record[0])
        dlRecordphotos(single_record)
finally:
    ids_tsv.close()
