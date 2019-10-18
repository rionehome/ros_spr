FILE_ID=1bn-zEOL1hsUwI1Hd4aS1LjUQsFYo4yp0
FILE_NAME=coco_posenet.npz.zip

curl -c /tmp/cookie.txt -s -L "https://drive.google.com/uc?export=download&id=${FILE_ID}" |grep confirm |  sed -e "s/^.*confirm=\(.*\)&amp;id=.*$/\1/" | xargs -I{} \
curl -b /tmp/cookie.txt  -L -o ${FILE_NAME} "https://drive.google.com/uc?confirm={}&export=download&id=${FILE_ID}"
unzip ${FILE_NAME}
mv coco_posenet.npz model
rm -rf ${FILE_NAME}


FILE_ID=1osfe6mWT4dlnmcUaIINZYKvIkqwVi759
FILE_NAME=cifier_adam.npz.zip

curl -c /tmp/cookie.txt -s -L "https://drive.google.com/uc?export=download&id=${FILE_ID}" |grep confirm |  sed -e "s/^.*confirm=\(.*\)&amp;id=.*$/\1/" | xargs -I{} \
curl -b /tmp/cookie.txt  -L -o ${FILE_NAME} "https://drive.google.com/uc?confirm={}&export=download&id=${FILE_ID}"
unzip ${FILE_NAME}
mv cifier_adam.npz model
rm -rf ${FILE_NAME}


FILE_ID=1qnV8_pWJofWOgsNXY3Kz5Iuh7ZrSYF_Y
FILE_NAME=haarcascade_frontalface_default.xml
curl -L -o ${FILE_NAME} "https://drive.google.com/uc?export=download&id=${FILE_ID}"
mv haarcascade_frontalface_default.xml model


FILE_ID=1azFacMd--wHUSNcwk82vYuKTKEsftxqQ
FILE_NAME=haarcascade_frontalface_alt.xml
curl -L -o ${FILE_NAME} "https://drive.google.com/uc?export=download&id=${FILE_ID}"
mv haarcascade_frontalface_alt.xml model
