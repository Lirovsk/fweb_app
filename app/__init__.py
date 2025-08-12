from flask import (Flask,
    render_template,
    request)
from .Engines.GeneralServices import insp_default_storage, create_default_storage
from pathlib import Path
from .paths import ROOM_PATH   

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= 'd8ce56cfafc6ad45885929686e2701fc1b594f39390621b3af6beae02eb1218a',
    )

    #this ensures the database storage is created
    inspect = insp_default_storage()
    if inspect["trial"] == False:
        print(f"Error inspecting default storage: {inspect['message']}")
    else:
        if 'engine_storage' in inspect["tables"]:
            print("Default storage already exists.")
            
        if 'engine_storage' not in inspect["tables"]:
            try:
                create_default_storage()
                print("Default storage created successfully.")
                
            except Exception as e:
                print(f"Error creating default storage: {e}")
    
    #this ensures the path to the directory exists
    if ROOM_PATH.exists(): #check if the rooms directory exists
        pass    
    else:
        ROOM_PATH.mkdir(parents=True, exist_ok=True) #create the directory in case it doesn't exist


    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
        
    #import the auth blueprint
    from . import auth_create
    app.register_blueprint(auth_create.bp)
    
    from . import room
    app.register_blueprint(room.bp)
    
    @app.route("/")
    def index():
        return render_template('index.html')
    
    return app
