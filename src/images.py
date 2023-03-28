import replicate

from log_config import logger

# Setup Replicate (Image Generation)
model = replicate.models.get("stability-ai/stable-diffusion")
version = model.versions.get(
    "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"
)


def generate_image(image_prompt):
    """
    Generates an image based on the provided prompt using the Replicate library.

    Args:
        image_prompt (str): The prompt to use for image generation.

    Returns:
        The generated image as a numpy array.
    """
    inputs = {
        "prompt": image_prompt,
        "image_dimensions": "768x768",
        "num_outputs": 1,
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        "scheduler": "DPMSolverMultistep",
    }

    try:
        image = version.predict(**inputs)
    except Exception as e:
        # Handle any exceptions that arise during image generation.
        logger.error(f"Error generating image: {e}")
        return None

    return image[0]
