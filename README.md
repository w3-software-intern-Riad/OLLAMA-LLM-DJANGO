# Django CLI App for Property Information Enhancement

This Django CLI application allows admins to log in, fetch property information from another database, generate creative titles and descriptions using the `ollama` LLM model, and create a summary based on the title, description, and additional information like location and amenities. The summary is then mapped to the corresponding property and stored in another table.

## Features

- Admin login for secure access.
- Fetch property information from an external database.
- Generate creative property titles using the `ollama` LLM model.
- Create property descriptions using the generated titles.
- Generate a comprehensive summary using the title, description, location, and amenities.
- Store the generated summary and map it to the corresponding property.

# Database Design for Hotel Information System

## Overview

This document outlines the database design for the Hotel Information System. The system manages hotel data, including titles, descriptions, images, locations, amenities, and summaries generated using the `ollama` LLM model.

## Tables

### 1. HotelInformation Table

Stores main details about each hotel.

| Column Name   | Data Type | Description                                               |
|---------------|-----------|-----------------------------------------------------------|
| `id`          | INTEGER   | Auto-generated unique identifier for each hotel (Primary Key). |
| `title`       | VARCHAR   | The title of the hotel.                                   |
| `description` | TEXT      | A description of the hotel.                               |
| `create_date` | DATETIME  | The date and time when the hotel information was created. |
| `update_date` | DATETIME  | The date and time when the hotel information was last updated. |

### 2. Image Table

Stores image details and relates them to hotels.

| Column Name | Data Type | Description                                               |
|-------------|-----------|-----------------------------------------------------------|
| `id`        | INTEGER   | Auto-generated unique identifier for each image (Primary Key). |
| `hotel_id`  | INTEGER   | Foreign Key referencing `HotelInformation(id)`.           |
| `name`      | VARCHAR   | The name of the image file.                               |

### 3. Location Table

Stores information about locations. A hotel can be associated with multiple locations.

| Column Name | Data Type | Description                                               |
|-------------|-----------|-----------------------------------------------------------|
| `id`        | INTEGER   | Auto-generated unique identifier for each location (Primary Key). |
| `name`      | VARCHAR   | The name of the location.                                 |
| `type`      | VARCHAR   | The type of location (city, state, country).              |
| `latitude`  | FLOAT     | The latitude coordinate of the location.                  |
| `longitude` | FLOAT     | The longitude coordinate of the location.                 |

### 4. HotelLocation Table (Many-to-Many Relationship)

A join table to create a many-to-many relationship between `HotelInformation` and `Location`.

| Column Name   | Data Type | Description                                               |
|---------------|-----------|-----------------------------------------------------------|
| `id`          | INTEGER   | Auto-generated unique identifier (Primary Key).           |
| `hotel_id`    | INTEGER   | Foreign Key referencing `HotelInformation(id)`.           |
| `location_id` | INTEGER   | Foreign Key referencing `Location(id)`.                   |

### 5. Amenity Table

Stores amenity details.

| Column Name | Data Type | Description                                               |
|-------------|-----------|-----------------------------------------------------------|
| `id`        | INTEGER   | Auto-generated unique identifier for each amenity (Primary Key). |
| `name`      | VARCHAR   | The name of the amenity.                                  |

### 6. HotelAmenity Table (Many-to-Many Relationship)

A join table to create a many-to-many relationship between `HotelInformation` and `Amenity`.

| Column Name  | Data Type | Description                                               |
|--------------|-----------|-----------------------------------------------------------|
| `id`         | INTEGER   | Auto-generated unique identifier (Primary Key).           |
| `hotel_id`   | INTEGER   | Foreign Key referencing `HotelInformation(id)`.           |
| `amenity_id` | INTEGER   | Foreign Key referencing `Amenity(id)`.                    |

### 7. Summary Table

Stores the generated summary and maps it to the corresponding hotel.

| Column Name  | Data Type | Description                                               |
|--------------|-----------|-----------------------------------------------------------|
| `id`         | INTEGER   | Auto-generated unique identifier for each summary (Primary Key). |
| `hotel_id`   | INTEGER   | Foreign Key referencing `HotelInformation(id)`.           |
| `summary`    | TEXT      | The generated summary for the hotel.                      |

## Relationships

- **HotelInformation** (1) <---> (M) **Image**
- **HotelInformation** (M) <---> (M) **Location** (via **HotelLocation**)
- **HotelInformation** (M) <---> (M) **Amenity** (via **HotelAmenity**)
- **HotelInformation** (1) <---> (1) **Summary**

## Notes

- The `HotelInformation` table is the main table storing details about each hotel.
- Images, locations, and amenities are linked to hotels via foreign key relationships and join tables to support one-to-many and many-to-many relationships.
- The `Summary` table stores the generated summary information, mapped directly to the corresponding hotel using a foreign key.

## Prerequisites

- Python 3.x
- Django 4.x
- Install Ollama
- PostgreSQL (or your preferred database)
- Necessary Python packages listed in `requirements.txt`

## Setup and Installation

1. **Clone the Repository**
```bash
   git clone https://github.com/w3-software-intern-Riad/OLLAMA-LLM-DJANGO.git
   cd OLLAMA-LLM-DJANGO
   ```
2. **Create a Virtual Environment and Activate It**   
```bash
python3 -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. **Create a Virtual Environment and Activate It** 

```bash
pip install -r requirements.txt
```
4. **Configure .env**
```bash
create a .env file and configure it as .env.sample
```
 5. **Apply Migrations**



 ```bash
 python manage.py makemigrations polls
 
 python manage.py migrate
 ```

  6. **Create a Superuser**

 ```bash
 python manage.py createsuperuser
 ```

  ## Admin Interface

  ### Command

  ```bash
python manage.py ollama_services
```

### Terminal Output Example:
```bash
Admin username:👤 [Please provide the admin username that was used during the creation of the superuser account.]
```
```bash
Admin password:🔑 [Please provide the admin password that was used during the creation of the superuser account.]

```
### If admin is authenticated then

Data will be fetched from the desired database and pass through ollama and create new title description and summary then save it into database



## Contributing
### Contributions are welcome! Please follow the guidelines for contributing and ensure your code adheres to the project's style guidelines.

 - Fork the repository.

- Create a new branch (git checkout -b feature-branch).
-  Make your changes.
- Commit your changes (git commit -am 'Add feature').
- Push to the branch (git push origin feature-branch).
- Create a new Pull Request.