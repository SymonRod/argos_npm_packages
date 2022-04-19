# Argos npm packages versions
This [Argos](https://github.com/p-e-w/argos) plugin is used to keep track of npm
packages version and will notify you if a new version is released.

## Requirements
- npm
- python3
- pip3

## Setup

- Pyton install requirements
    ``` bash
        pip3 install -r requirements.txt
    ```
- Change the db_path in the files "npmVersions.c.5m+.py" and "db.py"
- Change the file_path in "npmVersions.c.5m+.py"
- Create a symlink to the "npmVersions.c.5m+.py" file and making it executable
    ``` bash 
        ln -s $HOME/.config/argos/npmVersions.c.5m+.py ./npmVersions.c.5m+.py
        chmox +x $HOME/.config/argos/npmVersions.c.5m+.py
    ```
- Making "getVersionFromNpm.py" executable
    ``` bash
    chmod +x ./getVersionFromNpm.py
   ```
- Adding a crontab to update the db every n minutes or 1 a day [Crontab guru](https://crontab.guru/)
    ``` bash
        crontab -e
        
        # Every hour
        0 * * * * {this repo folder}/getVersionFromNpm.py

        # At startup
        @reboot {this repo folder}/getVersionFromNpm.py
    ```




## Adding the plugin to argos
    
I advice to create a symlink to file and not to copy the plugin directly in the "~/.config/argos" folder
The file to link is "npmVersions.c.5m+.py"

## Adding a package
To add a package to the "watch list" you need to:
``` bash
    python3 add_package.py
```



