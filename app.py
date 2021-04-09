from flask import abort, Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import yaml
import time as currentTime
import os
from mutagen.mp3 import MP3
import json
from flask import send_file
import zipfile
from dto.api_dto import api_dto


app = Flask(__name__)
currentDir = os.path.dirname(__file__)
config_path = os.path.join(currentDir, './configs/config.yaml')
config = yaml.load(open(config_path))
db = config['db_config']
app.config['MYSQL_HOST'] = db['host']
app.config['MYSQL_USER'] = db['user']
app.config['MYSQL_PASSWORD'] = db['pass']
app.config['MYSQL_DB'] = db['db']

mysql = MySQL(app)
CORS(app)

#Gets the duration of the uploaded mp3 file
def getDuration(music_file,fileType, name):
    audio = MP3(config['audio_file_path'] % (fileType, name))
    print("Length of the Audio is: ", audio.info.length)
    return float(audio.info.length)

#Saves the uploaded mp3 in defined dir
def saveFile(save_file, fileType):
    savefile = os.path.join(config['audio_file_path'] % (fileType, name))
    music_file.save(savefile)

#Makes zip file having all file in the fileType dir for download
def makeZip(fileType):
    zipfolder = zipfile.ZipFile('Audiofiles.zip','w', compression = zipfile.ZIP_STORED)
    for root,dirs, files in os.walk(config['audio_file_dir'] % (fileType)):
        for file in files:
            zipfolder.write('%s/'% (fileType)+file)
    zipfolder.close()

#To select and download a particular file
def downloadFile(fileType, name):
    path = os.path.join(config['audio_file_path'] % (fileType, name))
    return send_file(path, as_attachment=True)

#To delect a particular file
def deleteFile(fileType ,name):
    os.remove(config['audio_file_path'] % (fileType, name))

#To check the length of the participents. Not added
def checkParticipents(participentsOrNarrator):
    print(participentsOrNarrator)
    print("p",len(str(participentsOrNarrator)))
    if len(participentsOrNarrator)<100:
        for i in range(len(participentsOrNarrator)):
            print(i)
            if len(participentsOrNarrator[i])<100:
                print("Valid")
                
            else:
                print ("Participents name and size not valid")
                break
                return ("Participents name and size not valid")
    return True

@app.route('/')
def index():
    return "Lots of Hellos"



#To POST/CREATE the data and GET allData from DB
@app.route('/data', methods=['POST', 'GET'])
def data():
    
    # Handling POST
    
    if request.method == 'POST':
        
        body = request.form
        name = body['name']
        fileType = body['fileType']
        hostOrAuthor = body['hostOrAuthor']
        participentsOrNarrator = body['participentsOrNarrator']
        timestamp = currentTime.strftime('%Y-%m-%d %H:%M:%S')
        music_file = request.files['music_file']

        #See if file_name is unique. It not, throw Error res. 
        if os.path.isfile(config['audio_file_path']% (fileType, name)):
            out_dict = {
                    'Comments': 'File Already Present'
                    }
            output = api_dto(out_dict)
            return jsonify(output.clientError()), 400

        #If the fileType is song, perform name lenghth verification and execute
        if fileType == 'song' and len(name)<10:
            try: 
                savefile = os.path.join(config['audio_file_path'] % (fileType, name))
                music_file.save(savefile)
                duration = getDuration(music_file,fileType, name)
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO audio VALUES (null, %s, %s, %s, %s, null, null)', (str(name), str(fileType), str(duration), str(timestamp)))
                mysql.connection.commit()
                cursor.close()
                out_dict ={
                'status': 'success 200',
                'Name of the song': name,
                'fileType': fileType,
                'Duration': duration,
                "Time_Uploaded": timestamp
                }
            except:
                out_dict = {
                'Comments': 'Invalid data entered'
                }
                output = api_dto(out_dict)
                return jsonify(output.clientError()), 400
            else:
                output = api_dto(out_dict)
                return jsonify(output.success()), 200


        #If the fileType is podcast, perform name, host, participents length verification and execute
        elif fileType == 'podcast' and len(name)<10 and 0<len(hostOrAuthor)<10 and 0<len(participentsOrNarrator)<10:            
            
            try:
                savefile = os.path.join(config['audio_file_path'] % (fileType, name))
                music_file.save(savefile)
                duration = getDuration(music_file,fileType, name)
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO audio VALUES (null, %s, %s, %s, %s, %s, %s)', (str(name), str(fileType), str(duration), str(timestamp), str(hostOrAuthor), str(participentsOrNarrator)))
                mysql.connection.commit()
                cursor.close()
                out_dict = {
                
                'Name of the podcast': name,
                'fileType': fileType,
                'Duration': duration,
                'Host': hostOrAuthor,
                'Participents': participentsOrNarrator,
                "Time_Uploaded": timestamp
            }
            except: 
                out_dict = {
                'Comments': 'Invalid data entered'
                }
                output = api_dto(out_dict)
                return jsonify(output.clientError()), 400
            else:
                output = api_dto(out_dict)
                return jsonify(output.success()), 200


        #If the fileType is audiobook, perform name, author, narrator length verification and execute
        elif fileType == 'audiobook' and len(name)<10 and 0<len(hostOrAuthor)<10 and 0<len(participentsOrNarrator)<10:
            
            try:
                savefile = os.path.join(config['audio_file_path'] % (fileType, name))
                music_file.save(savefile)
                duration = getDuration(music_file,fileType, name)
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO audio VALUES (null, %s, %s, %s, %s, %s, %s)', (str(name), str(fileType), str(duration), str(timestamp), str(hostOrAuthor), str(participentsOrNarrator)))
                mysql.connection.commit()
                cursor.close()
                out_dict = {
                'Name of the audiobook': name,
                'FileType': fileType,
                'Duration': duration,
                'Author': hostOrAuthor,
                'Narrator': participentsOrNarrator,
                'Time_Uploaded': timestamp
                }
            except:
                out_dict = {
                'Comments': 'Invalid data entered'
                }
                output = api_dto(out_dict)
                return jsonify(output.clientError()), 400
            else:
                output = api_dto(out_dict)
                return jsonify(output.success()), 200
        else:
            out_dict = {
                'Comments': 'Invalid data entered. Make sure fileType is mp3 and text lengths are <100 char'
            }
            output = api_dto(out_dict)
            return jsonify(output.clientError()), 400
    
    # Handling GET 
    elif request.method == 'GET' :
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM audio')
            audio = cursor.fetchall()
            allData = []
            #GET all entry from DB
            #Performing For loop and appending to allData with appropriate key:value pair based on fileType
            for i in range(len(audio)):
                id = audio[i][0]
                name = audio[i][1]
                fileType = audio[i][2]
                duration = audio[i][3]
                time = audio[i][4]
                hostOrAuthor = audio[i][5]
                participantsOrNarrator = audio[i][6]
                if fileType == 'song':
                    out_dict = {
                        'id': id,
                        'name': name,
                        'File_Type': fileType,
                        'Duration': duration,
                        'Last_Uploaded_At': time,
                    }
                elif fileType == 'podcast':
                    out_dict = {
                        'id': id,
                        'name': name,
                        'File_Type': fileType,
                        'Duration': duration,
                        'Last_Uploaded_At': time,
                        'Host': hostOrAuthor,
                        'Participants': participantsOrNarrator
                    }
                elif fileType == 'audiobook':
                    out_dict = {
                        'id': id,
                        'name': name,
                        'File_Type': fileType,
                        'Duration': duration,
                        'Last_Uploaded_At': time,
                        'Author': hostOrAuthor,
                        'Narrator': participantsOrNarrator
                    }
                
                allData.append(out_dict)
        except:
            return "Internal error in getting data from DB"
        else:
            output = api_dto(allData)
            return jsonify(output.success()), 200

    else:
        out_dict = {
            'Comments': 'Invalid data entered. Make sure fileType is mp3 and text lengths are <100 char'
        }
        output = api_dto(out_dict)
        return jsonify(output.success()), 400


#To make changes to a specific entry
@app.route('/data/info/<string:fileType>/<string:name>', methods=['GET', 'DELETE', 'PUT'])
def onedata(fileType, name):

    # GET a specific data based on name
    if request.method == 'GET':
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM audio WHERE name = ("%s") and fileType = ("%s")' % (name, fileType))
            audio = cursor.fetchall()
            print(audio)
            data = []
            for i in range(len(audio)):
                id = audio[i][0]
                name = audio[i][1]
                fileType = audio[i][2]
                duration = audio[i][3]
                time = audio[i][4]
                hostOrAuthor = audio[i][5]
                participantsOrNarrator = audio[i][6]
                if fileType == 'song':
                    out_dict = {
                        'id': id,
                        'name': name,
                        'File_Type': fileType,
                        'Duration': duration,
                        'Last_Uploaded_At': time,
                    }
                                       
                elif fileType == 'podcast':
                    out_dict = {
                        'id': id,
                        'name': name,
                        'File_Type': fileType,
                        'Duration': duration,
                        'Last_Uploaded_At': time,
                        'Host': hostOrAuthor,
                        'Participants': participantsOrNarrator
                    }
                    
                elif fileType == 'audiobook':
                    out_dict = {
                        'id': id,
                        'name': name,
                        'File_Type': fileType,
                        'Duration': duration,
                        'Last_Uploaded_At': time,
                        'Author': hostOrAuthor,
                        'Narrator': participantsOrNarrator
                    }                    
                data.append(out_dict)

            if len(data) == 0:
                raise Exception("Not found in DB")

        except:
            out_dict = {
            'Comments': 'Invalid data entered'
            }
            output = api_dto(out_dict)
            return jsonify(output.clientError()), 400
        else:
            output = api_dto(data)
            return jsonify(output.success()), 200
        
    # DELETE a data from DB and music_file from storage based on music name
    if request.method == 'DELETE':
        try:
            deleteFile(fileType, name)
        except:
            out_dict = {
            'Comments': 'Invalid data entered. Make sure fileType is mp3 and text lengths are <100 char'
            }
            output = api_dto(out_dict)
            return jsonify(output.clientError()), 400
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('DELETE FROM audio WHERE name = "%s"' %(name))
            mysql.connection.commit()
            cursor.close()
            return jsonify({'status': 'Data '+name+' is deleted on MySQL!'})

    # UPDATE a data in DB based on music name
    if request.method == 'PUT':
        body = request.form
        new_name = body['name']
        new_fileType = body['fileType']
        # duration = body['duration']
        hostOrAuthor = body['hostOrAuthor']
        participentsOrNarrator = body['participentsOrNarrator']
        timestamp = currentTime.strftime('%Y-%m-%d %H:%M:%S')

        try:
            if fileType == 'song':
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE audio SET name = %s, fileType = %s, time = %s  WHERE name = %s and fileType = %s', (new_name, new_fileType, timestamp, name, fileType))
                mysql.connection.commit()
                cursor.close()
            else:
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE audio SET name = %s, fileType = %s, time = %s, hostOrAuthor =%s, participantsOrNarrator = %s  WHERE name = %s and fileType = %s', (new_name, new_fileType, timestamp, hostOrAuthor, participentsOrNarrator, name, fileType))
                mysql.connection.commit()
                cursor.close()
        except:
            return "Internal Error. Make sure you entered the right file name"
        else:
            out_dict = {
                "Comments": 'status: '+name +' name is updated on MySQL!'
            }
            output = api_dto(out_dict)
            return jsonify(output.success()), 200


#To download a specific music file
@app.route('/data/<string:fileType>/<string:name>', methods=['GET'])
def getfile(fileType, name):

    # GET a specific music file based on music name
    if request.method == 'GET':
        try:
            downloadFile(fileType, name)
            derivedFile = downloadFile(fileType, name)
        except:
            return "Internal Error in getting the file from Storage"
        else:       
            return (derivedFile)


# To Download all music of same fileType
@app.route('/data/<string:fileType>', methods=['GET'])
def downloadAllFiles(fileType):
    try:
        makeZip(fileType)
    except:
        return "Error making Zip File"
    else:
        return send_file('Audiofiles.zip',
                mimetype = 'zip',
                attachment_filename= 'Audiofiles.zip',
                as_attachment = True)

        # Delete the zip file if not needed
        os.remove("Audiofiles.zip")



#To initialize the required paths for storages
def initializePaths():
    try: 
        path = os.path.join(currentDir, 'song')
        os.mkdir(path)
    except:
        pass
    try: 
        path = os.path.join(currentDir, 'podcast')
        os.mkdir(path)
    except:
        pass
    try:
        path = os.path.join(currentDir, 'audiobook')
        os.mkdir(path)
    except:
        pass
    finally:
        print("Error creating dir. Already")

if __name__ == '__main__':
    initializePaths()
    app.run(debug = True)
