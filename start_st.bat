cls
@ECHO OFF
ECHO. ***********************************
ECHO. ** Starting Python Stimulus Environment **
ECHO. ** Consisting of Pyff and Psychopy **
ECHO. *******************************

call C:\ProgramData\Miniconda2\Scripts\activate.bat C:\ProgramData\Miniconda2
cd C:\Users\HIRF\nf\nf-stim\src
call conda activate st
call python FeedbackController.py

EXIT