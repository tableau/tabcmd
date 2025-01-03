#!/bin/bash

# Pyinstaller bundles cannot be run by double-clicking them
# https://github.com/pyinstaller/pyinstaller/issues/5154#issuecomment-2508011279
APP_NAME="tabcmd"

cd dist/$APP_NAME.app/Contents/MacOS
mv $APP_NAME ${APP_NAME}_cli

cat << EOF > $APP_NAME
#!/bin/bash
# This is the launcher for OSX, this way the app will be opened
# when you double click it from the apps folder
open -n /Applications/${APP_NAME}.app/Contents/MacOS/${APP_NAME}_cli
EOF

chmod +x $APP_NAME
      
