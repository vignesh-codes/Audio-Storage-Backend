# Audio Storage Provider Site


Foobar is a Python library for dealing with word pluralization.

## Routes:

@app.route('/data', methods=['POST', 'GET'])
@app.route('/data/<string:fileType>/<string:name>', methods=['GET'])
@app.route('/data/<string:fileType>', methods=['GET'])
@app.route('/data/info/<string:fileType>/<string:name>', methods=['GET', 'DELETE', 'PUT'])

## Can perform the following:
- Create, upload and store an audio file entry in DB and local storage. File Type can be song, podcast, audiobook
- Get the duration of uploaded audio file and store in DB
- Get the list of audio file information entries from DB
- Get specific audio file information entry from DB
- Delete an audio file from local storage and delete entry from DB
- Download a specific audio file
- Download all audio files based on file type in ZIP Format
- Update the entry information from DB based on specific name and filetype
- All audio files are stored in a unique name. If a user enters a name already in the storage dir, it will throw an error and suggests to change name.
- Can only POST if data entered are valid as defined in the requirements.


## Generic body for POST = request.form

```
        name = body['name']
        fileType = body['fileType']
        hostOrAuthor = body['hostOrAuthor']
        participentsOrNarrator = body['participentsOrNarrator']
        timestamp = currentTime.strftime('%Y-%m-%d %H:%M:%S')
        music_file = request.files['music_file']

```

## DB Schema:

```
create table audio (
        id int auto_increment,
        name varchar(100) not null,
        fileType varchar(25) not null,
        duration float,
        time DATETIME,
        hostOrAuthor varchar(100),                 #Host for Podcast. Author for AudioBook
        participantsOrNarrator varchar(100)); #Participants for Podcast. Narrator for AudioBook

```
Maintain 3 response codes:
Success: 200, BadRequest: 400 and ServerError:500


##TO RUN:
pip3 install requirments.txt
python3 app.py
