#SETTINGS: STORE ANY NEEDED (CUSTOMIZABLE) DATA REGARDING THE PROJECT HERE


#ROOT_URL
ROOT_URL = 'http://10.1.1.50:8000/'

#List of DJANGO APPS
DJANGO_APPS = (
    "users",
    "shows",
    "assets",
    "versions",
    "movies",
    "images",
    "companies",
    "renders",
    "renderfarm",
    "nodes",
    )

    
#List of urls based on the urlpattern from django. 
#Must edit it yourself.
    
URLS = {
    "api/" : (
        "users",
        "preferences",
        "show",
        "assets",
        "versions",
        "movies",
        "images",
        "companies",
        "layer",
        "render",
        "renderfarm",
        "action",
        "camera",
        "group",
        "material",
        "scene",
        "world",
        ),
    }
    
               
