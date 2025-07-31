from PIL import Image, ImageChops

class ImageCanvas:
    """
    A helper class for image manipulation using the Pillow library.
    It standardizes images to RGBA format for consistent processing.
    """

    def __init__(self, image: Image.Image):
        """
        Initializes the ImageCanvas with a Pillow Image object.
        It's recommended to use the factory class methods `create_blank` or `from_file`.
        """
        # Convert image to RGBA to standardize operations, especially blending
        self.image = image.convert('RGBA')

    @classmethod
    def create_blank(cls, size: tuple[int, int], color: tuple[int, int, int, int] = (0, 0, 0, 0)) -> 'ImageCanvas':
        """
        Creates a new ImageCanvas instance with a blank image.

        Args:
            size (tuple): The (width, height) of the new image.
            color (tuple): The RGBA background color. Defaults to fully transparent.
        
        Returns:
            ImageCanvas: A new instance with a blank image.
        """
        blank_image = Image.new('RGBA', size, color)
        return cls(blank_image)

    @classmethod
    def from_file(cls, filepath: str) -> 'ImageCanvas | None':
        """
        Creates a new ImageCanvas instance by loading an image from a file.

        Args:
            filepath (str): The path to the image file.
        
        Returns:
            ImageCanvas or None if the file cannot be loaded.
        """
        try:
            image = Image.open(filepath)
            return cls(image)
        except (FileNotFoundError, IOError) as e:
            print(f"Error: Could not load image from {filepath}. {e}")
            return None

    @property
    def size(self) -> tuple[int, int]:
        """Returns the (width, height) of the image."""
        return self.image.size

    def rescale(self, new_size: tuple[int, int]) -> 'ImageCanvas':
        """
        Rescales the image to a new size using a high-quality filter.

        This method returns a new ImageCanvas instance with the rescaled image,
        leaving the original instance unmodified.

        Args:
            new_size (tuple): The target (width, height).

        Returns:
            ImageCanvas: A new instance containing the rescaled image.
        """
        # Image.Resampling.LANCZOS is a high-quality downsampling filter that
        # preserves detail effectively.
        rescaled_image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        return ImageCanvas(rescaled_image)

    def blit(self, source: 'ImageCanvas', pos: tuple[int, int], new_size: tuple[int, int] | None = None, mode: str = 'alpha'):
        """
        Blits (draws) a source image onto this canvas.

        Args:
            source (ImageCanvas): The image instance to draw.
            pos (tuple): The (x, y) coordinates on the canvas to draw at.
            new_size (tuple, optional): A (width, height) to resize the source image to before blitting.
                                        If None, the source's original size is used. Defaults to None.
            mode (str, optional): The blending mode. Can be 'opaque', 'alpha',
                                  'lighten' (max color), or 'darken' (min color). Defaults to 'alpha'.
        """
        source_img = source.image
        if new_size:
            # Use the high-quality LANCZOS filter for resizing within blit as well.
            source_img = source_img.resize(new_size, Image.Resampling.LANCZOS)

        if mode == 'opaque':
            # Paste without transparency, ignoring the source's alpha channel.
            self.image.paste(source_img.convert('RGB'), pos)
        
        elif mode == 'alpha':
            # Paste using the source's alpha channel as the mask for smooth blending.
            self.image.paste(source_img, pos, source_img)

        elif mode in ('lighten', 'darken'):
            # For channel-wise operations, we need to work on a cropped region.
            x, y = pos
            w, h = source_img.size
            crop_box = (x, y, x + w, y + h)
            
            target_region = self.image.crop(crop_box)
            
            if mode == 'lighten':
                blended_region = ImageChops.lighter(target_region, source_img)
            else: # 'darken'
                blended_region = ImageChops.darker(target_region, source_img)
            
            self.image.paste(blended_region, crop_box)
        
        else:
            raise ValueError(f"Invalid blend mode '{mode}'. Choose from 'opaque', 'alpha', 'lighten', 'darken'.")

    def save(self, filepath: str):
        """
        Saves the current image to a file.

        Args:
            filepath (str): The destination file path (e.g., 'output.png').
        """
        try:
            # JPEG does not support transparency, so composite it over a white background.
            if filepath.lower().endswith(('.jpg', '.jpeg')):
                rgb_image = Image.new("RGB", self.image.size, (255, 255, 255))
                rgb_image.paste(self.image, mask=self.image.split()[3]) # 3 is the alpha channel
                rgb_image.save(filepath, 'JPEG', quality=95)
            else:
                # PNG and other formats support transparency.
                self.image.save(filepath)
            print(f"✅ Image successfully saved to {filepath}")
        except IOError as e:
            print(f"Error: Could not save image to {filepath}. {e}")
