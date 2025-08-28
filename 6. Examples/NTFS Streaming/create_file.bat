REM This file creates an malicious hidden stream.

echo Creating the malicious and readme.txt files

echo Please read this readme.txt file > readme.txt
echo This is really malicious... > malicious.dat

echo Creating the streams on readme.txt

type malicious.dat > readme.txt:malicious
del malicious.dat

type image.jpg > readme.txt:hacked

echo Ready!
