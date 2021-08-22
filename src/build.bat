::---------------------------------------------------------------------------
:: Generate basic
::---------------------------------------------------------------------------
python3 toyRoomGame.py > ..\build\toyroom.txt
python3 testGame.py > ..\build\test.txt

::---------------------------------------------------------------------------
:: Build disk 
::---------------------------------------------------------------------------

cd ..\build

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

