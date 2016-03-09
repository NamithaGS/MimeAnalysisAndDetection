/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.tika.detect;

import static org.junit.Assert.assertEquals;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;

import org.apache.tika.metadata.Metadata;
import org.apache.tika.mime.MediaType;
import org.apache.tika.mime.MimeDetectionTest;
import org.junit.Before;
import org.junit.Test;
import java.io.File;

public class MimeDetectionWithNNTest {

	private Detector detector;

	/** @inheritDoc */
	@Before
	public void setUp() {
 		detector = new NNExampleModelDetector();
	}

	/**
	 * The test case only works on the detector that only has grb model as
	 * currently the grb model is used as an example; if more models are added
	 * in the TrainedModelDetector, the following tests will need to modified to reflect
	 * the corresponding type instead of test-equal with the "OCTET_STREAM";
	 * 
	 * @throws Exception
	 */
	@Test
	public void testDetection() throws Exception {
		String octetStream_str = MediaType.OCTET_STREAM.toString();
		String img_str = "image/jpeg";
                File folder = new File( "C:/Users/Namithaa/Desktop/599/Project1/Prog/ExtraCredit9/imagetest/jpeg/"); // test on Correct files
                File[] listOfFiles = folder.listFiles();
                //testFile(img_str, "0005D8F00D68E1D57E7A47EDC3AC656437830EE155A1AD7F93AE2454E4839DE0");
                for (File file : listOfFiles) {
                testFile(img_str,  file.getName());
                }
                File folderjunk = new File( "C:/Users/Namithaa/Desktop/599/Project1/Prog/ExtraCredit9/imagetest/junk/"); // test on negative files
                File[] listOfjunkFiles = folderjunk.listFiles();
                
                for (File junkfile : listOfjunkFiles) {
                testFile(img_str, junkfile.getName());
                }

	}

	private void testUrl(String expected, String url, String file)
			throws IOException {
		InputStream in = MimeDetectionTest.class.getResourceAsStream(file);
		testStream(expected, url, in);
	}

	private void testFile(String expected, String filename) throws IOException {

		InputStream in = MimeDetectionTest.class.getResourceAsStream(filename);
		testStream(expected, filename, in);
	}

	private void testStream(String expected, String urlOrFileName,
			InputStream in) throws IOException {
		assertNotNull("Test stream: [" + urlOrFileName + "] is null!", in);
		if (!in.markSupported()) {
			in = new java.io.BufferedInputStream(in);
		}
		try {
			Metadata metadata = new Metadata();
			String mime = this.detector.detect(in, metadata).toString();
			assertEquals(
					urlOrFileName + " is not properly detected: detected.",
					expected, mime);

			// Add resource name and test again
			// metadata.set(Metadata.RESOURCE_NAME_KEY, urlOrFileName);
			mime = this.detector.detect(in, metadata).toString();
			assertEquals(urlOrFileName
					+ " is not properly detected after adding resource name.",
					expected, mime);
		} finally {
			in.close();
		}
	}

	private void assertNotNull(String string, InputStream in) {
		// TODO Auto-generated method stub

	}

	/**
	 * Test for type detection of empty documents.
	 */
	@Test
	public void testEmptyDocument() throws IOException {
		assertEquals(MediaType.OCTET_STREAM, detector.detect(
				new ByteArrayInputStream(new byte[0]), new Metadata()));

	}

}
