
# Helper file for building assets. If run on its own creates an asset watchdog.

# Import Python modules.
import os
import sys
import time
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import SCSS parser and compressor.
import sass

# Import Javascript minifier.
from jsmin import jsmin

# Script directory.
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

# Specifiy constants for the file paths.
SCSS_PATH = "{}/assets/scss/".format(ROOT_PATH)
CSS_PATH = "{}/static/css/".format(ROOT_PATH)

JS_PATH = "{}/assets/js/".format(ROOT_PATH)
MINJS_PATH = "{}/static/js/".format(ROOT_PATH)


def build_scss(filename):
    # Create the output CSS directory if it doesn't exist.
    if not os.path.exists(os.path.dirname(CSS_PATH)):
        try:
            os.makedirs(os.path.dirname(CSS_PATH))

        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise

    # Get the full paths to the files.
    srcpath = os.path.join(SCSS_PATH, filename)
    outpath = "{}{}.css".format(CSS_PATH, os.path.splitext(filename)[0])

    # Generate the output CSS.
    try:
        output = sass.compile(
            string=open(srcpath, "r", encoding="utf-8").read(),
            output_style="compressed"
        )

    except sass.CompileError as e:
        print("{}SCSS build failed: Please fix the shown error to continue.".format(e))

        return

    # Write the output CSS to the correct path.
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(output)

    print("SCSS built: {} -> {}".format(srcpath, outpath))


def build_js(filename):
    # Create the output minified Javascript directory if it doesn't exist.
    if not os.path.exists(os.path.dirname(MINJS_PATH)):
        try:
            os.makedirs(os.path.dirname(MINJS_PATH))

        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise

    # Get the full paths to the files.
    srcpath = os.path.join(JS_PATH, filename)
    outpath = "{}{}.js".format(MINJS_PATH, os.path.splitext(filename)[0])

    # Generate the output minified Javascript.
    output = jsmin(
        open(srcpath, "r", encoding="utf-8").read(),
        quote_chars="'\"`"
    )

    # Write the output Javascript to the correct path.
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(output)

    print("MINJS built: {} -> {}".format(srcpath, outpath))


def build_assets():
    # Compress source files beforehand and move them to the static directory.
    print("Building SCSS source files...")

    # Iterate over SCSS source files.
    for filename in os.listdir(SCSS_PATH):
        if filename.endswith(".scss"):
            # Build the CSS file from the detected SCSS file.
            build_scss(filename)

            continue

        else:
            continue

    print("Building minified Javascript files...")

    # Iterate over JS source files.
    for filename in os.listdir(JS_PATH):
        if filename.endswith(".js"):
            # Build the minified Javascript file from the detected JS file.
            build_js(filename)

            continue

        else:
            continue


class SCSSHandler(FileSystemEventHandler):

    def on_modified(self, event):
        filename = os.path.basename(event.src_path)

        print("\n{} - Detected a change in '{}'.".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename))

        # Rebuild the detected file.
        build_scss(filename)


class JSHandler(FileSystemEventHandler):

    def on_modified(self, event):
        filename = os.path.basename(event.src_path)

        print("\n{} - Detected a change in '{}'.".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename))

        # Rebuild the detected file.
        build_js(filename)


if __name__ == "__main__":
    # Build all our assets for use in the application.
    build_assets()

    # Setup a watchdog for the build asset directories.
    scss_handler = SCSSHandler()
    js_handler = JSHandler()

    observer = Observer()
    observer.schedule(scss_handler, SCSS_PATH, recursive=False)
    observer.schedule(js_handler, JS_PATH, recursive=False)
    observer.start()

    print("\nStarted watchdog for '{}*' & '{}*'.".format(SCSS_PATH, JS_PATH))

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
