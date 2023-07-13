# calendar-note

## Simple app note 
- Login / Register -> user
- CURD note ( set date and time to alert )
- Alert with email
- Simple to use

### Config With docker 
- Login docker ( Or use Docker desktop in WINDOW )
- COPY this:
  - ```  docker pull baphongpine/supercuif-calendar-note:v1  ```
- Run image:
  - ```  docker run -p 8000:8000 -e EMAIL_HOST_PASSWORD=YOUR-PASSWORD-HOST EMAIL_HOST_USER=YOUR-EMAIL  baphongpine/supercuif-calendar-note:v1  ```
- If don't want to send email:
  - ```  docker run -p 8000:8000 baphongpine/supercuif-calendar-note:v1  ```
  - Or contact me for use email HOST :))
- Then: http://localhost:8000
- Enjoy it !!


