#!/bin/sh
curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/detect" -F "api_key=ULMkOR2ixs4zLTIGz_5u0Tnj6yvpETd2" \
-F "api_secret=tOmHvb1WPT6eCydDIQ3xrUfVmkK1V1sW" \
-F "image_file=@/home/pi/pi/pics/3.jpg" \
-F "return_landmark=1" \
-F "return_attributes=gender,age"
