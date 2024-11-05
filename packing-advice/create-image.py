import os

from openai import OpenAI

openai_client = OpenAI()


def main():
    # Step 1: Get truck type from user and auto-fetch dimensions
    print("Describe your image:\n")
    image_desc = input().strip().lower()
    generated_image = openai_client.images.generate(
        model="dall-e-3",
        prompt=image_desc,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = generated_image.data[0].url
    print("Image created here:")
    print(image_url)


if __name__ == "__main__":
    main()