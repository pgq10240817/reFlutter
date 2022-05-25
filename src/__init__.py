import pkg_resources
from io import BytesIO
import re
import sys
import csv
import string
import os
import os.path
from os.path import join
from zipfile import ZipFile
import zipfile
import shutil

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
    from urllib.request import urlopen
else:
    from urllib import urlretrieve
    from urllib import urlopen

patchDump = True    

IPBurp = '192.168.1.12'
PROXY = '10.8.0.67'
libAppArm64 = '',''
libAppArm = '',''
libAppX64 = '',''
libAppX86 = '',''
libios = '',''
libappHash = ''
ZIPSTORED = False

def patchLibrary():
 print('patchLibrary return');
 if True:
     return;


 if len(libios[1]) != 0:
    buffer = open('Flutter', 'rb').read().replace(PROXY, IPBurp.encode('ascii'))
    open('Flutter', 'wb').write(buffer)
 if len(libAppArm64[1]) != 0:
    buffer = open('libflutter_arm64.so', 'rb').read().replace(PROXY, IPBurp.encode('ascii'))
    open('libflutter_arm64.so', 'wb').write(buffer)
 if len(libAppArm[1]) != 0:
    buffer = open('libflutter_arm.so', 'rb').read().replace(PROXY, IPBurp.encode('ascii'))
    open('libflutter_arm.so', 'wb').write(buffer)
 if len(libAppX64[1]) != 0:
    buffer = open('libflutter_x64.so', 'rb').read().replace(PROXY, IPBurp.encode('ascii'))
    open('libflutter_x64.so', 'wb').write(buffer)

def patchCase():
 global patchDump
 try:
     choice = raw_input("\n Choose an option: \n\n 1. Traffic monitoring and interception \n 2. Display absolute code offset for functions\n\n [1/2]? ").lower()
 except:
     choice = input('\n Choose an option: \n\n 1. Traffic monitoring and interception \n 2. Display absolute code offset for functions\n\n [1/2]? ').lower()
 if choice == "1":
   patchDump = False
   return
 elif choice == "2":
   print("\n This mode is only for dump and offset output, slow application operation is possible (network patch is still left)")
   return
 else:
   print(" Please respond with '1' or '2'\n")
 patchCase()

def inputIPBurp():
    global IPBurp
    try:
        IPBurp = raw_input("\nExample: (192.168.1.154) etc.\nPlease enter your BurpSuite IP: ")
        if not re.match(r'[0-9]+(?:\.[0-9]+){3}', IPBurp):
            print("Invalid IP Address")
            inputIPBurp()
    except:
        IPBurp = input('\nExample: (192.168.1.154) etc.\nPlease enter your BurpSuite IP: ')
        if not re.match(r'[0-9]+(?:\.[0-9]+){3}', IPBurp):
            print("Invalid IP Address")
            inputIPBurp()
    convertIPFix()

def networkLib():
    global libAppArm64,libAppArm,libAppX64,libAppX86,libios,patchDump
    verUrl = "v2-"
    if patchDump:
       verUrl = "v3-"
    if len(libios[1]) != 0:
       try:
        urlretrieve("https://github.com/Impact-I/reFlutter/releases/download/ios-"+verUrl+libios[1]+"/Flutter", "Flutter")
       except:
        libios='',''
        notexcept("Flutter")
    if len(libAppArm64[1]) != 0:
       try: 
        urlretrieve("https://github.com/Impact-I/reFlutter/releases/download/android-"+verUrl+libAppArm64[1]+"/libflutter_arm64.so", "libflutter_arm64.so")
       except:
        libAppArm64='',''
        notexcept("libflutter_arm64.so")
    if len(libAppArm[1]) != 0:
       try:
        urlretrieve("https://github.com/Impact-I/reFlutter/releases/download/android-"+verUrl+libAppArm[1]+"/libflutter_arm.so", "libflutter_arm.so")
       except:
        libAppArm='',''
        notexcept("libflutter_arm.so")
    if len(libAppX64[1]) != 0:
       try:
        urlretrieve("https://github.com/Impact-I/reFlutter/releases/download/android-"+verUrl+libAppX64[1]+"/libflutter_x64.so", "libflutter_x64.so")
       except:
        libAppX64='',''
        notexcept("libflutter_x64.so")
    if len(libAppX86[1]) != 0:
       try:
        urlretrieve("https://github.com/Impact-I/reFlutter/releases/download/android-"+verUrl+libAppX86[1]+"/libflutter_x86.so", "libflutter_x86.so")
       except:
        libAppX86='',''
        notexcept("libflutter_x86.so")
    patchLibrary()

def convertIPFix():
    global IPBurp
    intoct = list(IPBurp.split('.'))
    finallistIP=list(IPBurp.split('.'))
    intoct.sort(key=lambda s: len(s))
    intoct.reverse()
    for i in intoct:
        if len(i)!=3 and int(i)>7 and int(i)>63 and len('.'.join(intoct))<15: #64-99
            intoct[intoct.index(i)]=str(oct(int(i))).replace('o','')
        elif len(i)!=3 and int(i)>7 and int(i)<64 and len('.'.join(intoct))<15: #8-63
            intoct[intoct.index(i)]=str(oct(int(i))).replace('o','')
        elif len(i)<3 and int(i)<8 and len('.'.join(intoct))<15: #0-7
            intoct[intoct.index(i)]=intoct[intoct.index(i)].zfill(3)
    for i in intoct:
        if i.startswith('0'):
            if len(i)!=3 and int(i, 8)>7 and len('.'.join(intoct))>15: #8-63
                intoct[intoct.index(i)]=str(int(i, 8)).replace('o','')
            elif len(i)<3 and int(i)<8 and len('.'.join(intoct))<15: #0-7
                intoct[intoct.index(i)]=intoct[intoct.index(i)].zfill(3)
        elif len(i)==3 and int(i)>7 and int(i)>99 and len('.'.join(intoct))>15: #64-99
            intoct[intoct.index(i)]=str(oct(int(i))).replace('o','')
    for f in finallistIP:
        for i in intoct:
            if i.startswith('0'):
                if f==str(int(i, 8)):
                    finallistIP[finallistIP.index(f)]=i.replace('o','')
    IPBurp = '.'.join(finallistIP)

def notexcept(filename):
    try:
        os.remove(filename)
    except:
        pass

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            if type(file) is str:
                if file.endswith('.so') and ZIPSTORED or file.endswith('resources.arsc'):
                    ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root.replace('release/',''), file),os.path.join(path, '..')),zipfile.ZIP_STORED)
                else:
                    ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root.replace('release/',''), file),os.path.join(path, '..')),zipfile.ZIP_DEFLATED)
            else:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root.replace('release/',''), file),os.path.join(path, '..')),zipfile.ZIP_DEFLATED)

def replaceLibFlutter():
    if len(sys.argv) < 3:
        patchCase()
        checkHash()
        inputIPBurp()
        print("\n Wait...\n")
        networkLib()
    if os.path.exists("libflutter_arm64.so") or os.path.exists("libflutter_arm.so") or os.path.exists("libflutter_x64.so") or os.path.exists("libflutter_x86.so") or os.path.exists("Flutter"):
     try:
        shutil.move("Flutter", join("release",libios[0].replace("App.framework/App","Flutter.framework/Flutter").replace("FlutterApp.framework/FlutterApp","Flutter.framework/Flutter")))
     except:
         pass
     try:
        shutil.move("libflutter_arm64.so", join("release",libAppArm64[0].replace("libapp.so","libflutter.so")))
     except:
         pass
     try:
        shutil.move("libflutter_arm.so", join("release",libAppArm[0].replace("libapp.so","libflutter.so")))
     except:
         pass
     try:
        shutil.move("libflutter_x64.so", join("release",libAppX64[0].replace("libapp.so","libflutter.so")))
     except:
         pass
     try:
        shutil.move("libflutter_x86.so", join("release",libAppX86[0]))
     except:
         pass

     zipf = zipfile.ZipFile('release.RE.zip', 'w', zipfile.ZIP_DEFLATED)
     zipdir('release/', zipf)
     zipf.close()
     shutil.rmtree('libappTmp')
     shutil.rmtree('release')
     print("\nSnapshotHash: "+libappHash)
     if len(libios[1]) != 0:
         shutil.move("release.RE.zip", "release.RE.ipa")
         print("The resulting ipa file: ./release.RE.ipa\nPlease install the ipa file\n\nConfigure Burp Suite proxy server to listen on *:8888\nProxy Tab -> Options -> Proxy Listeners -> Edit -> Binding Tab\n\nThen enable invisible proxying in Request Handling Tab\nSupport Invisible Proxying -> true\n")
     else:
         shutil.move("release.RE.zip", "release.RE.apk")
         print("The resulting apk file: ./release.RE.apk")
         print("Please sign,align the apk file\n\nConfigure Burp Suite proxy server to listen on *:8888\nProxy Tab -> Options -> Proxy Listeners -> Edit -> Binding Tab\n\nThen enable invisible proxying in Request Handling Tab\nSupport Invisible Proxying -> true\n")
     sys.exit()

def replaceFileText(fname,textOrig,textReplace):
   try:
    with open(fname, 'r') as file :
     filedata = file.read()
     filedata = filedata.replace(textOrig, textReplace)
    with open(fname, 'w') as file:
     file.write(filedata)
   except (IOError, OSError) as e:
       pass

def patchSource(hashS,ver):
    global patchDump
    try:
        os.makedirs(os.path.join(os.environ["HOME"],"Documents"))
    except:
        pass
    try:
        os.makedirs("Documents")
    except:
        pass
    replaceFileText("DEPS","'src/third_party/dart/third_party/pkg/stagehand':\n   Var('dart_git') + '/stagehand.git@e64ac90cac508981011299c4ceb819149e71f1bd',", "")
    replaceFileText("DEPS","'src/third_party/dart/third_party/pkg/stagehand':\n   Var('dart_git') + '/stagehand.git' + '@' + Var('dart_stagehand_tag'),", "")
    replaceFileText("DEPS","'src/third_party/dart/third_party/pkg/tflite_native':\n   Var('dart_git') + '/tflite_native.git' + '@' + Var('dart_tflite_native_rev'),", "")
    replaceFileText('src/third_party/dart/DEPS','Var("dart_root") + "/third_party/pkg/tflite_native":\n      Var("dart_git") + "tflite_native.git" + "@" + Var("tflite_native_rev"),', '')
    replaceFileText('DEPS','Var("dart_root") + "/third_party/pkg/tflite_native":\n      Var("dart_git") + "tflite_native.git" + "@" + Var("tflite_native_rev"),', '')
    if ver>=24 and patchDump:
        replaceFileText('src/third_party/dart/runtime/vm/clustered_snapshot.cc','monomorphic_entry_point + unchecked_offset','previous_text_offset_')
    if ver<24 and patchDump:
        replaceFileText('src/third_party/dart/runtime/vm/clustered_snapshot.cc','monomorphic_entry_point + unchecked_offset','bare_offset')
    if ver<39 and patchDump:
        replaceFileText('src/third_party/dart/runtime/vm/app_snapshot.cc','monomorphic_entry_point + unchecked_offset','previous_text_offset_')
    if ver>38 and patchDump:
        replaceFileText('src/third_party/dart/runtime/vm/app_snapshot.cc','monomorphic_entry_point + unchecked_offset','instructions_table_.rodata()->entries()[instructions_table_.rodata()->first_entry_with_code + instructions_index_-1].pc_offset')
    if patchDump:
        replaceFileText('src/third_party/dart/runtime/vm/dart.cc','FLAG_print_class_table)','true)')
        replaceFileText('src/third_party/dart/runtime/vm/class_table.cc','#include "vm/visitor.h"','#include "vm/visitor.h"\n#include <sys/stat.h>')
    if ver>27:
        replaceFileText('src/flutter/BUILD.gn','  if (is_android) {\n    public_deps +=\n        [ "//flutter/shell/platform/android:flutter_shell_native_unittests" ]\n  }','')
    if ver>27 and patchDump:
        replaceFileText('src/third_party/dart/runtime/vm/class_table.cc','::Print() {','::Print()  { OS::PrintErr("reFlutter");\n char pushArr[160000]="";\n')
        replaceFileText('src/third_party/dart/runtime/vm/class_table.cc','OS::PrintErr("%" Pd ": %s\\n", i, name.ToCString());','\n     auto& funcs = Array::Handle(cls.functions());    if (funcs.Length()>1000) {    continue;    }	char classText[250000]=""; 	  String& supname = String::Handle();  	  name = cls.Name();	strcat(classText,cls.ToCString());  	  Class& supcls = Class::Handle();    supcls = cls.SuperClass();  	  if (!supcls.IsNull()) {		 supname = supcls.Name();		  strcat(classText," extends ");		 strcat(classText,supname.ToCString()); 	}		  const auto& interfaces = Array::Handle(cls.interfaces());	auto& interface = Instance::Handle();		  for (intptr_t in = 0;in < interfaces.Length(); in++) {	interface^=interfaces.At(in);	if(in==0){strcat(classText," implements ");} 	  if(in>0){strcat(classText," , ");}		strcat(classText,interface.ToCString());	}		  strcat(classText," {\\n");	const auto& fields = Array::Handle(cls.fields());   	  auto& field = Field::Handle();	auto& fieldType = AbstractType::Handle(); 	  String& fieldTypeName = String::Handle();	String& finame = String::Handle();		  Instance& instance2 = Instance::Handle();		  for (intptr_t f = 0; f < fields.Length(); f++)		  {    field ^= fields.At(f);	finame = field.name();	fieldType = field.type();	fieldTypeName = fieldType.Name();	strcat(classText,"  ");		  strcat(classText,fieldTypeName.ToCString()); 	strcat(classText," ");	strcat(classText,finame.ToCString()); 		  if(field.is_static()){			instance2 ^= field.StaticValue();			strcat(classText," = ");			  strcat(classText,instance2.ToCString());			strcat(classText," ;\\n");  } 	  else {	  strcat(classText," = ");	  strcat(classText," nonstatic;\\n");  }	}  	  for (intptr_t c = 0; c < funcs.Length(); c++) {		    auto& func = Function::Handle();    func = cls.FunctionFromIndex(c);  	  String& signature = String::Handle();    signature = func.InternalSignature();auto& codee = Code::Handle(func.CurrentCode());	  	  if(!func.IsLocalFunction()) {		  strcat(classText," \\n  ");	strcat(classText,func.ToCString());	strcat(classText," ");    strcat(classText,signature.ToCString());		  strcat(classText," { \\n\\n              ");	  char append[70];	  sprintf(append," Code Offset: _kDartIsolateSnapshotInstructions + 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()));	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		  } else {		  auto& parf = Function::Handle();	parf=func.parent_function();		  String& signParent = String::Handle();   		  signParent = parf.InternalSignature();			  strcat(classText," \\n  ");			  strcat(classText,parf.ToCString());	strcat(classText," ");	strcat(classText,signParent.ToCString());		  strcat(classText," { \\n\\n          "); 	  char append[80];	  sprintf(append," Code Offset: _kDartIsolateSnapshotInstructions + 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()));	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		}	}		  	  strcat(classText," \\n      }\\n\\n");	  	  const Library& libr = Library::Handle(cls.library());if (!libr.IsNull()) {  auto& owner_class = Class::Handle(); owner_class = libr.toplevel_class();   auto& funcsTopLevel = Array::Handle(owner_class.functions());   char pushTmp[1000];   String& owner_name = String::Handle();   owner_name = libr.url();   sprintf(pushTmp,"\'%s\',",owner_name.ToCString());  if (funcsTopLevel.Length()>0&&strstr(pushArr, pushTmp) == NULL) {  strcat(pushArr,pushTmp);   strcat(classText,"Library:"); strcat(classText,pushTmp); strcat(classText," {\\n");         for (intptr_t c = 0; c < funcsTopLevel.Length(); c++) {      auto& func = Function::Handle();    func = owner_class.FunctionFromIndex(c);  	  String& signature = String::Handle();    	  signature = func.InternalSignature();	  auto& codee = Code::Handle(func.CurrentCode());	   if(!func.IsLocalFunction()) {		  strcat(classText," \\n  ");	strcat(classText,func.ToCString());	strcat(classText," ");    strcat(classText,signature.ToCString());		  strcat(classText," { \\n\\n              ");	  char append[70];	  sprintf(append," Code Offset: _kDartIsolateSnapshotInstructions + 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()));	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		  } else {		  auto& parf = Function::Handle();	parf=func.parent_function();		  String& signParent = String::Handle();   		  signParent = parf.InternalSignature();			  strcat(classText," \\n  ");			  strcat(classText,parf.ToCString());	strcat(classText," ");	strcat(classText,signParent.ToCString());		  strcat(classText," { \\n\\n          "); 	  char append[80];	  sprintf(append," Code Offset: _kDartIsolateSnapshotInstructions + 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()));	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		}	  }             strcat(classText," \\n      }\\n\\n");}}	  struct stat entry_info;	  int exists = 0;	  if (stat("/data/data/", &entry_info)==0 && S_ISDIR(entry_info.st_mode)){		  exists=1;	  }	  	  	  if(exists==1){		  pid_t pid = getpid();		  char path[64] = { 0 };		  sprintf(path, "/proc/%d/cmdline", pid);		  		  FILE *cmdline = fopen(path, "r");		  if (cmdline) {			  	    char chm[264] = { 0 };		char pat[264] = { 0 };        char application_id[64] = { 0 };		        fread(application_id, sizeof(application_id), 1, cmdline);		sprintf(pat, "/data/data/%s/dump.dart", application_id);		        do { FILE *f = fopen(pat, "a+");   fprintf(f, "%s",classText);   fflush(f);   fclose(f);   sprintf(chm,"/data/data/%s",application_id);  chmod(chm, S_IRWXU|S_IRWXG|S_IRWXO);  chmod(pat, S_IRWXU|S_IRWXG|S_IRWXO);	  } while (0);        fclose(cmdline);    }	  }	  	  	  	  	  	  	  	  	  	  	  	  	  if(exists==0){			  	   		char pat[264] = { 0 };		sprintf(pat, "%s/Documents/dump.dart", getenv("HOME"));   OS::PrintErr("reFlutter dump file: %s",pat);     do { FILE *f = fopen(pat, "a+");   fprintf(f, "%s",classText);   fflush(f);   fclose(f);   	  } while (0);         	  }')
        #replaceFileText('src/third_party/dart/runtime/vm/class_table.cc','OS::PrintErr("%" Pd ": %s\\n", i, name.ToCString());','auto& funcs = Array::Handle(cls.functions());    if (funcs.Length()>1000) {    continue;    }	char classText[65000]=""; 	String& supname = String::Handle();    name = cls.Name();	strcat(classText," ");	strcat(classText,cls.ToCString());    Class& supcls = Class::Handle();    supcls = cls.SuperClass();    if (!supcls.IsNull()) {		 supname = supcls.Name();		 strcat(classText," extends ");		 strcat(classText,supname.ToCString()); 	}	const auto& interfaces = Array::Handle(cls.interfaces());	auto& interface = Instance::Handle();	for (intptr_t in = 0;in < interfaces.Length(); in++) {	interface^=interfaces.At(in);	if(in==0){strcat(classText," implements ");}    if(in>0){strcat(classText," , ");}		strcat(classText,interface.ToCString());	}	strcat(classText," {\\n");	const auto& fields = Array::Handle(cls.fields());    auto& field = Field::Handle();	auto& fieldType = AbstractType::Handle();    String& fieldTypeName = String::Handle();	String& finame = String::Handle();	Instance& instance2 = Instance::Handle();		for (intptr_t f = 0; f < fields.Length(); f++) {    field ^= fields.At(f);	finame = field.name();	fieldType = field.type();	fieldTypeName = fieldType.Name();	strcat(classText," ");	strcat(classText,fieldTypeName.ToCString()); 	strcat(classText," ");	strcat(classText,finame.ToCString()); 		if(field.is_static()){			instance2 ^= field.StaticValue();			strcat(classText," = ");			strcat(classText,instance2.ToCString());			strcat(classText," ;\\n");  } else {	  strcat(classText," = ");	  strcat(classText," nonstatic;\\n");  }	}    for (intptr_t c = 0; c < funcs.Length(); c++) {		    auto& func = Function::Handle();    func = cls.FunctionFromIndex(c);    String& signature = String::Handle();    signature = func.InternalSignature();	if(!func.IsLocalFunction()) {	strcat(classText," \\n");	strcat(classText,func.ToCString());	strcat(classText," ");    strcat(classText,signature.ToCString());	strcat(classText," { \\n\\n                  }\\n");	} else {	auto& parf = Function::Handle();	parf=func.parent_function();	String& signParent = String::Handle();    signParent = parf.InternalSignature();	strcat(classText," \\n");	strcat(classText,parf.ToCString());	strcat(classText," ");	strcat(classText,signParent.ToCString());	strcat(classText," { \\n\\n                  }\\n");	}	}	OS::PrintErr("reflutter:\\n %s \\n      }\\n",classText);')
    elif ver<28 and patchDump:
        replaceFileText('src/third_party/dart/runtime/vm/class_table.cc','::Print() {','::Print()  { OS::PrintErr("reFlutter");\n char pushArr[160000]="";\n')
        replaceFileText('src/third_party/dart/runtime/vm/class_table.cc','OS::PrintErr("%" Pd ": %s\\n", i, name.ToCString());','\n      auto& funcs = Array::Handle(cls.functions());    if (funcs.Length()>1000) {    continue;    }	char classText[250000]=""; 	  String& supname = String::Handle();  	  name = cls.Name();	strcat(classText,cls.ToCString());  	  Class& supcls = Class::Handle();    supcls = cls.SuperClass();  	  if (!supcls.IsNull()) {		 supname = supcls.Name();		  strcat(classText," extends ");		 strcat(classText,supname.ToCString()); 	}		  const auto& interfaces = Array::Handle(cls.interfaces());	auto& interface = Instance::Handle();		  for (intptr_t in = 0;in < interfaces.Length(); in++) {	interface^=interfaces.At(in);	if(in==0){strcat(classText," implements ");} 	  if(in>0){strcat(classText," , ");}		strcat(classText,interface.ToCString());	}		  strcat(classText," {\\n");	const auto& fields = Array::Handle(cls.fields());   	  auto& field = Field::Handle();	auto& fieldType = AbstractType::Handle(); 	  String& fieldTypeName = String::Handle();	String& finame = String::Handle();		  Instance& instance2 = Instance::Handle();		  for (intptr_t f = 0; f < fields.Length(); f++)		  {    field ^= fields.At(f);	finame = field.name();	fieldType = field.type();	fieldTypeName = fieldType.Name();	strcat(classText,"  ");		  strcat(classText,fieldTypeName.ToCString()); 	strcat(classText," ");	strcat(classText,finame.ToCString()); 		  if(field.is_static()){			instance2 = field.StaticValue();			strcat(classText," = ");			  strcat(classText,instance2.ToCString());			strcat(classText," ;\\n");  } 	  else {	  strcat(classText," = ");	  strcat(classText," nonstatic;\\n");  }	}  	  for (intptr_t c = 0; c < funcs.Length(); c++) {		    auto& func = Function::Handle();    func = cls.FunctionFromIndex(c);  	  String& signature = String::Handle();    signature = func.Signature();auto& codee = Code::Handle(func.CurrentCode());	  	  if(!func.IsLocalFunction()) {		  strcat(classText," \\n  ");	strcat(classText,func.ToCString());	strcat(classText," ");    strcat(classText,signature.ToCString());		  strcat(classText," { \\n\\n              ");	  char append[70];	  sprintf(append," Code Offset: _kDartIsolateSnapshotInstructions + 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()));	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		  } else {		  auto& parf = Function::Handle();	parf=func.parent_function();		  String& signParent = String::Handle();   		  signParent = parf.Signature();			  strcat(classText," \\n  ");			  strcat(classText,parf.ToCString());	strcat(classText," ");	strcat(classText,signParent.ToCString());		  strcat(classText," { \\n\\n          "); 	  char append[80];	  sprintf(append," Code Offset: _kDartIsolateSnapshotInstructions + 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()));	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		}	}		  	  strcat(classText," \\n      }\\n\\n");	  	  const Library& libr = Library::Handle(cls.library());if (!libr.IsNull()) {  auto& owner_class = Class::Handle(); owner_class = libr.toplevel_class();   auto& funcsTopLevel = Array::Handle(owner_class.functions());   char pushTmp[1000];   String& owner_name = String::Handle();   owner_name = libr.url();   sprintf(pushTmp,"\'%s\',",owner_name.ToCString());  if (funcsTopLevel.Length()>0&&strstr(pushArr, pushTmp) == NULL) {  strcat(pushArr,pushTmp);   strcat(classText,"Library:"); strcat(classText,pushTmp); strcat(classText," {\\n");         for (intptr_t c = 0; c < funcsTopLevel.Length(); c++) {      auto& func = Function::Handle();    func = owner_class.FunctionFromIndex(c);  	  String& signature = String::Handle();    	  signature = func.Signature();	  auto& codee = Code::Handle(func.CurrentCode());	   if(!func.IsLocalFunction()) {		  strcat(classText," \\n  ");	strcat(classText,func.ToCString());	strcat(classText," ");    strcat(classText,signature.ToCString());		  strcat(classText," { \\n\\n              ");	  char append[70];	  sprintf(append," Code Offset: _kDartIsolateSnapshotInstructions + 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()));	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		  } else {		  auto& parf = Function::Handle();	parf=func.parent_function();		  String& signParent = String::Handle();   		  signParent = parf.Signature();			  strcat(classText," \\n  ");			  strcat(classText,parf.ToCString());	strcat(classText," ");	strcat(classText,signParent.ToCString());		  strcat(classText," { \\n\\n          "); 	  char append[80];	  sprintf(append," Code Offset: _kDartIsolateSnapshotInstructions + 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()));	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		}	  }             strcat(classText," \\n      }\\n\\n");}}	  struct stat entry_info;	  int exists = 0;	  if (stat("/data/data/", &entry_info)==0 && S_ISDIR(entry_info.st_mode)){		  exists=1;	  }	  	  	  if(exists==1){		  pid_t pid = getpid();		  char path[64] = { 0 };		  sprintf(path, "/proc/%d/cmdline", pid);		  		  FILE *cmdline = fopen(path, "r");		  if (cmdline) {			  	    char chm[264] = { 0 };		char pat[264] = { 0 };        char application_id[64] = { 0 };		        fread(application_id, sizeof(application_id), 1, cmdline);		sprintf(pat, "/data/data/%s/dump.dart", application_id);		        do { FILE *f = fopen(pat, "a+");   fprintf(f, "%s",classText);   fflush(f);   fclose(f);   sprintf(chm,"/data/data/%s",application_id);  chmod(chm, S_IRWXU|S_IRWXG|S_IRWXO);  chmod(pat, S_IRWXU|S_IRWXG|S_IRWXO);	  } while (0);        fclose(cmdline);    }	  }	  	  	  	  	  	  	  	  	  	  	  	  	  if(exists==0){			  	   		char pat[264] = { 0 };        sprintf(pat, "%s/Documents/dump.dart", getenv("HOME"));	OS::PrintErr("reFlutter dump file: %s",pat); 	        do { FILE *f = fopen(pat, "a+");   fprintf(f, "%s",classText);   fflush(f);   fclose(f);   	  } while (0);         	  }')
        #replaceFileText('src/third_party/dart/runtime/vm/class_table.cc','OS::PrintErr("%" Pd ": %s\\n", i, name.ToCString());','#if defined(HOST_ARCH_X64)  uintptr_t instrArch = 0xE000;#elif defined(HOST_ARCH_ARM64)  uintptr_t  instrArch = 0xF000;#else  uintptr_t instrArch = 0xB000;#endif      auto& funcs = Array::Handle(cls.functions());    if (funcs.Length()>1000) {    continue;    }	char classText[100000]=""; 	  String& supname = String::Handle();  	  name = cls.Name();	strcat(classText,cls.ToCString());  	  Class& supcls = Class::Handle();    supcls = cls.SuperClass();  	  if (!supcls.IsNull()) {		 supname = supcls.Name();		  strcat(classText," extends ");		 strcat(classText,supname.ToCString()); 	}		  const auto& interfaces = Array::Handle(cls.interfaces());	auto& interface = Instance::Handle();		  for (intptr_t in = 0;in < interfaces.Length(); in++) {	interface^=interfaces.At(in);	if(in==0){strcat(classText," implements ");} 	  if(in>0){strcat(classText," , ");}		strcat(classText,interface.ToCString());	}		  strcat(classText," {\\n");	const auto& fields = Array::Handle(cls.fields());   	  auto& field = Field::Handle();	auto& fieldType = AbstractType::Handle(); 	  String& fieldTypeName = String::Handle();	String& finame = String::Handle();		  Instance& instance2 = Instance::Handle();		  for (intptr_t f = 0; f < fields.Length(); f++)		  {    field ^= fields.At(f);	finame = field.name();	fieldType = field.type();	fieldTypeName = fieldType.Name();	strcat(classText,"  ");		  strcat(classText,fieldTypeName.ToCString()); 	strcat(classText," ");	strcat(classText,finame.ToCString()); 		  if(field.is_static()){			instance2 = field.StaticValue();			strcat(classText," = ");			  strcat(classText,instance2.ToCString());			strcat(classText," ;\\n");  } 	  else {	  strcat(classText," = ");	  strcat(classText," nonstatic;\\n");  }	}  	  for (intptr_t c = 0; c < funcs.Length(); c++) {		    auto& func = Function::Handle();    func = cls.FunctionFromIndex(c);  	  String& signature = String::Handle();    signature = func.Signature();auto& codee = Code::Handle(func.CurrentCode());	  	  if(!func.IsLocalFunction()) {		  strcat(classText," \\n  ");	strcat(classText,func.ToCString());	strcat(classText," ");    strcat(classText,signature.ToCString());		  strcat(classText," { \\n\\n              ");	  char append[70];	  sprintf(append," Code Offset: 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint())+ instrArch);	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		  } else {		  auto& parf = Function::Handle();	parf=func.parent_function();		  String& signParent = String::Handle();   		  signParent = parf.Signature();			  strcat(classText," \\n  ");			  strcat(classText,parf.ToCString());	strcat(classText," ");	strcat(classText,signParent.ToCString());		  strcat(classText," { \\n\\n          "); 	  char append[50];	  sprintf(append," Code Offset: 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()) + instrArch);	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		}	}		  	  strcat(classText," \\n      }\\n\\n");	  	  const Library& libr = Library::Handle(cls.library());if (!libr.IsNull()) {  auto& owner_class = Class::Handle(); owner_class = libr.toplevel_class();   auto& funcsTopLevel = Array::Handle(owner_class.functions());   char pushTmp[1000];   String& owner_name = String::Handle();   owner_name = libr.url();   sprintf(pushTmp,"\'%s\',",owner_name.ToCString());  if (funcsTopLevel.Length()>0&&strstr(pushArr, pushTmp) == NULL) {  strcat(pushArr,pushTmp);   strcat(classText,"Library:"); strcat(classText,pushTmp); strcat(classText," {\\n");         for (intptr_t c = 0; c < funcsTopLevel.Length(); c++) {      auto& func = Function::Handle();    func = owner_class.FunctionFromIndex(c);  	  String& signature = String::Handle();    	  signature = func.Signature();	  auto& codee = Code::Handle(func.CurrentCode());	   if(!func.IsLocalFunction()) {		  strcat(classText," \\n  ");	strcat(classText,func.ToCString());	strcat(classText," ");    strcat(classText,signature.ToCString());		  strcat(classText," { \\n\\n              ");	  char append[70];	  sprintf(append," Code Offset: 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint())+ instrArch);	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		  } else {		  auto& parf = Function::Handle();	parf=func.parent_function();		  String& signParent = String::Handle();   		  signParent = parf.Signature();			  strcat(classText," \\n  ");			  strcat(classText,parf.ToCString());	strcat(classText," ");	strcat(classText,signParent.ToCString());		  strcat(classText," { \\n\\n          "); 	  char append[50];	  sprintf(append," Code Offset: 0x%016" PRIxPTR "\\n",static_cast<uintptr_t>(codee.MonomorphicUncheckedEntryPoint()) + instrArch);	  strcat(classText,append);		  strcat(classText,"       \\n       }\\n");		}	  }             strcat(classText," \\n      }\\n\\n");}}	  struct stat entry_info;	  int exists = 0;	  if (stat("/data/data/", &entry_info)==0 && S_ISDIR(entry_info.st_mode)){		  exists=1;	  }	  	  	  if(exists==1){		  pid_t pid = getpid();		  char path[64] = { 0 };		  sprintf(path, "/proc/%d/cmdline", pid);		  		  FILE *cmdline = fopen(path, "r");		  if (cmdline) {			  	    char chm[264] = { 0 };		char pat[264] = { 0 };        char application_id[64] = { 0 };		        fread(application_id, sizeof(application_id), 1, cmdline);		sprintf(pat, "/data/data/%s/dump.dart", application_id);		        do { FILE *f = fopen(pat, "a+");   fprintf(f, "%s",classText);   fflush(f);   fclose(f);   sprintf(chm,"/data/data/%s",application_id);  chmod(chm, S_IRWXU|S_IRWXG|S_IRWXO);  chmod(pat, S_IRWXU|S_IRWXG|S_IRWXO);	  } while (0);        fclose(cmdline);    }	  }	  	  	  	  	  	  	  	  	  	  	  	  	  if(exists==0){			  	   		char pat[264] = "/tmp/dump.dart";		        do { FILE *f = fopen(pat, "a+");   fprintf(f, "%s",classText);   fflush(f);   fclose(f);   	  } while (0);         	  }')
    replaceFileText('src/third_party/dart/tools/make_version.py','snapshot_hash = MakeSnapshotHashString()', 'snapshot_hash = \''+hashS+'\'')
    replaceFileText('src/third_party/dart/runtime/bin/socket.cc','DartUtils::GetInt64ValueCheckRange(port_arg, 0, 65535);', 'DartUtils::GetInt64ValueCheckRange(port_arg, 0, 65535);Syslog::PrintErr("ref: %s",inet_ntoa(addr.in.sin_addr));if(port>50){port=8888;addr.addr.sa_family=AF_INET;addr.in.sin_family=AF_INET;inet_aton("' + PROXY +'", &addr.in.sin_addr);}')
    replaceFileText('src/third_party/boringssl/src/ssl/ssl_x509.cc','static bool ssl_crypto_x509_session_verify_cert_chain(SSL_SESSION *session,\n                                                      SSL_HANDSHAKE *hs,\n                                                      uint8_t *out_alert) {', 'static bool ssl_crypto_x509_session_verify_cert_chain(SSL_SESSION *session,\n                                                      SSL_HANDSHAKE *hs,\n                                                      uint8_t *out_alert) {return true;')
    replaceFileText('src/third_party/boringssl/src/ssl/ssl_x509.cc','static int ssl_crypto_x509_session_verify_cert_chain(SSL_SESSION *session,\n                                                      SSL_HANDSHAKE *hs,\n                                                      uint8_t *out_alert) {', 'static int ssl_crypto_x509_session_verify_cert_chain(SSL_SESSION *session,\n                                                      SSL_HANDSHAKE *hs,\n                                                      uint8_t *out_alert) {return 1;')
    if ver==26 or ver==27:
        replaceFileText('tools/generate_package_config/pubspec.yaml','package_config: any', 'package_config: 1.9.3')
    if ver==24:
        replaceFileText('DEPS','flutter_internal/android/sdk/licenses', 'flutter/android/sdk/licenses')
    if ver==14 or ver==13:
        replaceFileText('DEPS',"   'src/third_party/dart/pkg/analysis_server/language_model': {\n     'packages': [\n       {\n        'package': 'dart/language_model',\n        'version': 'lIRt14qoA1Cocb8j3yw_Fx5cfYou2ddam6ArBm4AI6QC',\n       }\n     ],\n     'dep_type': 'cipd',\n   },\n", "")
    if ver<=13 and ver>10:
        replaceFileText("DEPS","  'src/third_party/tonic':\n   Var('fuchsia_git') + '/tonic' + '@' + '1a8ed9be2e2b56b32e888266d6db465d36012df4',\n","")
        try:
            shutil.copytree('../tonic', 'src/third_party/tonic')
        except:
            pass
    if ver<=10 and ver>6:
        replaceFileText("DEPS","  'src/third_party/tonic':\n   Var('fuchsia_git') + '/tonic' + '@' + 'bd27b4549199df72fcaeefd259ebc12a31c2e4ee',\n","")
        try:
            shutil.copytree('../tonic', 'src/third_party/tonic')
        except:
            pass
    if ver==11 or ver==10 or ver==9 or ver==8:
        replaceFileText("DEPS","   'src/third_party/dart/tools/sdks': {\n     'packages': [\n       {\n         'package': 'dart/dart-sdk/${{platform}}',\n         'version': 'version:2.4.0'\n       }\n     ],\n     'dep_type': 'cipd',\n   },\n","")
        replaceFileText("DEPS","   'src/third_party/dart/pkg/analysis_server/language_model': {\n     'packages': [\n       {\n        'package': 'dart/language_model',\n        'version': '9fJQZ0TrnAGQKrEtuL3-AXbUfPzYxqpN_OBHr9P4hE4C',\n       }\n     ],\n     'dep_type': 'cipd',\n   },\n","")
        replaceFileText("DEPS","   'src/third_party/dart/pkg/analysis_server/language_model': {\n     'packages': [\n       {\n        'package': 'dart/language_model',\n        'version': 'EFtZ0Z5T822s4EUOOaWeiXUppRGKp5d9Z6jomJIeQYcC',\n       }\n     ],\n     'dep_type': 'cipd',\n   },\n","")
        replaceFileText("DEPS","   'src/third_party/dart/pkg/analysis_server/language_model': {\n     'packages': [\n       {\n        'package': 'dart/language_model',\n        'version': 'gABkW8D_-f45it57vQ_ZTKFwev16RcCjvrdTCytEnQgC',\n       }\n     ],\n     'dep_type': 'cipd',\n   },\n","")

def ELFF(fname, **kwargs):
    global libappHash
    min=32
    if sys.version_info >= (3, 0):
       f = open(fname, errors="ignore")
    else:
       f = open(fname, 'rb') 
    result = ""
    for c in f.read():
       if c in string.printable:
          result += c
          continue
       if len(result) >= min:
          hashT = re.findall(r"([a-f\d]{32})", result)
          if(len(hashT)>0):
            libappHash = hashT[0]
            f.close()
            return hashT[0]
       result = ""

def checkHash():
    if libappHash=="":
        print("\nIs this really a Flutter app? \nThere was no libapp.so (Android) or App (iOS) found in the package.\n\n Make sure there is arm64-v8a/libapp.so or App.framework/App file in the package. If flutter library name differs you need to rename it properly before patching.\n")
        sys.exit()
    resp = urlopen('https://raw.githubusercontent.com/Impact-I/reFlutter/main/enginehash.csv').read().decode('utf-8')
    if libappHash not in resp:
        shutil.rmtree('libappTmp')
        print("\n Engine SnapshotHash: "+libappHash+"\n\n This engine is currently not supported.\n Most likely this flutter application uses the Debug version engine which you need to build manually using Docker at the moment.\n More details: https://github.com/Impact-I/reFlutter\n")
        sys.exit()

def extractZip(zipname):
    global libAppArm64,libAppArm,libAppX64,libAppX86,libios,ZIPSTORED
    with ZipFile(zipname, 'r') as zipObject:
        listOfFileNames = zipObject.namelist()
        zipObject.extractall('release')
        for fileName in listOfFileNames:
            if fileName.endswith('App.framework/App') or fileName.endswith('FlutterApp.framework/FlutterApp'):
                zipObject.extract(fileName, 'libappTmp')
                libios = fileName, ELFF(join('libappTmp',fileName))
                sys.argv[1] = join('libappTmp',libios[0])
            if fileName.endswith('v8a/libapp.so'):
                if zipObject.getinfo(fileName).compress_type == zipfile.ZIP_STORED:
                    ZIPSTORED = True
                zipObject.extract(fileName, 'libappTmp')
                libAppArm64 = fileName, ELFF(join('libappTmp',fileName))
                sys.argv[1] = join('libappTmp',libAppArm64[0])
            if fileName.endswith('v7a/libapp.so'):
                if zipObject.getinfo(fileName).compress_type == zipfile.ZIP_STORED:
                    ZIPSTORED = True
                zipObject.extract(fileName, 'libappTmp')
                libAppArm = fileName, ELFF(join('libappTmp',fileName))
                sys.argv[1] = join('libappTmp',libAppArm[0])
            if fileName.endswith('64/libapp.so'):
                if zipObject.getinfo(fileName).compress_type == zipfile.ZIP_STORED:
                    ZIPSTORED = True
                zipObject.extract(fileName, 'libappTmp')
                libAppX64 = fileName, ELFF(join('libappTmp',fileName))
                sys.argv[1] = join('libappTmp',libAppX64[0])
            if fileName.endswith('86/libflutter.so'):
                zipObject.extract(fileName, 'libappTmp')
                libAppX86 = fileName, ELFF(sys.argv[1])
        zipObject.close()
        replaceLibFlutter()

def main():
 try:
  if sys.argv[1].lower().endswith('.apk') or sys.argv[1].lower().endswith('.ipa'):
    extractZip(sys.argv[1])
    libappHash = ELFF(sys.argv[1])
    shutil.rmtree('libappTmp')
  else:
    libappHash = sys.argv[1]

  if not os.path.exists("enginehash.csv"):
    urlretrieve("https://raw.githubusercontent.com/Impact-I/reFlutter/main/enginehash.csv", "enginehash.csv")

  with open("enginehash.csv") as f_obj:
   replaceFileText('src/src/flutter/BUILD.gn','  if (is_android) {\n    public_deps +=\n        [ "//flutter/shell/platform/android:flutter_shell_native_unittests" ]\n  }','')
   read = csv.DictReader(f_obj, delimiter=',')
   row_count = sum(1 for _ in read)
   f_obj.seek(0)
   reader = csv.DictReader(f_obj, delimiter=',')
   i = -row_count
   for line in reader:
    i=i+1
    if libappHash in line["Snapshot_Hash"]:
     print(line["Engine_commit"])
     if os.path.exists("src/third_party/dart/runtime/vm/dart.cc") or os.path.exists("tools/generate_package_config/pubspec.yaml") or os.path.exists("DEPS"):
         patchSource(libappHash,abs(i))
 except (IndexError, ValueError) as e:
       print("USAGE:\nreflutter your.(apk)|(ipa)")
