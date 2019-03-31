import pymysql as db
import my_settings
import sys
import bottle
from bottle import request ,template

def connection():

    con = db.connect(my_settings.mysql_host,
    	my_settings.mysql_user,
		my_settings.mysql_passwd,
		my_settings.mysql_schema,
        use_unicode = True,
        charset = "utf8")
    return con

def renderArtists(tuples):
    printResult = """<style type='text/css'> h1 {color:red;} h2 {color:blue;} p {color:green;} </style>
    <table border = '1' frame = 'above'>"""
    header = '<h3>View Artists Results</h3>'
    printResult += header
    data='<tr>'+'</tr><tr>'.join(['<td>'+'</td><td>'.join([str(y) for y in row])+
    '</td><td><form METHOD="POST" ACTION="/UpdateArtistInformation"><input name="dataZ" type="hidden" value="'
    + row[0]+"?"+row[1]+"?"+row[2]+"?"+str(row[3])+"?" +'" /><input type="submit" value="Edit Me!"></form></td>' for row in tuples[0:]])+'</tr>'
    printResult += data+"</table>"
    return printResult

def renderSongs(tuples):
    printResult = """<style type='text/css'> h1 {color:red;} h2 {color:blue;} p {color:green;} </style>
    <table border = '1' frame = 'above'>"""
    header = '<h3>View Songs Results</h3>'
    data='<tr>'+'</tr><tr>'.join(['<td>'+'</td><td>'.join([str(y) for y in row])+'</td>' for row in tuples[0:]])+'</tr>'
    printResult += header+data+"</table>"
    return printResult

def presentation_of_artists():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = request.POST['onoma']
    surname = request.POST['epitheto']
    date_birth_from = request.POST['etos_gen_from']
    date_birth_to = request.POST['etos_gen_to']

    if len(date_birth_from) == 0:
        date_birth_from = '0';

    if len(date_birth_to) == 0:
        date_birth_to = 'YEAR(CURDATE())'

    con = connection()
    it = con.cursor()
    query = " SELECT * FROM songsdump.kalitexnis WHERE onoma LIKE IF('" + name + "' = '', '%', '" + name + "%') "
    query += " AND epitheto LIKE IF('" + surname + "' = '', '%', '" + surname + "%') "
    query += " AND etos_gen BETWEEN " + date_birth_from + " AND " + date_birth_to + ";"

    it.execute(query)
    fields = it.fetchall()
    it.close()
    con.close()
    return "<html><body>" + renderArtists(fields) + "</body></html>"

def view_artist_results():
    dataZ = request.POST['dataZ']
    html = "<form METHOD=\"POST\" ACTION=\"/Update_info\">"
    html += "<h3>Update Artist Information</h3>"
    html += "<TABLE cellpadding=\"0\" cellspacing=\"2\" border=\"0\" width=\"500\">"
    html += "<TR><TD>Name:</TD><TD><input type=\"text\" name=\"onoma\" value=" + dataZ.split('?', 2)[1] + "></TD></TR>"
    html += "<TR><TD>Surname:</TD><TD><input type=\"text\" name=\"epitheto\" value=" + dataZ.split('?', 3)[2] + "></TD></TR>"
    html += "<TR><TD>Birth Year:</TD><TD><input type=\"date\" name=\"etos_gen\" value=" + dataZ.split('?', 4)[3] + "></TD></TR>"
    html += "<TR><TD><input type=\"hidden\" name=\"ar_taut\" value=" + dataZ.split('?', 1)[0] + "></TD></TR>"
    html += "<TR><TD><TD><input type=\"submit\" value=\"Update Information\"></TD></TD></TR>"
    html += "</form>"
    return "<html><body>" + html + "</body></html>"

def update_artist_information():
    con = connection()
    it = con.cursor()
    query = "UPDATE songsdump.kalitexnis SET onoma = '" + request.POST['onoma'] + "',"
    query += " epitheto = '" + request.POST['epitheto'] + "',"
    query += " etos_gen = " + request.POST['etos_gen'] + " WHERE ar_taut = '" + request.POST['ar_taut'] + "';"
    it.execute(query)
    it.close()
    con.commit()
    con.close()
    return "<html><body>Update Successful<BR><TD><TD><form METHOD=\"POST\" ACTION=\"/\"><input type = \"submit\" value=\"Return to Main\"></TD></TD></body></html>"

def presentation_of_songs():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    song_title = request.POST['titlos']
    production_year = request.POST['etos_par']
    company = request.POST['etaireia']


    con = connection()
    it = con.cursor()

    query = " SELECT DISTINCT T.titlos , T.etos_par, CDP.etaireia "
    query += " FROM songsdump.cd_production as CDP, songsdump.tragoudi as T,"
    query += " songsdump.singer_prod as SP, songsdump.group_prod as GP "
    query += " WHERE (T.titlos LIKE IF('" + song_title + "' = '', '%', '" + song_title + "%')"
    query += " AND CDP.etaireia LIKE IF('" + company + "' = '', '%', '" + company + "%') "
    query += " AND T.etos_par LIKE IF('" + production_year + "' = '', '%', '" + production_year + "') "
    query += " AND T.titlos = SP.title AND SP.cd = CDP.code_cd ) OR "
    query += " (T.titlos LIKE IF('" + song_title + "' = '', '%', '" + song_title + "%')"
    query += " AND CDP.etaireia LIKE IF('" + company + "' = '', '%', '" + company + "%') "
    query += " AND T.etos_par LIKE IF('" + production_year + "' = '', '%', '" + production_year + "') "
    query += " AND T.titlos = GP.title AND GP.cd = CDP.code_cd ) ;"


    it.execute(query)
    fields = it.fetchall()
    it.close()
    con.close()

    success = "Search Successful<BR><TD><TD><form METHOD=\"POST\" ACTION=\"/\"><input type = \"submit\" value=\"Return to Main\"></TD></TD>"
    return "<html><body>" + renderSongs(fields) + success +"</body></html>"

def insert_artist_information():
    con = connection()
    it = con.cursor()
    query = "INSERT INTO songsdump.kalitexnis SET ar_taut = '" + request.POST['ar_taut'] + "',"
    query += " onoma = '" + request.POST['onoma'] + "',"
    query += " epitheto = '" + request.POST['epitheto'] + "',"
    query += " etos_gen = " + request.POST['etos_gen'] + ";"
    it.execute(query)
    it.close()
    con.commit()
    con.close()
    return "<html><body>Insert Successful<BR><TD><TD><form METHOD=\"POST\" ACTION=\"/\"><input type = \"submit\" value=\"Return to Main\"></TD></TD></body></html>"

def insert_song_preview():
    con = connection()
    it = con.cursor()
    queryCD = "SELECT code_cd FROM songsdump.cd_production;"
    it.execute(queryCD)
    fieldsCD = it.fetchall()
    querySINGER = "SELECT DISTINCT ar_taut FROM songsdump.kalitexnis, songsdump.singer_prod WHERE ar_taut = tragoudistis"
    it.execute(querySINGER)
    fieldsSINGER = it.fetchall()
    queryCOMPOSER = "SELECT DISTINCT ar_taut FROM songsdump.kalitexnis, songsdump.tragoudi WHERE ar_taut = sinthetis;"
    it.execute(queryCOMPOSER)
    fieldsCOMPOSER = it.fetchall()
    querySONGWRITER = "SELECT DISTINCT ar_taut FROM songsdump.kalitexnis, songsdump.tragoudi WHERE ar_taut = stixourgos;"
    it.execute(querySONGWRITER)
    fieldsSONGWRITER = it.fetchall()
    it.close()
    con.close()
    return bottle.template("InsertSong.tpl",fieldsCD = fieldsCD, fieldsSINGER = fieldsSINGER, fieldsCOMPOSER = fieldsCOMPOSER, fieldsSONGWRITER = fieldsSONGWRITER)

def insert_song_information():
    con = connection()
    it = con.cursor()
    query = "INSERT INTO songsdump.tragoudi SET tragoudi.titlos = '" + request.POST['titlos'] + "',"
    query += " tragoudi.etos_par = " + request.POST['etos_par'] + ","
    query += " tragoudi.sinthetis = '" + request.POST['Composer'] + "',"
    query += " tragoudi.stixourgos = '" + request.POST['SongWriter'] + "';"
    query2 = "INSERT INTO songsdump.singer_prod SET "
    query2 += " singer_prod.title = '" + request.POST['titlos'] + "',"
    query2 += " singer_prod.tragoudistis = '" + request.POST['Singer'] + "',"
    query2 += " singer_prod.cd = '" + request.POST['CD'] + "';"
    it.execute(query)
    it.execute(query2)
    it.close()
    con.commit()
    con.close()
    return "<html><body>Insert Successful<BR><TD><TD><form METHOD=\"POST\" ACTION=\"/\"><input type = \"submit\" value=\"Return to Main\"></TD></TD></body></html>"
