# Base image
FROM python:3-onbuild

# The port number the container should expose
EXPOSE 80

# run the application
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver"]
