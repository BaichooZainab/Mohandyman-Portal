from webappfiles import create_app
app = create_app()
# the if statement is used to prevent other scripts from running
# run your server and allow errors to be shown on the page
# after publishing the app, you can remove the debug=true
# everytime you make a change in the main.py file, the webserver will automatically rerun
if __name__ == "__main__":
    app.run(debug=True)
