@ECHO OFF

SET man1=%1

git add .
git rm --cached aimagine\yolov3-wider_16000.weights
git rm --cached .\aimagine\yolov3-wider.cfg
git rm --cached aimagine\coco.names.wider
git rm --cached aimagine\people.jpg
git rm --cached img.jpg
git rm --cached aimagine\static\media\Cattura.PNG
git rm --cached aimagine\static\media\rekog_Cattura.PNG

git status

git commit -m %man1%