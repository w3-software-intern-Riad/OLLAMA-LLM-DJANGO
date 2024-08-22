
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from polls.models import HotelInformation,  Summary

from colorama import Style, init
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from django.conf import settings
import requests  # type: ignore
from decouple import config

# Initialize Colorama
init(autoreset=True)

# Define custom style dictionary
custom_style = Style.from_dict({
    'prompt': 'fg:#00ff00 bold',  # Cyan text, bold
})


class Command(BaseCommand):
    help = 'Creating Title and description and summary with ollama'

    def handle(self, *args, **kwargs):

        print("\n\x1b[36m\x1b[1m=== Admin Login ===\x1b[0m\n")
        username = prompt('Admin username: ', style=custom_style)
        password = prompt('Admin password: ',
                          style=custom_style, is_password=True)
        if not username or not password:
            self.stdout.write(self.style.ERROR(
                'Please provide all required arguments: admin credentials'))
            return

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user or not user.is_superuser:
            self.stdout.write(self.style.ERROR(
                'Authentication failed or user is not an admin.'))
            return
        else:
            print("\n\x1b[36m\x1b[1m=== Admin is authenticated ===\x1b[0m\n")

        print(
            "\n\x1b[36m\x1b[1m=== Hold on OLLAMA is generating the data ===\x1b[0m\n")

    # Fetch all hotels
        hotels = HotelInformation.objects.all()

        for hotel in hotels:
            creative_title = self.generate_creative_title(hotel.title)

            if creative_title:
                hotel.title = creative_title

            else:
                print('Failed to create creative title')
            # Send the hotel title to ollama gemma:2b model to generate a description
            description = self.get_description_from_ollama(hotel.title)

            if description:
                # Update the hotel description
                hotel.description = description
                hotel.save()

                # Generate a summary using the new description, location, and amenities
                summary_text = self.get_summary_from_ollama(hotel, description)

                # Save the summary in the Summary model
                try:
                    # Attempt to create a Summary object
                    summary_instance = Summary.objects.get_or_create(
                        hotel=hotel,
                        summary_text=summary_text
                    )

                except Exception as e:
                    # Catch any exception that occurs and log or print the error message
                    print(
                        f"An error occurred while creating the summary: {str(e)}")
    # Optionally, you can log the exception or take other actions

                self.stdout.write(self.style.SUCCESS(
                    f"Processed hotel: {hotel.title}"))

        print("\n\x1b[36m\x1b[1m=== OLLAMA GENERATION FINISHED ===\x1b[0m\n")

    def generate_creative_title(self, title):
        response = requests.post(
            config('OLLAMA_URL'),  # Replace with actual port
            json={
                "model": config('OLLAMA_MODEL'),
                "prompt": f"Generate a single creative title for '{title}'. Respond with only the title, no additional text or explanations. The title should not include any special characters.",
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            self.stdout.write(self.style.ERROR(
                f"Failed to generate creative title for hotel: {title}"))
            return None

    def get_description_from_ollama(self, title):
        response = requests.post(
            config('OLLAMA_URL'),  # Replace with actual port
            json={
                "model": config('OLLAMA_MODEL'),
                "prompt": f" '{title}'. give me a creative description in short and don't add any intoductory part and don't use any special character",
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            self.stdout.write(self.style.ERROR(
                f"Failed to generate description for hotel title: {title}"))
            return None

    def get_summary_from_ollama(self, hotel, description):
        location = ", ".join(
            [f"{loc.name} ({loc.type})" for loc in hotel.locations.all()])
        amenities = ", ".join(
            [amenity.name for amenity in hotel.amenities.all()])

        prompt = (

            f"Description: {description}, Location: {location}, Amenities: {amenities}. "
            f"now give me a creative summary using this information and don't add any introductory part and don't use any special character"
        )

        response = requests.post(
            config('OLLAMA_URL'),  # Replace with actual port
            json={
                "model": config('OLLAMA_MODEL'),
                "prompt": prompt,
                "stream": False,
            }
        )

        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            self.stdout.write(self.style.ERROR(
                f"Failed to generate summary for hotel: {hotel.title}"))
            return "No summary available"
