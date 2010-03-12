
#----------------------------------------------------------------------
# Installer for Einstein Thermal Energy Audit Program
Name Einstein
#----------------------------------------------------------------------

# General Symbol Definitions
!define REGKEY "SOFTWARE\$(^Name)"

# Installer attributes
OutFile setup.exe
InstallDir $PROGRAMFILES\einstein
CRCCheck on
XPStyle on
ShowInstDetails hide
InstallDirRegKey HKLM "${REGKEY}" Path
ShowUninstDetails hide

#----------------------------------------------------------------------


# Definition of the MUI Installer Options 
# Customizes Look and Feel
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_FINISHPAGE_RUN "$INSTDIR\GUI\einstein.bat"
!define MUI_UNFINISHPAGE_NOAUTOCLOSE
!define MUI_WELCOMEFINISHPAGE_BITMAP "res\installtitle.bmp"
!define MUI_COMPONENTSPAGE_SMALLDESC

!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "res\einstein_logo.bmp"

#----------------------------------------------------------------------


# Include Files and Librarys

# Look and Feel of the Installer
!include MUI2.nsh
!include InstallOptions.nsh
!include nsDialogs.nsh

# Logic and various
!include Sections.nsh
!include LogicLib.nsh

#----------------------------------------------------------------------


# Installerpages with the correct order and custom pages
# Default pages are part of Modern User Interface 2 (MUI 2)
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "res\gpl-3.0-standalone.rtf"

Page custom nsAskMySQLAccount nsAskMySQLLeave
!insertmacro MUI_PAGE_COMPONENTS
Page custom nsAccountsetting nsAccountsettingLeave
Page custom nsInstallPath nsPathLeave
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

#----------------------------------------------------------------------

# Installer languages
!insertmacro MUI_LANGUAGE English

# Saves the mein Directory e.g. C:\
# Var MainDir
Var md

Var overrideDB
Var MySQLAccountText
Var mysql_instpath
Var mysql_pw
Var mysql_user

Var bmysqlinstall
Var bdotnetinstall

Var regadress
Var path_result
Var version_result
Var bmessage

#Begin of Installer Macros

#----------------------------------------------------------------------
# Macro for selecting uninstaller sections
!macro SELECT_UNSECTION SECTION_NAME UNSECTION_ID
    Push $R0
    ReadRegStr $R0 HKLM "${REGKEY}\Components" "${SECTION_NAME}"
    StrCmp $R0 1 0 next${UNSECTION_ID}
    !insertmacro SelectSection "${UNSECTION_ID}"
    GoTo done${UNSECTION_ID}
next${UNSECTION_ID}:
    !insertmacro UnselectSection "${UNSECTION_ID}"
done${UNSECTION_ID}:
    Pop $R0
!macroend

#----------------------------------------------------------------------

!macro CheckMySqlReg _RESULT _RESULT2
    Push $0
    Push $1
    Push $2
    Push $R0
    StrCpy $0 0
    StrCpy ${_RESULT} ""
    StrCpy ${_RESULT2} ""
    loopSqlReg:
        ClearErrors
        EnumRegKey $1 HKLM $regadress $0
        StrCmp $1 "" doneSqlReg
        IntOp $0 $0 + 1
        StrCpy $2 $1 12
        StrCmp $2 "MySQL Server" foundSqlReg 0
        Goto loopSqlReg
    foundSqlReg:
        ReadRegStr $R0 HKLM "$regadress\$1" "Location"
        IfFileExists "$R0\bin\mysql.exe" 0 doneSqlReg
        StrCpy ${_RESULT} "$R0"
        ReadRegStr $R0 HKLM "$regadress\$1" "Version"
        StrCpy ${_RESULT2} "$R0"
    doneSqlReg:
    Pop $R0
    Pop $2
    Pop $1
    Pop $0
!macroend

#----------------------------------------------------------------------

#Begin of Installer Sections

Section -Main SEC0000
    SetOutPath $INSTDIR
    SetOverwrite on
    File /r ..\..\auxiliary\*
	File /r ..\..\databases\*
	File /r ..\..\developers\*
	File /r ..\..\docs\*
	File /r ..\..\GUI\*
	File /r ..\..\modules\*
	File /r ..\..\PE\*
	File /r ..\..\docs\*
	File /r ..\..\projects\*
	File /r ..\..\questionnaire\*
	File /r ..\..\reports\*
	File /r ..\..\sql\*
	File /r ..\..\tmp_dev\*
	File /r ..\..\__init__.py
	
    WriteRegStr HKLM "${REGKEY}\Components" Main 1
SectionEnd

#----------------------------------------------------------------------

Section -post SEC0001
    WriteRegStr HKLM "${REGKEY}" Path $INSTDIR
    SetOutPath $INSTDIR
    WriteUninstaller $INSTDIR\uninstall.exe
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayName "$(^Name)"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayIcon $INSTDIR\uninstall.exe
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" UninstallString $INSTDIR\uninstall.exe
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" NoModify 1
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" NoRepair 1
SectionEnd

#----------------------------------------------------------------------

Section "Einstein" einsteinsection
SectionIn RO
SectionEnd

Section "MySQL" mysqlsection
	SetOutPath "$INSTDIR\Prerequisites\"
    StrCpy $bmysqlinstall "1"
    File "..\Prerequisites\mysql-essential-5.1.24-rc-win32.msi"
    ExecWait '"msiexec" /i "$INSTDIR\Prerequisites\mysql-essential-5.1.24-rc-win32.msi" /quiet INSTALLDIR="$mysql_instpath"'

SectionEnd


#----------------------------------------------------------------------

Section -DatabaseConig
    
	${If} $mysql_user == "root"
		${If} $mysql_pw == "root"
			ExecWait "$mysql_instpath\bin\mysqlinstanceconfig.exe -i -q ServiceName=MySQL RootPassword=root ServerType=DEVELOPMENT DatabaseType=MYISAM Port=3306"
		${Else}
			ExecWait "$mysql_instpath\bin\mysqlinstanceconfig.exe -i -q ServiceName=MySQL RootPassword=$mysql_pw ServerType=DEVELOPMENT DatabaseType=MYISAM Port=3306"
		${EndIf}
	${EndIf}
	
	${If} $mysql_user == "root"
	${AndIf} $overrideDB == "1"
		${If} $mysql_pw == "root"
			Push '"$mysql_instpath\bin\mysql" --user=root --password=root < "$INSTDIR\sql\einstein.sql"'
		${Else}
			Push '"$mysql_instpath\bin\mysql" --user=root --password=$mysql_pw < "$INSTDIR\sql\einstein.sql"' 
		${EndIf}
	${EndIf}
	Push "$INSTDIR\db.bat" ;file to write to 
    Call WriteToFile  
    ExecWait "$INSTDIR\db.bat"
	
	
    ${If} $mysql_user != "root"
        Push "Create user '$mysql_user'@'localhost' identified by '$mysql_pw';"
        Push "$INSTDIR\newuser.txt" ;file to write to 
        Call WriteToFile  
        
        Push "GRANT ALL ON einstein.* TO '$mysql_user'@'localhost';"
        Push "$INSTDIR\grants.txt" ;file to write to 
        Call WriteToFile  
        
        Push '"$mysql_instpath\bin\mysql" --user=root --password=root < "$INSTDIR\newuser.txt"' ;text to write to file 
        Push "$INSTDIR\newuser.bat" ;file to write to 
        Call WriteToFile  
        ExecWait "$INSTDIR\newuser.bat"
        
        Push '"$mysql_instpath\bin\mysql" --user=root --password=root < "$INSTDIR\grants.txt"' ;text to write to file 
        Push "$INSTDIR\grants.bat" ;file to write to 
        Call WriteToFile
        ExecWait "$INSTDIR\grants.bat"
		
    ${EndIf}

    ;Function Call for Writeline (Push, Push, Call, ExecWait)
    Push '"$mysql_instpath\bin\mysql" --user=$mysql_user --password=$mysql_pw < "$INSTDIR\sql\update_einsteinDB_V1.00b_to_V1.0.sql"'
    Push "$INSTDIR\data.bat"
    Call WriteToFile
    ExecWait "$INSTDIR\data.bat"

    Delete "$INSTDIR\db.bat"
    Delete "$INSTDIR\data.bat"

SectionEnd

#----------------------------------------------------------------------

Section -DatabaseUpdates

    ${If} $bmysqlinstall == 1
        Push '"$INSTDIR\Python25Einstein\python.exe" "$INSTDIR\Prerequisites\writeupdate.py" "$mysql_instpath\bin\mysql" "$INSTDIR" "$PROFILE" "$mysql_user" "$mysql_pw"'
        Push "$PROFILE\update.bat"
        Call WriteToFile
        ExecWait "$PROFILE\update.bat"
        Delete "$PROFILE\update.bat"
    ${EndIf}
SectionEnd

#----------------------------------------------------------------------
/*
Section ".netFramework" dotnetsection
    StrCpy $bdotnetinstall 1
    File "..\Prerequisites\WindowsInstaller-KB893803-v2-x86.exe"
    ExecWait '"$INSTDIR\Prerequisites\WindowsInstaller-KB893803-v2-x86.exe" /quiet'
    File "..\Prerequisites\dotnetfx35.exe"
    ExecWait '"$INSTDIR\Prerequisites\dotnetfx35" /passive'
SectionEnd
*/
#----------------------------------------------------------------------


Section -finish

    RmDir /r $INSTDIR\Prerequisites

    SetoutPath "$INSTDIR\GUI\"
    createShortCut "$DESKTOP\Einstein.lnk" "$INSTDIR\GUI\einstein.bat" "" "$INSTDIR\GUI\img\einstein.ico" 0
    
    call CreateStartMenu
    
SectionEnd


#----------------------------------------------------------------------

# Uninstaller sections
Section /o -un.Main UNSEC0000

    RmDir /r /REBOOTOK $INSTDIR\auxiliary
    RmDir /r /REBOOTOK $INSTDIR\databases
    RmDir /r /REBOOTOK $INSTDIR\developers
    RmDir /r /REBOOTOK $INSTDIR\docs
    RmDir /r /REBOOTOK $INSTDIR\modules
    RmDir /r /REBOOTOK $INSTDIR\PE
    RmDir /r /REBOOTOK $INSTDIR\projects
    RmDir /r /REBOOTOK $INSTDIR\questionnaire
    RmDir /r /REBOOTOK $INSTDIR\reports
    RmDir /r /REBOOTOK $INSTDIR\sql
    RmDir /r /REBOOTOK $INSTDIR\tmp_dev
    RmDir /r /REBOOTOK $INSTDIR\.git
	RmDir /r /REBOOTOK $INSTDIR\Python25Einstein
	RmDir /r /REBOOTOK $INSTDIR\Prerequisites
	RmDir /r /REBOOTOK $SMPROGRAMS\Einstein
    Delete $INSTDIR\__init__.py
    Delete $INSTDIR\__init__.pyc
    Delete $INSTDIR\einstein
    Delete $INSTDIR\GUI\*.py
    Delete $INSTDIR\GUI\*.pyc
    Delete $INSTDIR\GUI\*.txt
    Delete $INSTDIR\GUI\*.csv
    Delete $INSTDIR\GUI\einstein.bat
    Delete $INSTDIR\einstein.lnk
    Delete $INSTDIR\GUI\einsteinrun.bat
    RmDir /r /REBOOTOK $INSTDIR\GUI\img
    RmDir /r /REBOOTOK $INSTDIR\GUI\locale
    Delete $DESKTOP\Einstein.lnk
    
    DeleteRegValue HKLM "${REGKEY}\Components" Main
SectionEnd

#----------------------------------------------------------------------

Section -un.post UNSEC0001
    DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)"
    Delete /REBOOTOK $INSTDIR\uninstall.exe
    DeleteRegValue HKLM "${REGKEY}" Path
    DeleteRegKey /IfEmpty HKLM "${REGKEY}\Components"
    DeleteRegKey /IfEmpty HKLM "${REGKEY}"
    RmDir /REBOOTOK $INSTDIR
SectionEnd

#----------------------------------------------------------------------


#Begin of Installer Functions

#----------------------------------------------------------------------
Function CreateStartMenu
  CreateDirectory "$SMPROGRAMS\Einstein"
  CreateShortCut "$SMPROGRAMS\Einstein\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\Einstein\einstein.lnk" "$INSTDIR\GUI\einstein.bat" "" "$INSTDIR\GUI\img\einstein.ico" 0
FunctionEnd
#----------------------------------------------------------------------


Function testversion
    ${If} $bmessage != "1"
        StrCpy $bmessage "1"
            
        StrCpy $5 $4 "" -13
        StrCpy $6 $5 1
        StrCpy $5 $4 1 -12
        ${If} $version_result != ""
            MessageBox MB_YESNO "MySQL Version $version_result is already installed. \ 
			If you don't want to override or install a new MySQL Version 5.1.24 uncheck it! \
			Do you want to override the einstein database if it exists?" IDYES true IDNO false
		${EndIf}
    ${EndIf}
	true:
	StrCpy $overrideDB "1"
	Goto next
	false:
	StrCpy $overrideDB "0"
	next:

FunctionEnd

#----------------------------------------------------------------------
Function .onInit
    InitPluginsDir
	
    StrCpy $md $PROGRAMFILES 3
    StrCpy $1 $PROGRAMFILES
    StrCpy $2 $PROGRAMFILES
    StrCpy $mysql_user "root"
    StrCpy $mysql_pw "root"
    StrCpy $regadress "Software\MYSQL AB"
    StrCpy $bmessage "0"
	StrCpy $overrideDB "0"

    !insertmacro CheckMySqlReg $path_result $version_result
	${If} $path_result == ""
		MessageBox MB_OK "Pfad ist leer"
		
	${Else}
		StrCpy $mysql_instpath $path_result -1
		MessageBox MB_OK "Pfad ist : $path_result"
	${EndIf}
	
	
	FunctionEnd

#----------------------------------------------------------------------

Function WriteToFile
 Exch $0 ;file to write to
 Exch
 Exch $1 ;text to write
 
  FileOpen $0 $0 a #open file
   FileSeek $0 0 END #go to end
   FileWrite $0 $1 #write to file
  FileClose $0
 
 Pop $1
 Pop $0
FunctionEnd
 
#----------------------------------------------------------------------

# Uninstaller functions
Function un.onInit
    ReadRegStr $INSTDIR HKLM "${REGKEY}" Path
    !insertmacro SELECT_UNSECTION Main ${UNSEC0000}
FunctionEnd


#----------------------------------------------------------------------


Var Dialog
Var DialogInstallpath
Var lbUsername
Var lbPassword
Var lbChangeUsername
Var lbChangepw
Var lbAccountDescription
Var txtMySQLUser
Var pwtxtMySQL
Var boxMySQLconfig
Var Chk_path
Var Chk_path_state


Function nsAskMySQLAccount
	
    Call testversion
	${If} $overrideDB == "1"
		nsDialogs::Create 1018
		Pop $Dialog

		${If} $Dialog == error
			Abort
		${EndIf}

	
		StrCpy $MySQLAccountText "Please enter your MySQL Account Information"
		
		${NSD_CreateLabel} 10u 87u 40u 8u "Username:"
		Pop $lbUsername

		${NSD_CreateText} 55u 85u 125u 12u "$mysql_user"
		Pop $txtMySQLUser

		${NSD_CreateLabel} 10u 107u 40u 8u "Password:"
		Pop $lbPassword

		${NSD_CreatePassword} 55u 105u 125u 12u "$mysql_pw"
		Pop $pwtxtMySQL
		
		${NSD_CreateLabel} 190u 85u 100u 10u "Change the default username."
		Pop $lbChangeUsername
		
		${NSD_CreateLabel} 190u 105u 100u 10u "Change the default password."
		Pop $lbChangepw
		
		${NSD_CreateLabel} 10u 65u 280u 20u $MySQLAccountText
		Pop $lbAccountDescription
			
		SectionGetFlags ${mysqlsection} $R9
		${If} $R9 != "1" 
			#EnableWindow $Chk_path 0
		${EndIf}
		
		;${NSD_CreateLabel} 10u 105u 280u 10u "(Username: 'root' and Password: 'root' is the recommended choice)"
		;Pop $Label6
		
		${NSD_CreateGroupBox} 5u 5u 290u 125u "MySQL Configuration"
		Pop $boxMySQLconfig

		nsDialogs::Show
	${EndIf}
FunctionEnd

#----------------------------------------------------------------------


Function nsAccountsetting

	${If} $overrideDB == "0"
		nsDialogs::Create 1018
		Pop $Dialog
		
		${If} $Dialog == error
			Abort
		${EndIf}

		StrCpy $MySQLAccountText "This option will create a new custom MySQL account for Einstein. \
		If you dont need a new Useraccount for Einstein leave fields unchanged. If you already got \
		a MySQL User, please fill in your account data."

		${NSD_CreateLabel} 10u 87u 40u 8u "Username:"
		Pop $lbUsername

		${NSD_CreateText} 55u 85u 125u 12u "$mysql_user"
		Pop $txtMySQLUser
		${If} $Chk_path_state != ${BST_CHECKED}
			EnableWindow $txtMySQLUser 0
		${EndIf}
		
		${NSD_CreateLabel} 10u 107u 40u 8u "Password:"
		Pop $lbPassword

		${NSD_CreatePassword} 55u 105u 125u 12u "$mysql_pw"
		Pop $pwtxtMySQL
		${If} $Chk_path_state != ${BST_CHECKED}
			EnableWindow $pwtxtMySQL 0
		${EndIf}
		
		${NSD_CreateLabel} 190u 85u 100u 10u "Change the default username."
		Pop $lbChangeUsername
		
		${NSD_CreateLabel} 190u 105u 100u 10u "Change the default password."
		Pop $lbChangepw
		
		${NSD_CreateLabel} 10u 25u 280u 25u $MySQLAccountText
		Pop $lbAccountDescription
		
		${NSD_CreateCheckbox} 10u 65u 115u 10u "Set Custom User Account"
		Pop $Chk_path
		${NSD_OnClick} $Chk_path EnDisableForm
		

		${If} $Chk_path_state == ${BST_CHECKED}
			${NSD_Check} $Chk_path
		${EndIf}
		
		SectionGetFlags ${mysqlsection} $R9
		${If} $R9 != "1" 
			#EnableWindow $Chk_path 0
		${EndIf}
		
		;${NSD_CreateLabel} 10u 105u 280u 10u "(Username: 'root' and Password: 'root' is the recommended choice)"
		;Pop $Label6
		
		${NSD_CreateGroupBox} 5u 5u 290u 125u "MySQL Configuration"
		Pop $boxMySQLconfig

		nsDialogs::Show
	${EndIf}
FunctionEnd

#----------------------------------------------------------------------

Function nsAskMySQLLeave
    ${NSD_GetState} $Chk_path $Chk_path_state
    
    ${If} $Chk_path_state == ${BST_CHECKED}
        ${NSD_GetText} $txtMySQLUser $mysql_user
        ${NSD_GetText} $pwtxtMySQL $mysql_pw
    ${Else}
        StrCpy $mysql_user "root"
        StrCpy $mysql_pw "root"
    ${EndIf}
FunctionEnd

#----------------------------------------------------------------------
Function nsAccountsettingLeave
    ${NSD_GetState} $Chk_path $Chk_path_state
    
    ${If} $Chk_path_state == ${BST_CHECKED}
        ${NSD_GetText} $txtMySQLUser $mysql_user
        ${NSD_GetText} $pwtxtMySQL $mysql_pw
    ${Else}
        StrCpy $mysql_user "root"
        StrCpy $mysql_pw "root"
    ${EndIf}
    
FunctionEnd

#----------------------------------------------------------------------

Var lbMySQL
Var lbPythonMysqlDir
Var boxInstallationpath
Var DirRequestMySQL
Var btnBrowseMySQLpath


Function nsInstallPath
Call einsteinDBexists
	SectionGetFlags ${mysqlsection} $9
	${If} $9 == "1"
		nsDialogs::Create 1018
		Pop $DialogInstallpath

		${If} $DialogInstallpath == error
			Abort
		${EndIf}
		
		${NSD_CreateGroupbox} 10u 75u 285u 65u "Installation Paths:"
		Pop $boxInstallationpath
	  
		${NSD_CreateLabel} 20u 117u 45u 10u "MySQL 5.1:"
		Pop $lbMySQL

		${NSD_CreateLabel} 15u 5u 265u 25u "Setup will install MySQL 5.1 in the following folder. To install in a different folder, click 'Browse' and select another folder. Click Next to continue."
		Pop $lbPythonMysqlDir

		${If} $path_result == ""
			${NSD_CreateDirRequest} 70u 115u 170u 12u "$PROGRAMFILES\MySQL\MySQL Server 5.1"
		${Else}
			${NSD_CreateDirRequest} 70u 115u 170u 12u "$path_result"
		${EndIf}
		Pop $DirRequestMySQL
		${NSD_OnChange} $DirRequestMySQL nsVerifyPath
		
		${NSD_CreateBrowseButton} 242u 115u 35u 12u "Browse"
		Pop $btnBrowseMySQLpath
		${NSD_OnClick} $btnBrowseMySQLpath nsFileChoose
		
		SectionGetFlags ${mysqlsection} $9
		${If} $9 != "1"
			EnableWindow $DirRequestMySQL 0
			EnableWindow $btnBrowseMySQLpath 0
		${EndIf}
		
		nsDialogs::Show
    ${EndIf}
FunctionEnd

#----------------------------------------------------------------------

Function nsPathLeave

	${If} $9 == "1" 
        ${NSD_GetText} $DirRequestMySQL $mysql_instpath
    ${EndIf}
FunctionEnd

#----------------------------------------------------------------------

Function nsFileChoose

    nsDialogs::SelectFolderDialog /NOUNLOAD "" $0
    Pop $0
    ${If} $0 != "error"
        StrCpy $2 $0
        StrCpy $md $0 "3"
    ${Else}
        StrCpy $4 $2 3
        ${If} $4 != $md
            StrCpy $2 md
        ${EndIf}
    ${EndIf}
    ${If} $0 == $md
        ${NSD_SetText} $DirRequestMySQL "$0MySQL\MySQL Server 5.1"
    ${ElseIf} $0 == "error"
        ${If} $2 == $md
            ${NSD_SetText} $DirRequestMySQL "$2MySQL\MySQL Server 5.1"
        ${Else}
            ${NSD_SetText} $DirRequestMySQL "$2\MySQL\MySQL Server 5.1"
        ${EndIf}  
    ${Else}
        ${NSD_SetText} $DirRequestMySQL "$0\MySQL\MySQL Server 5.1"
    ${EndIf}
    ${NSD_GetText} $DirRequestMySQL $mysql_instpath
FunctionEnd


#----------------------------------------------------------------------

Var STR_HAYSTACK
Var STR_NEEDLE
Var STR_CONTAINS_VAR_1
Var STR_CONTAINS_VAR_2
Var STR_CONTAINS_VAR_3
Var STR_CONTAINS_VAR_4
Var STR_RETURN_VAR
 
Function StrContains
  Exch $STR_NEEDLE
  Exch 1
  Exch $STR_HAYSTACK
  ; Uncomment to debug
  ;MessageBox MB_OK 'STR_NEEDLE = $STR_NEEDLE STR_HAYSTACK = $STR_HAYSTACK '
    StrCpy $STR_RETURN_VAR ""
    StrCpy $STR_CONTAINS_VAR_1 -1
    StrLen $STR_CONTAINS_VAR_2 $STR_NEEDLE
    StrLen $STR_CONTAINS_VAR_4 $STR_HAYSTACK
    loop:
      IntOp $STR_CONTAINS_VAR_1 $STR_CONTAINS_VAR_1 + 1
      StrCpy $STR_CONTAINS_VAR_3 $STR_HAYSTACK $STR_CONTAINS_VAR_2 $STR_CONTAINS_VAR_1
      StrCmp $STR_CONTAINS_VAR_3 $STR_NEEDLE found
      StrCmp $STR_CONTAINS_VAR_1 $STR_CONTAINS_VAR_4 done
      Goto loop
    found:
      StrCpy $STR_RETURN_VAR $STR_NEEDLE
      Goto done
    done:
   Pop $STR_NEEDLE ;Prevent "invalid opcode" errors and keep the
   Exch $STR_RETURN_VAR  
FunctionEnd


!macro _StrContainsConstructor OUT NEEDLE HAYSTACK
  Push "${HAYSTACK}"
  Push "${NEEDLE}"
  Call StrContains
  Pop "${OUT}"
!macroend

!define StrContains '!insertmacro "_StrContainsConstructor"'


#----------------------------------------------------------------------

Function nsVerifyPath
    Pop $2 #DirRequest
    ${NSD_GetText} $2 $4
    GetDlgItem $R1 $HWNDPARENT 1
    StrCpy $0 $4 3
    StrCpy $1 $4 "" 3
    ${StrContains} $R2 ":" $1
    ${StrContains} $R3 "*" $1
    ${StrContains} $R4 "?" $1
    ${StrContains} $R5 "$\"" $1
    ${StrContains} $R6 "<" $1
    ${StrContains} $R7 ">" $1
    ${StrContains} $R8 "|" $1
    ${StrContains} $R9 "\\" $1
    
    #Check if Installation isn't attempted in Windows Directory
    StrCpy $3 $1 7
    ${If} ${FileExists} "$0\*.*"
    ${AndIf} $4 != $md
    ${AndIf} $3 != "Windows"
    ${AndIf} $R2 == "" 
    ${AndIf} $R3 == "" 
    ${AndIf} $R4 == "" 
    ${AndIf} $R5 == "" 
    ${AndIf} $R6 == "" 
    ${AndIf} $R7 == "" 
    ${AndIf} $R8 == "" 
    ${AndIf} $R9 == "" 
        #Enable the Next Button
        EnableWindow $R1 1
    ${Else}
        EnableWindow $R1 0
    ${EndIf}

FunctionEnd

#----------------------------------------------------------------------

Function EnDisableForm
    Pop $Chk_path
    ${NSD_GetState} $Chk_path $0
    ${If} $0 == 1
        EnableWindow $txtMySQLUser 1
        EnableWindow $pwtxtMySQL 1
    ${Else}
        EnableWindow $txtMySQLUser 0
        EnableWindow $pwtxtMySQL 0
    ${EndIf}
FunctionEnd


Function checkforEinsteinDB
	${If} $path_result != ""
	
	${EndIf}

FunctionEnd

Function einsteinDBexists
	
	Push "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'einstein' INTO OUTFILE '$md\einstein.txt';"
	Push "$INSTDIR\existingdb.txt" 
	Call WriteToFile  
	
	#Check for Default Passwords in MySQL root account
	
	Push '"$mysql_instpath\bin\mysql" --user=root < "$INSTDIRexistingdb.txt"$\n' 
	Push "$INSTDIR\existingdb.bat"
	Call WriteToFile  
	
	#Push '"$mysql_instpath\bin\mysql" --user=root --password=root < "$INSTDIR\existingdb.txt"$\n' 
	#Push "$INSTDIR\existingdb.bat"
	#Call WriteToFile  
	
	Push '"$mysql_instpath\bin\mysql" --user=root --password=mysql < "$INSTDIR\existingdb.txt"' 
	Push "$INSTDIR\existingdb.bat"
	Call WriteToFile  

	ExecWait "$INSTDIR\existingdb.bat"

	FileOpen $0 "$mdeinstein.txt" r
	IfErrors done
	FileRead $0 $1
	MessageBox MB_OK "Ergebnis: $1"
	FileClose $0
	done:
	MessageBox MB_OK "$mdeinstein.txt  Ergebnis: $1"
	
	Delete "$INSTDIR\existingdb.bat"
	Delete "$INSTDIR\existingdb.txt"
	#Delete "$md\einstein.txt"
FunctionEnd