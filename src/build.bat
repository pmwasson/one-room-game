::---------------------------------------------------------------------------
:: Generate basic
::---------------------------------------------------------------------------
cd ..\build
python3 ..\src\toyRoomGame.py > toyroom.txt
python3 ..\src\testGame.py > test.txt


::---------------------------------------------------------------------------
:: Build disk 
::---------------------------------------------------------------------------

:: Start with a blank prodos disk
copy ..\disk\blank.dsk toyroom.dsk

:: Copy basic program
java -jar C:\jar\AppleCommander.jar -bas toyroom.dsk STARTUP < toyroom.txt
java -jar C:\jar\AppleCommander.jar -bas toyroom.dsk TESTGAME < test.txt

:: Copy results out of the build directory
copy toyroom.dsk ..\disk

::---------------------------------------------------------------------------
:: Test on emulator
::---------------------------------------------------------------------------
C:\AppleWin\Applewin.exe -no-printscreen-dlg -d1 toyroom.dsk

