import os
import shutil
import glob
from PIL import Image

# --- Configuration ---
# The name of the main directory to export files into.
EXPORT_DIR_NAME = "export"
# The directory where the source folders (01-99) are located.
SOURCE_DIR = "saves"

# --- HTML Template ---
# This is the template for the index.html file.
# The placeholder {FOLDER_COUNT} will be replaced by the script.
# The image source is now correctly pointing to the .jpg file.
# Note: CSS/JS curly braces are escaped by doubling them (e.g., {{...}})
# so that Python's f-string formatting ignores them.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIXTAPES</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Montserrat', sans-serif;
            background: #ffffff;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            margin-bottom: 60px;
            opacity: 0;
            animation: fadeInUp 1s ease-out 0.2s forwards;
        }}

        .header h1 {{
            font-size: 4rem;
            font-weight: 900;
            color: white;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.1em;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 300;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            padding: 0;
        }}

        .grid-item {{
            position: relative;
            aspect-ratio: 320/470;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            opacity: 0;
            animation: fadeInUp 0.3s ease-out forwards;
        }}

        .grid-item:hover {{
            transform: translateY(-2px) scale(1.02);
        }}

        .mixtape-cover {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            transition: transform 0.4s ease;
        }}

        .grid-item:hover .mixtape-cover {{
            transform: scale(1.02);
        }}

        .text-tile {{
            grid-column: span 2;
            aspect-ratio: 640/435;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
            overflow: hidden;
            border-radius: 8px;
        }}

        .text-tile::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            transition: transform 0.6s ease;
        }}

        .text-tile:hover::before {{
            transform: rotate(45deg) translateX(100%);
        }}

        .text-content {{
            z-index: 2;
            position: relative;
            color: white;
            font-weight: 700;
            font-size: 1.5rem;
            line-height: 1.2;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            white-space: pre-line;
        }}

        .play-icon {{
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 8px;
            transition: transform 0.3s ease;
        }}

        .grid-item:hover .play-icon {{
            transform: scale(1.05);
        }}

        .play-icon::after {{
            content: '';
            width: 0;
            height: 0;
            border-left: 14px solid #333;
            border-top: 8px solid transparent;
            border-bottom: 8px solid transparent;
            margin-left: 3px;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 20px 15px;
            }}

            .header h1 {{
                font-size: 2.5rem;
            }}

            .header p {{
                font-size: 1rem;
            }}

            .grid {{
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 12px;
            }}

            .text-content {{
                font-size: 1.2rem;
            }}
        }}

        @media (max-width: 480px) {{
            .header h1 {{
                font-size: 2rem;
            }}

            .grid {{
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
            }}

            .text-content {{
                font-size: 1rem;
            }}

            .text-tile {{
                grid-column: span 3;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="grid" id="mixtapeGrid">
            <!-- Single large text tile -->
            <div class="grid-item text-tile">
                <div class="text-content">MIXTAPES<br>FROM THE '90s<br>Dreamt up by AI.<br>Click a tape to listen.</div>
            </div>
        </div>
    </div>

    <script>
        // Function to add a mixtape to the grid
        function addMixtape(coverImage, htmlPage, title) {{
            const grid = document.getElementById('mixtapeGrid');
            const gridItem = document.createElement('div');
            gridItem.className = 'grid-item';
            gridItem.onclick = () => window.location.href = htmlPage;
            
            gridItem.innerHTML = `
                <img src="${{coverImage}}" alt="${{title}}" class="mixtape-cover">
            `;
            
            grid.appendChild(gridItem);
        }}

        // Dynamically generate mixtapes
        function generateMixtapes() {{
            // Create array of numbers from 1 to the number of folders created
            const mixtapeNumbers = Array.from({{length: {FOLDER_COUNT}}}, (_, i) => i + 1);
            
            // Shuffle the array using Fisher-Yates algorithm
            for (let i = mixtapeNumbers.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [mixtapeNumbers[i], mixtapeNumbers[j]] = [mixtapeNumbers[j], mixtapeNumbers[i]];
            }}
            
            // Create mixtapes in scrambled order
            mixtapeNumbers.forEach(num => {{
                const paddedNumber = num.toString().padStart(2, '0');
                const coverImage = `${{paddedNumber}}/cover-composited.jpg`;
                const htmlPage = `${{paddedNumber}}/page.html`;
                const title = `Mixtape ${{paddedNumber}}`;
                
                addMixtape(coverImage, htmlPage, title);
            }});
        }}

        // Generate all mixtapes when page loads
        document.addEventListener('DOMContentLoaded', function() {{
            generateMixtapes();
            
            // Apply staggered animation delays to all grid items
            const gridItems = document.querySelectorAll('.grid-item');
            gridItems.forEach((item, index) => {{
                item.style.animationDelay = `${{index * 0.05}}s`;
            }});
        }});

        // Add hover sound effect (optional)
        document.addEventListener('DOMContentLoaded', function() {{
            // Use event delegation since items are added dynamically
            document.getElementById('mixtapeGrid').addEventListener('mouseenter', function(e) {{
                if (e.target.closest('.grid-item:not(.text-tile)')) {{
                    // Optional: Play a subtle hover sound
                    // const audio = new Audio('hover-sound.mp3');
                    // audio.volume = 0.1;
                    // audio.play();
                }}
            }}, true);
        }});
    </script>
</body>
</html>
"""

def organize_files():
    """
    Finds numbered subdirectories in 'saves/', creates sequentially numbered folders
    in an 'export' directory, converts cover PNG to JPG, copies other files,
    and finally generates an index.html file.
    """
    print("Starting the file organization process...")
    print("NOTE: This script requires the Pillow library. Install it with 'pip install Pillow'")

    # --- 1. Create the main export directory ---
    export_path = os.path.join(".", EXPORT_DIR_NAME)
    try:
        os.makedirs(export_path, exist_ok=True)
        print(f"Successfully created or found the main export directory: '{export_path}'")
    except OSError as e:
        print(f"Error: Could not create directory {export_path}. Reason: {e}")
        return

    # --- Initialize a counter for the sequential export folders ---
    export_folder_counter = 1

    # --- 2. Go through all potential source subdirectories (saves/01-99) ---
    for i in range(1, 100):
        source_subdir_name = f"{i:02d}"
        source_subdir_path = os.path.join(SOURCE_DIR, source_subdir_name)

        if os.path.isdir(source_subdir_path):
            print(f"\nProcessing source subdirectory: '{source_subdir_path}'")

            # --- 3. Create the next sequential folder in the export directory ---
            target_subdir_name = f"{export_folder_counter:02d}"
            target_subdir_path = os.path.join(export_path, target_subdir_name)
            try:
                os.makedirs(target_subdir_path, exist_ok=True)
                print(f" -> Created destination folder: '{target_subdir_path}'")
            except OSError as e:
                print(f"Error: Could not create directory {target_subdir_path}. Skipping. Reason: {e}")
                continue

            # --- 4. Find and copy the -tape.mp3 file ---
            tape_files = glob.glob(os.path.join(source_subdir_path, "*-tape.mp3"))
            if tape_files:
                for tape_file_path in tape_files:
                    try:
                        shutil.copy(tape_file_path, target_subdir_path)
                        print(f"   -> Copied '{os.path.basename(tape_file_path)}'")
                    except (shutil.Error, IOError) as e:
                        print(f"Error: Could not copy '{os.path.basename(tape_file_path)}'. Reason: {e}")
            else:
                print(f"   -> Warning: No '*-tape.mp3' file found in '{source_subdir_path}'.")

            # --- 5. Convert cover-composited.png to JPG ---
            source_image_path = os.path.join(source_subdir_path, "cover-composited.png")
            target_image_path = os.path.join(target_subdir_path, "cover-composited.jpg")
            if os.path.exists(source_image_path):
                try:
                    with Image.open(source_image_path) as img:
                        # Convert to RGB to remove alpha channel, which is necessary for JPG
                        rgb_img = img.convert('RGB')
                        rgb_img.save(target_image_path, 'jpeg', quality=90)
                        print("   -> Converted 'cover-composited.png' to JPG.")
                except Exception as e:
                    print(f"Error: Could not convert image. Reason: {e}")
            else:
                print("   -> Warning: File 'cover-composited.png' not found.")

            # --- 6. Read, modify, and write page.html ---
            source_page_path = os.path.join(source_subdir_path, "page.html")
            if os.path.exists(source_page_path):
                try:
                    # Read the original page.html content
                    with open(source_page_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace the image reference
                    modified_content = content.replace('cover-composited.png', 'cover-composited.jpg')
                    
                    # Write the modified content to the new location
                    target_page_path = os.path.join(target_subdir_path, 'page.html')
                    with open(target_page_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    
                    print("   -> Copied and modified 'page.html' to use JPG.")

                except Exception as e:
                    print(f"Error: Could not process 'page.html'. Reason: {e}")
            else:
                print(f"   -> Warning: File 'page.html' not found in '{source_subdir_path}'.")

            # --- Increment the counter for the next destination folder ---
            export_folder_counter += 1

    # --- 7. Create the index.html file after all copying is done ---
    final_folder_count = export_folder_counter - 1
    if final_folder_count > 0:
        print(f"\nFile copying complete. Processed {final_folder_count} director{'y' if final_folder_count == 1 else 'ies'}.")
        
        final_html_content = HTML_TEMPLATE.format(FOLDER_COUNT=final_folder_count)
        index_file_path = os.path.join(export_path, "index.html")
        
        try:
            with open(index_file_path, "w", encoding="utf-8") as f:
                f.write(final_html_content)
            print(f"Successfully created 'index.html' in '{export_path}'.")
        except IOError as e:
            print(f"Error: Could not write index.html file. Reason: {e}")
    else:
        print(f"\nNo source directories found in '{SOURCE_DIR}'. No files were copied and index.html was not created.")

    print("\nDone. File organization process finished.")

if __name__ == "__main__":
    organize_files()
