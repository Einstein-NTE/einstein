
#----------------------------------------------------------------------
# Installer for Einstein Thermal Energy Audit Program
Name Einstein
#----------------------------------------------------------------------

# General Symbol Definitions
!define REGKEY "SOFTWARE\$(^Name)"

# Installer attributes
OutFile ..\..\..\setup.exe
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
# Default pages are part of Modern User Interface 2 (MUI 2) or nsDialogs
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "res\gpl-3.0-standalone.rtf"
!insertmacro MUI_PAGE_COMPONENTS
Page custom nsAccountsetting nsAccountsettingLeave
Page custom nsInstallPath nsPathLeave
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

# Installer languages
!insertmacro MUI_LANGUAGE English

Var main.dir.path

Var mysql.path
Var mysql.version
Var mysql.einstein.exists
Var mysql.einstein.overwrite
Var mysql.exists
Var mysql.selected
Var mysql.user
Var mysql.password


Function .onSelChange
	/*${If} $mysql.selected == "1"
		StrCpy $mysql.selected "0"
	${ElseIf} $mysql.selected == "0"
		StrCpy $mysql.selected "1"
	${EndIf}*/
	${If} ${SectionIsSelected} ${MYSQLSEC}
		StrCpy $mysql.selected "1"
	${EndIf}
FunctionEnd
#----------------------------------------------------------------------
!macro CheckMySqlReg _RESULT _RESULT2
	StrCpy $4 "Software\MYSQL AB"
    StrCpy $0 0
    StrCpy ${_RESULT} ""
    StrCpy ${_RESULT2} ""
    loopSqlReg:
        ClearErrors
        EnumRegKey $1 HKLM $4 $0
        StrCmp $1 "" doneSqlReg
        IntOp $0 $0 + 1
        StrCpy $2 $1 12
        StrCmp $2 "MySQL Server" foundSqlReg 0
        Goto loopSqlReg
    foundSqlReg:
        ReadRegStr $R0 HKLM "$4\$1" "Location"
        IfFileExists "$R0\bin\mysql.exe" 0 doneSqlReg
        StrCpy ${_RESULT} "$R0"
        ReadRegStr $R0 HKLM "$4\$1" "Version"
        StrCpy ${_RESULT2} "$R0"
    doneSqlReg:
!macroend

#----------------------------------------------------------------------

!macro CheckforEinsteinDB _RESULT _UNAME _PW

	StrCpy ${_RESULT} "0"
	Push "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'einstein' INTO OUTFILE '$main.dir.path\einstein.txt';"
	Push "$main.dir.path\existingdb.txt" 
	Call WriteToFile  
	
	Push '"$mysql.pathbin\mysql" --user=${_UNAME} --password=${_PW} < "$main.dir.path\existingdb.txt"$\n'
	Push "$main.dir.path\existingdb.bat"
	Call WriteToFile 
	
	ExecWait "$main.dir.path\existingdb.bat"
	IfFileExists $main.dir.path\einstein.txt found
	Goto notfound
	found:
	StrCpy ${_RESULT} "1"
	notfound:
	
	Delete "$main.dir.path\existingdb.txt"
	Delete "$main.dir.path\existingdb.bat"
	Delete "$main.dir.path\einstein.txt"
!macroend
#----------------------------------------------------------------------
Function .onInit
    InitPluginsDir
    StrCpy $main.dir.path $PROGRAMFILES 3
	StrCpy $mysql.einstein.exists "0"
	StrCpy $mysql.selected "1"
	#Test at the Startup if MySQL is installed, and if the database Einstein exists
	!insertmacro CheckMySqlReg $mysql.path $mysql.version
	${If} $mysql.path == ""
		StrCpy $mysql.exists "0"
	${Else}
		StrCpy $mysql.exists "1"
		#!insertmacro CheckforEinsteinDB $mysql.einstein.exists
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

Function nsAccountsetting

  ${If} ${SectionIsSelected} ${MYSQLSEC}
		nsDialogs::Create 1018
		Pop $Dialog

		${If} $Dialog == error
			Abort
		${EndIf}
		
		${NSD_CreateLabel} 10u 87u 40u 8u "Username:"
		Pop $lbUsername

		${If} $mysql.exists == "1"
			${NSD_CreateText} 55u 85u 125u 12u ""
			MessageBox MB_OK "MySQL Installation already exists. Please enter your username and password to proceed"
			Pop $txtMySQLUser
		${Else}
			${NSD_CreateText} 55u 85u 125u 12u "root"
			Pop $txtMySQLUser
			EnableWindow $txtMySQLUser 0
		${EndIf}
		
		Push $txtMySQLUser
		Call notempty
		${NSD_OnChange} $txtMySQLUser notempty
		
		${NSD_CreateLabel} 10u 107u 40u 8u "Password:"
		Pop $lbPassword

		${If} $mysql.exists == "1"
			${NSD_CreatePassword} 55u 105u 125u 12u ""
		${Else}
			${NSD_CreatePassword} 55u 105u 125u 12u "root"
		${EndIf}				
		Pop $pwtxtMySQL

		${NSD_CreateLabel} 190u 85u 100u 10u "Change the default username."
		Pop $lbChangeUsername

		${NSD_CreateLabel} 190u 105u 100u 10u "Change the default password."
		Pop $lbChangepw

		${NSD_CreateLabel} 10u 25u 280u 25u "This option will create a new custom MySQL account for Einstein. \
		Please enter username and password."
		Pop $lbAccountDescription

		${NSD_CreateGroupBox} 5u 5u 290u 125u "MySQL Configuration"
		Pop $boxMySQLconfig

		nsDialogs::Show
		
	${EndIf}

FunctionEnd

Function notempty
	Pop $2
	${NSD_GetText} $2 $4
	GetDlgItem $R1 $HWNDPARENT 1
	${If} $4 != ""
        EnableWindow $R1 1
    ${Else}
        EnableWindow $R1 0
    ${EndIf}
FunctionEnd

#----------------------------------------------------------------------	
Function nsAccountsettingLeave
	${NSD_GetText} $txtMySQLUser $mysql.user
	${NSD_GetText} $pwtxtMySQL $mysql.password
	${If} $mysql.exists == "1"
		!insertmacro CheckforEinsteinDB $mysql.einstein.exists $mysql.user $mysql.password
		${If} $mysql.einstein.exists == "1"
			MessageBox MB_YESNO "Database with the name Einstein was found! Do you want to overwrite it?" IDYES true IDNO false
		${EndIf}
		true:
		StrCpy $mysql.einstein.overwrite "1"
		Goto next
		false:
		StrCpy $mysql.einstein.overwrite "0"
		next:
	${EndIf}
FunctionEnd



#----------------------------------------------------------------------

Var lbMySQL
Var lbPythonMysqlDir
Var boxInstallationpath
Var DirRequestMySQL
Var btnBrowseMySQLpath

Function nsInstallPath
	
	SectionGetFlags ${MYSQLSEC} $9
	
	${If} $mysql.exists == "0"
		nsDialogs::Create 1018
		Pop $DialogInstallpath

		${If} $DialogInstallpath == error
			Abort
		${EndIf}
		
		${NSD_CreateGroupbox} 10u 75u 285u 65u "Installation Path:"
		Pop $boxInstallationpath
	  
		${NSD_CreateLabel} 20u 117u 45u 10u "MySQL 5.1:"
		Pop $lbMySQL

		${NSD_CreateLabel} 15u 5u 265u 25u "Setup will install MySQL 5.1 in the following folder. To install in a different folder, click 'Browse' and select another folder. Click Next to continue."
		Pop $lbPythonMysqlDir

		${If} $mysql.path == ""
			${NSD_CreateDirRequest} 70u 115u 170u 12u "$PROGRAMFILES\MySQL\MySQL Server 5.1"
		${Else}
			${NSD_CreateDirRequest} 70u 115u 170u 12u "$mysql.path"
		${EndIf}
		Pop $DirRequestMySQL
		${NSD_OnChange} $DirRequestMySQL nsVerifyPath
		
		${NSD_CreateBrowseButton} 242u 115u 35u 12u "Browse"
		Pop $btnBrowseMySQLpath
		${NSD_OnClick} $btnBrowseMySQLpath nsFileChoose
		
		SectionGetFlags ${MYSQLSEC} $9
		${If} $9 != "1"
			EnableWindow $DirRequestMySQL 0
			EnableWindow $btnBrowseMySQLpath 0
		${EndIf}
		
		nsDialogs::Show
    ${EndIf}
FunctionEnd

#----------------------------------------------------------------------

Function nsPathLeave
	${If} $mysql.exists == "0"
		${NSD_GetText} $DirRequestMySQL $mysql.path
	${EndIf}
FunctionEnd

#----------------------------------------------------------------------

Function nsFileChoose

    nsDialogs::SelectFolderDialog /NOUNLOAD "" $0
    Pop $0
    ${If} $0 != "error"
        StrCpy $2 $0
        StrCpy $main.dir.path $0 "3"
    ${Else}
        StrCpy $4 $2 3
        ${If} $4 != $main.dir.path
            StrCpy $2 main.dir.path
        ${EndIf}
    ${EndIf}
    ${If} $0 == $main.dir.path
        ${NSD_SetText} $DirRequestMySQL "$0MySQL\MySQL Server 5.1"
    ${ElseIf} $0 == "error"
        ${If} $2 == $main.dir.path
            ${NSD_SetText} $DirRequestMySQL "$2MySQL\MySQL Server 5.1"
        ${Else}
            ${NSD_SetText} $DirRequestMySQL "$2\MySQL\MySQL Server 5.1"
        ${EndIf}  
    ${Else}
        ${NSD_SetText} $DirRequestMySQL "$0\MySQL\MySQL Server 5.1"
    ${EndIf}
    ${NSD_GetText} $DirRequestMySQL $mysql.path
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
    ${AndIf} $4 != $main.dir.path
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
#Begin of Installer Sections

Section -Main SEC0000
    SetOutPath $INSTDIR
    SetOverwrite on
	File /r ..\..\*
    WriteRegStr HKLM "${REGKEY}\Components" Main 1
SectionEnd

#----------------------------------------------------------------------

Section "Einstein" einsteinsection
SectionIn RO
SectionEnd

#----------------------------------------------------------------------

Section "MySQL" MYSQLSEC

	SetOutPath "$INSTDIR\Prerequisites\"
    File "..\Prerequisites\mysql-essential-5.1.24-rc-win32.msi"
    ExecWait '"msiexec" /i "$INSTDIR\Prerequisites\mysql-essential-5.1.24-rc-win32.msi" /quiet INSTALLDIR="$mysql.path"'

SectionEnd
#----------------------------------------------------------------------




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

    RMdir /r $INSTDIR\Prerequisites
	RMdir /r $INSTDIR\Install
    createShortCut "$DESKTOP\Einstein.lnk" "$INSTDIR\GUI\einstein.bat" "" "$INSTDIR\GUI\img\einstein.ico" 0
    Call CreateStartMenu
    
SectionEnd
#----------------------------------------------------------------------

Function CreateStartMenu
  CreateDirectory "$SMPROGRAMS\Einstein"
  CreateShortCut "$SMPROGRAMS\Einstein\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\Einstein\einstein.lnk" "$INSTDIR\GUI\einstein.bat" "" "$INSTDIR\GUI\img\einstein.ico" 0
FunctionEnd
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
# Macro for selecting uninstaller sections
!macro SELECT_UNSECTION SECTION_NAME UNSECTION_ID
    Push $R0
    ReadRegStr $R0 HKLM "${REGKEY}\Components" "${SECTION_NAME}"
    StrCmp $R0 1 0 next${UNSECTION_ID}
    !insertmacro SelectSection "${UNSECTION_ID}"
    Goto done${UNSECTION_ID}
next${UNSECTION_ID}:
    !insertmacro UnselectSection "${UNSECTION_ID}"
done${UNSECTION_ID}:
    Pop $R0
!macroend
#----------------------------------------------------------------------

# Uninstaller functions
Function un.onInit
    ReadRegStr $INSTDIR HKLM "${REGKEY}" Path
    !insertmacro SELECT_UNSECTION Main ${UNSEC0000}
FunctionEnd

#----------------------------------------------------------------------

# Uninstaller sections
Section /o -un.Main UNSEC0000

    RMDir /r /REBOOTOK $INSTDIR\auxiliary
    RMDir /r /REBOOTOK $INSTDIR\databases
    RMDir /r /REBOOTOK $INSTDIR\developers
    RMDir /r /REBOOTOK $INSTDIR\docs
    RMDir /r /REBOOTOK $INSTDIR\modules
    RMDir /r /REBOOTOK $INSTDIR\PE
    RMDir /r /REBOOTOK $INSTDIR\projects
    RMDir /r /REBOOTOK $INSTDIR\questionnaire
    RMDir /r /REBOOTOK $INSTDIR\reports
    RMDir /r /REBOOTOK $INSTDIR\sql
    RMDir /r /REBOOTOK $INSTDIR\tmp_dev
    RMDir /r /REBOOTOK $INSTDIR\.git
	RMDir /r /REBOOTOK $INSTDIR\Python25Einstein
	RMDir /r /REBOOTOK $INSTDIR\Prerequisites
	RMDir /r /REBOOTOK $SMPROGRAMS\Einstein
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
    RMDir /r /REBOOTOK $INSTDIR\GUI\img
    RMDir /r /REBOOTOK $INSTDIR\GUI\locale
    Delete $DESKTOP\Einstein.lnk
	RMDir /r /REBOOTOK $SMPROGRAMS\Einstein
    
    DeleteRegValue HKLM "${REGKEY}\Components" Main
SectionEnd



#----------------------------------------------------------------------

Section -un.post UNSEC0001
    DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)"
    Delete /REBOOTOK $INSTDIR\uninstall.exe
    DeleteRegValue HKLM "${REGKEY}" Path
    DeleteRegKey /IfEmpty HKLM "${REGKEY}\Components"
    DeleteRegKey /IfEmpty HKLM "${REGKEY}"
    RMDir /REBOOTOK $INSTDIR
SectionEnd

#----------------------------------------------------------------------















