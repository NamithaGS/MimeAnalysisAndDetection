/*
 * Copyright 2016 The Apache Software Foundation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.tika.parser.image;
import java.io.IOException;
import java.io.InputStream;
import java.util.Collections;
import java.util.Set;
import org.apache.poi.util.IOUtils;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.mime.MediaType;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.AbstractParser;
import org.apache.tika.sax.XHTMLContentHandler;
import org.xml.sax.ContentHandler;
import org.xml.sax.SAXException;
/**
 *
 * @author Manisha Kampasi
 */

//Create a basic parser class to parse ICNS files
//TODO: Extract more metadata information from the ICNS files. Look for already available open source ICNS parsers.
public class ICNSParser extends AbstractParser {
    private static final long serialVersionUID = 261736541253892772L;
    private static final Set<MediaType> SUPPORTED_TYPES = Collections.singleton(MediaType.image("icns"));
        public static final String ICNS_MIME_TYPE = "image/icns";
        
        public Set<MediaType> getSupportedTypes(ParseContext context) {
                return SUPPORTED_TYPES;
        }

        public void parse(
                        InputStream stream, ContentHandler handler,
                        Metadata metadata, ParseContext context)
                        throws IOException, SAXException, TikaException {

             byte[] signature = new byte[4];
        IOUtils.readFully(stream, signature);
        if (signature[0] == (byte) 'i' && signature[1] == (byte) 'c' &&
                signature[2] == (byte) 'n' && signature[3] == (byte) 's') {
            // Signature found
        } else {
            throw new TikaException("ICNS magic signature invalid");
        }    
            metadata.set(Metadata.CONTENT_TYPE, ICNS_MIME_TYPE);
         

                XHTMLContentHandler xhtml = new XHTMLContentHandler(handler, metadata);
                xhtml.startDocument();
                xhtml.endDocument();
        }
}
