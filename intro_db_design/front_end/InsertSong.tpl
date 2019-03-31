<HTML><HEAD><meta http-equiv="Content-Type" content="text/html   charset=utf-8" />
</HEAD>
<BODY>
<form METHOD="POST" ACTION="/Insert_Song_Info">
<h2>Insert Song</h2>
<TABLE cellpadding="0" cellspacing="2" border="0" width="500">
<TR><TD>Title:</TD><TD><input type="text" name="titlos" required></TD></TR>
<TR><TD>Production Year:</TD><TD><input type="date" name="etos_par" required></TD></TR>
<TR><TD>CD:<TD><select name="CD" required>
%for i in fieldsCD:
<option value = {{i[0]}}>{{i[0]}}</option>
%end
</TD></TD></TR>
<TR><TD>Singer:<TD><select name="Singer" required>
%for i in fieldsSINGER:
<option value = {{i[0]}}>{{i[0]}}</option>
%end
</TD></TD></TR>
<TR><TD>Composer:<TD><select name="Composer" required>
%for i in fieldsCOMPOSER:
<option value = {{i[0]}}>{{i[0]}}</option>
%end
</TD></TD></TR>
<TR><TD>SongWriter:<TD><select name="SongWriter" required>
%for i in fieldsSONGWRITER:
<option value = {{i[0]}}>{{i[0]}}</option>
%end
</TD></TD></TR>
<TR><TD><TD><input type="submit" value="Update Information" ></TD></TD></TR>
</form>
</body>
</html>
