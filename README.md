# MagicDot
A set of rootkit-like abilities for unprivileged users, and vulnerabilities based on the DOT-to-NT path conversion known issue

<div align="center">
<img src="./images/magician-w-md-logo-KO-white.png" width="50%"/>
</div align="center">

## MagicDot Python Package
Implements MagicDot's rootkit-like techniques:
* Files/Directories named only with dots
  * Bonus - Such Directories prevent any shadow copy restoration of any parent directory of the inoperable directory
* Inoperable Files/Directories
* Impersonated Files/Directories
* Impersonated Process
* Process Explorer DoS Vulnerability - `CVE-2023-42757`
* Hidden files in ZIP archives

### MagicDot Python Package Installation
1. Clone the repo
2. Install it locally:
```
pip install <cloned repo path>
```

## MagicDot Tools
Inside the `tools` folder you'll find the `magic_dot_cli` tool (dependent on the MagicDot Python package) along with 3 different solo scripts that implement the exploits for vulnerabilities `CVE-2023-36396`, `CVE-2023-32054`, and a third unfixed Deletion EoP vulnerability. During the installation of the MagicDot Python package, the requirements for these scripts are installed as well.

For convenience purposes, it is recommended to pack magic_dot_cli into an executable using Pyinstaller:
```
cd tools\magic_dot_cli\
pyinstaller --onefile magic_dot_cli.py
```

### magic_dot_cli Usage
```
python .\magic_dot_cli.py -h
usage: magic_dot_cli.py [-h]
                        {CREATE_IMPERSONATED_PROCESS,CREATE_INOPERABLE_FILE,CREATE_INOPERABLE_DIR,CREATE_DOTS_FILE,CREATE_DOTS_DIR,CREATE_IMPERSONATED_FILE,CREATE_IMPERSONATED_DIR,ADD_INVISIBLE_FILE_INTO_ZIP,DISABLE_PROCEXP}
                        ...

An unprivileged rootkit-like tool

optional arguments:
  -h, --help            show this help message and exit

command:
  {CREATE_IMPERSONATED_PROCESS,CREATE_INOPERABLE_FILE,CREATE_INOPERABLE_DIR,CREATE_DOTS_FILE,CREATE_DOTS_DIR,CREATE_IMPERSONATED_FILE,CREATE_IMPERSONATED_DIR,ADD_INVISIBLE_FILE_INTO_ZIP,DISABLE_PROCEXP}
    CREATE_IMPERSONATED_PROCESS
                        Create a process that impersonates a different process. Both Task Manager and Process Explorer will display    
                        information about the target process to impersonate to
    CREATE_INOPERABLE_FILE
                        Create an inoperable file
    CREATE_INOPERABLE_DIR
                        Create an inoperable directory
    CREATE_DOTS_FILE    Create a dots file
    CREATE_DOTS_DIR     Create a dots directory
    CREATE_IMPERSONATED_FILE
                        Create a file that impersonates a different file
    CREATE_IMPERSONATED_DIR
                        Create a directory that impersonates a different directory
    ADD_INVISIBLE_FILE_INTO_ZIP
                        Inserts a file into a zip. The file is inserted with a name that prevents Windows' ZIP archiver from being     
                        able to list it in the ZIP.
    DISABLE_PROCEXP     Exploits a DOS vulnerability in ProcExp. Creates a process that runs forever and does nothing. The process     
                        has a certain name that crashes ProcExp whenever it runs. Valid against all ProcExp versions under version     
                        17.04 (released in April 3rd 2023).
```

For more help per each command use `-h` for the specific command. For Example:
```
python magic_dot_cli.py CREATE_IMPERSONATED_PROCESS -h
```

### prepare_archive_rce_exploit Usage (CVE-2023-36396)
```
python prepare_archive_rce_exploit.py -h
usage: prepare_archive_rce_exploit.py [-h] [--target-dir-relative TARGET_DIR_RELATIVE]
                                      files_to_write_paths [files_to_write_paths ...]     
                                      out_archive_path

Exploits CVE-2023-36396. Crafts a malicious archive that exploits Windows File Explorer   
to extract a file to an arbitrary relative path. The default relative path is set to      
point from the Downloads directory to the user's Startup folder

positional arguments:
  files_to_write_paths  File paths separated by spaces. These files are the files which   
                        will be written to the chosen victim's directory
  out_archive_path      Path to the archive to be created that will contain the exploit.  
                        the type of the archive will be determined based on the file      
                        extension provided. Supported types: .tar|.tar.gz|.tar.gzip|.tar  
                        .xz|.tar.bz2|.tar.bzip2|.tar.zst|.tar.zstd|.7z|.7zip

optional arguments:
  -h, --help            show this help message and exit
  --target-dir-relative TARGET_DIR_RELATIVE
                        A relative path from the victim's estimated extraction folder to  
                        the destination folder of the executables
```

### prepare_shadow_copy_restoration_write_exploit Usage (CVE-2023-32054)
```
python .\prepare_shadow_copy_restoration_write_exploit.py -h
usage: prepare_shadow_copy_restoration_write_exploit.py [-h] -target-dir TARGET_DIR
                                                        (-replacing-dir REPLACING_DIR | -remove-dir)

Exploits CVE-2023-32054

optional arguments:
  -h, --help            show this help message and exit
  -target-dir TARGET_DIR
                        The target directory to try to overwrite its files. The
                        directory is vulnerable if an unprivileged user is allowed to
                        create a new directory its parent directory
  -replacing-dir REPLACING_DIR
                        The directory that contains files with the same names in the
                        same structure of the target dir but with the new desired
                        content
  -remove-dir           Delete the directory created a part of the exploit in an       
                        earlier point in time. This is recommended to be done after a  
                        shadow copy was taken by an admin, while the directory
                        existed
```

### prepare_delete_dir_exploit Usage
```
python prepare_delete_dir_exploit.py -h
usage: prepare_delete_dir_exploit.py [-h] target_dir

Exploits a "won't fixed" deletion EoP vulnerability triggered by a privileged user
interaction. Creates a directory called "... " in a target directory to delete. When      
"... " is deleted, then its parent directory is deleted too.

positional arguments:
  target_dir  The target directory to try to delete. It is vulnerable only if you can     
              create a directory inside it.

optional arguments:
  -h, --help  show this help message and exit
```

