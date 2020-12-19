FROM node:14 AS build-stage

WORKDIR /react-app

COPY react-app/. .

# Build our React App
RUN npm install

RUN npm run build
# RUN echo $(ls)

FROM python:3.8

# Setup Flask environment
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV SQLALCHEMY_ECHO=True

EXPOSE 8000

WORKDIR /var/www
COPY . .
COPY --from=build-stage /react-app/build/* app/static/

# Install Python Dependencies
RUN pip install -r requirements.txt
RUN pip install psycopg2

# Run flask environment
CMD gunicorn app:app
# WORKDIR /var/www

# COPY . .
# # TODO: Copy build files from build-stage into app/static
# # COPY requirements.txt .
# # COPY /app /app
# # COPY .flaskenv .
# RUN pip install -r requirements.txt

# # RUN cd app && mkdir static
# # # RUN cd ..
# # RUN ls
# # RUN pwd
# # WORKDIR /var/www/app/static
# # RUN mkdir static
# # COPY --from=build-stage /react-app/build /app/static
# COPY --from=build-stage /react-app/build/* app/static/

# # TODO: Install Python Dependencies

# # Run flask environment
# # WORKDIR /var/www
# CMD gunicorn app:app