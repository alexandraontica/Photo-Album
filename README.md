# Photo Management Web App

To start the Flask server of the app (*app.py*), run the following commands in the root directory:

`docker build -t iap1-tema .`

`docker run -p 5000:5000 -it iap1-tema`

***To log in as administrator, use the following credentials:***

Username: **felix_motanul**

Password: **miau123!**

## Docker Container
The Dockerfile sets up an Alpine Linux environment with Python 3 installed.

The base image it builds upon is Alpine Linux, specifically the edge version. It installs Python 3 and pip using Alpine's package manager `apk`, creates a Python virtual environment named `venv` in the root directory, copies all files and directories from the current directory from the host machine to the `/usr/src/app/` directory inside the Docker container, installing the Python dependencies, exposes port **5000** and then runs the command `python3 /usr/src/app/app.py`, which starts the application.

## Frontend
All pages are based on the Jinja2 template from **base.html**, which links the CSS stylesheet **style.css**, the Bootstrap CSS framework stylesheet and the  Bootstrap JavaScript bundle from a CDN (Content Delivery Network). 
Each page has a header (a navigation bar) and a main part where the content is displayed.

**To be noted that I tried to make the application responsive using CSS. :)**

### Navigation Bar
The navbar is entirely created using Bootstrap. Based on whether the administrator is logged in or not, the navbar displays different links.

When the admin is authenticated, the admin can navigate between the home page (the gallery), the photo upload form, and the *About Me* page and can also log out.

Any other user can only navigate between the home page, the *About Me* page, and the login form.

### Home Page (Photo Gallery)
Using Jinja2, the home page displays each category name and the corresponding pictures.

When the admin is logged in and clicks on a thumbnail, the whole picture is displayed. To achieve this, I remove the *.thumb* from the picture's name and send the request to the backend of the app.

### "About Me" Page
Here I used Bootstrap to display the elements in two columns: the paragraph on the left and two pictures on the right. When the user hovers over a picture, its size will increase.

### Login and Upload
The login form has two fields, username and password.
Upon submission of the form, it will post the data to the `/login` route.
An error message is displayed when the credentials are incorrect.

The upload form includes fields for selecting an image file, optionally entering a name, and selecting a category (there are 4 categories available).

If the user is not authenticated as administrator, the upload form will not be displayed.

## Backend
### Libraries used:
- **Flask**
- **render_template**
- **request**
- **redirect**
- **os**
- **url_for**:  used for URL generation.
- **session**: used to manage user sessions.
- **send_from_directory**: used to send files from a directory.
- **secrets**: module used to generate strong random numbers for managing session keys.
- **re**: module for regular expressions.
- **PIL (Python Imaging Library)**: used for image processing.

### Routes:
- **home**: Renders the home page (**'/'**). It retrieves thumbnail images from the specified upload directory and displays them on the page.

- **uploaded_file**: Serves uploaded files from the specified upload directory (**'/upload/< path:filename >'**).

- **aboutme**: Renders the *About Me* page (**'/aboutme'**).

- **login**: Renders the login page (**'/login'**) and handles user authentication. If the user provides valid credentials, it sets the logged_in session variable to `True`.

- **upload_page**: Renders the upload page (**'/upload'**).

- **upload**: Handles the image upload process (**'/upload-file'**). It saves the uploaded image to the specified upload directory, creates a thumbnail, and redirects to the home page upon successful upload.

- **logout**: Logs the user out by clearing the session (**'/logout'**).
