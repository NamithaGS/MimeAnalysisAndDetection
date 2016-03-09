The following steps were followed to add the new mime-types:

ICNS:
1. Updated the src/main/resources/org/apache/tika/mime/tika-mimetypes.xml with the following information:

   <mime-type type="image/icns">
        <_comment>Apple Icon Image Format</_comment>
             <magic priority="50">
      <match value="icns" type="string" offset="0">
     </match>
    </magic>
          <glob pattern="*.icns"/>
   </mime-type>
2. Added a basic parser for the ICNS files - ICNSParser.java under tika-parser/org/apache/tika/parser/image

3. Registered the parser by adding an entry in the list of parsers in the  tika-parsers/src/main/resources/META-INF/services/org.apache.tika.parser.Parser file.

--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
SFDU:

1. Updated the tika-mimetypes.xml with the following information:
   
      <mime-type type="application/x-sfdu">
        <_comment>Standard Formatted Data Units</_comment>
             <magic priority="50">
      <match value="Standard Formatted Data Units" type="string" offset="0:512">
     </match>
    </magic>
          <glob pattern="*.sfdu"/>
   </mime-type>


--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------   
For all the other remaining mime-types that were updated, new magic patterns were added under the corresponding mime tags in tika-mimetypes.xml.