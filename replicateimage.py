import os
import replicate
import traceback

ASPECT_TO_WIDTH_HEIGHT_SANA = {
	"2:1": (1536,768),
	"9:16": (768,1344),
	"2:3": (768,1152),
	"1:1": (1024,1024),
	"1:2": (768,1536),
	"16:9": (1344,768),
	"3:2": (1152,768),    
}
ASPECT_TO_WIDTH_HEIGHT_SDXL = {
	"2:1": (1024,512),
	"9:16": (720,1280),
	"2:3": (768,1152),
	"1:1": (1024,1024),
	"1:2": (512,1024),
	"16:9": (1280,720),
	"3:2": (1152,768),    
}

ASPECT_TO_STRING_HIDREAM = {
    "1:1": "1024 × 1024 (Square)",
    "16:9": "768 × 1360 (Portrait)",
    "9:16": "1360 × 768 (Landscape)",
    "2:3": "1248 × 832 (Landscape)",
    "3:2": "832 × 1248 (Portrait)",	
    "1:2": "1248 × 832 (Landscape)",
    "2:1": "832 × 1248 (Portrait)",	
}

ASPECT_TO_STRING_IMAGEN = {
    "1:1": "1:1",
    "16:9": "16:9",
    "9:16": "9:16",
    "2:3": "3:4",
    "3:2": "4:3",	
    "1:2": "9:16",
    "2:1": "16:9",	
}

# models:
# black-forest-labs/flux-dev
# black-forest-labs/flux-1.1-pro

OUTPAINT_ZOOM_150 = "Zoom out 1.5x"
OUTPAINT_ZOOM_200 = "Zoom out 2x"
OUTPAINT_MAKE_SQUARE = "Make square"
OUTPAINT_LEFT = "Left outpaint"
OUTPAINT_RIGHT = "Right outpaint"
OUTPAINT_TOP = "Top outpaint"
OUTPAINT_BOTTOM = "Bottom outpaint"

class ReplicateImage:
	def __init__(self, api_key):
		self.api_key = api_key
		os.environ["REPLICATE_API_TOKEN"] = api_key

	def outpaint_image(self, input_url, output_path, outpaint_option, prompt, prompt_upsampling = True, seed = None):
		print("FLUX outpaint")
		print(f"DEBUG - Input URL at Replicate client: {input_url}")
		input = {
			"image": input_url,
			"steps": 50,
			"prompt": prompt,
			"output_format": "png",
			"safety_tolerance": 6,
			"prompt_upsampling": prompt_upsampling,
			"outpaint": outpaint_option
		}
		if seed is not None:
			input["seed"] = seed
		output = replicate.run(
			"black-forest-labs/flux-fill-pro",
			input=input
		)
		with open(output_path, "wb") as file:
			file.write(output.read())

	def inpaint_image(self, input_url, mask_url, output_path, prompt, prompt_upsampling=True, seed=None):
		"""Generates an inpaint image using flux-fill-pro."""
		print("FLUX inpaint")
		print(f"DEBUG - Input URL: {input_url}")
		print(f"DEBUG - Mask URL: {mask_url}")
		input_params = {
			"image": input_url,
			"mask": mask_url,
			"steps": 50,
			"prompt": prompt,
			"output_format": "png",
			"safety_tolerance": 6,
			"prompt_upsampling": prompt_upsampling
		}
		if seed is not None:
			input_params["seed"] = seed

		try:
			output = replicate.run(
				"black-forest-labs/flux-fill-pro",
				input=input_params
			)
			# Save the output image
			with open(output_path, "wb") as file:
				file.write(output.read())
			print(f"Successfully saved inpaint result to: {output_path}")
			return True # Indicate success
		except Exception as e:
			print(f"Error during Replicate inpaint run: {e}")
			traceback.print_exc()
			return False # Indicate failure

	def generate_image(self, output_path, prompt, aspect = "16:9", prompt_upsampling = True, model = "black-forest-labs/flux-1.1-pro", seed = None):
		print("FLUX prompt: " + prompt)
		if model == "black-forest-labs/flux-1.1-pro":
			input = {
				"prompt": prompt,
				"aspect_ratio": aspect,
				"output_format": "png",
				"output_quality": 100,
				"safety_tolerance": 6,
				"prompt_upsampling": prompt_upsampling
			}
			if seed is not None:
				input["seed"] = seed

			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output.read())

			return True
		elif model == "black-forest-labs/flux-dev":
			input = {
				"prompt": prompt,
				"guidance": 3.5,
				"aspect_ratio": aspect,
				"output_format": "png",
				"output_quality": 100,
				"disable_safety_checker": True
			}
			if seed is not None:
				input["seed"] = seed
			print(input)

			output = replicate.run(
				"black-forest-labs/flux-dev",
				input=input
			)
			print(output)
			with open(output_path, 'wb') as f:
				f.write(output[0].read())
			return True
		elif model == "google/imagen-3":
			input = {
				"prompt": prompt,
				"aspect_ratio": ASPECT_TO_STRING_IMAGEN[aspect],
				"safety_filter_level": "block_only_high"
			}
			if seed is not None:
				input["seed"] = seed
			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output.read())
			return True
		elif model == "google/imagen-4":
			input = {
				"prompt": prompt,
				"aspect_ratio": ASPECT_TO_STRING_IMAGEN[aspect],
				"safety_filter_level": "block_only_high",
				"output_format": "png",
			}
			if seed is not None:
				input["seed"] = seed
			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output.read())
			return True
		elif model == "ideogram-ai/ideogram-v3-quality":
			input = {
				"prompt": prompt,
				"aspect_ratio": aspect,
				"magic_prompt_option": "On" if prompt_upsampling else "Off"
			}
			if seed is not None:
				input["seed"] = seed
			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output.read())
			return True
		elif model == "bytedance/sdxl-lightning-4step:6f7a773af6fc3e8de9d5a3c00be77c17308914bf67772726aff83496ba1e3bbe":
			dim = ASPECT_TO_WIDTH_HEIGHT_SDXL[aspect]
			input = {
				"prompt": prompt,
				"width": dim[0],
				"height": dim[1],
				"disable_safety_checker": True
			}
			if seed is not None:
				input["seed"] = seed
			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output[0].read())
			return True
		elif model == "luma/photon":
			input = {
				"prompt": prompt,
				"aspect_ratio": aspect,
			}
			if seed is not None:
				input["seed"] = seed
			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output.read())
			return True
		elif model == "minimax/image-01":
			input = {
				"prompt": prompt,
				"aspect_ratio": aspect,
				"prompt_optimizer": prompt_upsampling
			}
			if seed is not None:
				input["seed"] = seed
			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output[0].read())
			return True
		elif model == "nvidia/sana:c6b5d2b7459910fec94432e9e1203c3cdce92d6db20f714f1355747990b52fa6":
			dim = ASPECT_TO_WIDTH_HEIGHT_SANA[aspect]
			input = {
				"prompt": prompt,
				"width": dim[0],
				"height": dim[1]
			}
			if seed is not None:
				input["seed"] = seed
			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output.read())
			return True
		elif model == "prunaai/hidream-l1-dev:597c67f9baf9bd7f4c363366c1991ff4e126b566437e10c5f5d83e25208be34b":
			input = {
				"prompt": prompt,
				"resolution": ASPECT_TO_STRING_HIDREAM[aspect],
				"speed_mode": "Unsqueezed 🍋 (highest quality)",
				"output_format": "png"
			}
			if seed is not None:
				input["seed"] = seed
			output = replicate.run(
				model,
				input=input
			)

			with open(output_path, "wb") as file:
				file.write(output.read())
			return True
		return False