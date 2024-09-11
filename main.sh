python3 src/main.py

if [ -d "static" ]; then
    # Copy all files and subdirectories from static to public
    cp -r static/* public/
    echo "All files copied from static to public."
else
    echo "Source directory 'static' does not exist."
fi


cd public && python3 -m http.server 8888