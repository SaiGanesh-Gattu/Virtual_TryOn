import streamlit as st
from PIL import Image
import subprocess
from glob import glob
import numpy as np
import os
# Define your function for virtual try-on
def generate_tryon(person_image, cloth_image):
    # Replace with your actual logic for generating the try-on image
    # For now, let's assume it just returns one of the images for demonstration
    # person_img = Image.fromarray(np.uint8(person_img))
    # cloth_img = Image.fromarray(np.uint8(cloth_img))

    # Save images for the model input
    # person_img_path = './datasets/test/image/test_img.jpg'
    # cloth_img_path = './datasets/test/cloth/test_cloth.jpg'
    # print(f"Type of person_image: {type(person_image)}, Shape: {person_image.shape if isinstance(person_image, np.ndarray) else 'N/A'}")
    # print(f"Type of cloth_image: {type(cloth_image)}, Shape: {cloth_image.shape if isinstance(cloth_image, np.ndarray) else 'N/A'}")
    # person_image.save(person_img_path)
    # cloth_image.save(cloth_img_path)
    
    

    # Overwrite the first line of `test_pairs.txt` without truncating the file
    with open('./datasets/test_pairs.txt', 'r+') as f:
        lines = f.readlines()  # Read all lines
        lines[0] = f"{os.path.basename(person_image)} {os.path.basename(cloth_image)}\n"  # Overwrite the first line
        f.seek(0)  # Go back to the start of the file
        f.writelines(lines)  # Write the modified content

    # Run the VITON-HD model to generate the try-on image
    try:
        result = subprocess.run(
            "python test.py --name checkpoints", 
            shell=True, capture_output=True, text=True
        )

        # Check for any errors in the subprocess output
        if result.returncode != 0:
            return f"Error during model execution: {result.stderr}"
    except Exception as e:
        st.error(f"Exception during model execution: {e}")
        return None

    # Access the first image from the results directory (no sorting needed)
    result_folder = './results/checkpoints/'
    result_images = glob(result_folder + '*.jpg')  # Get list of output images

    # Return the first generated image if it exists
    if result_images:
        return Image.open(result_images[0])
    else:
        return "No output generated."

st.title("AI Based Virtual Try-On")
tab1, tab2, tab3 = st.tabs(["Home", "About", "Contact"])

with tab1:
    col1,col2=st.columns(2)

    # Upload Images
    with col1:
        st.header("Person Image:")
        person_file = st.file_uploader("Select the Person Image", type=["jpg", "jpeg", "png"])
        if person_file is not None: 
            st.image(Image.open(person_file), caption="Selected Person", use_container_width=True)
        else:
            st.info("Please person image to proceed.")

    with col2:
        st.header("Cloth Image:")
        cloth_file = st.file_uploader("Select the Cloth Image", type=["jpg", "jpeg", "png"])
        if cloth_file is not None: 
            st.image(Image.open(cloth_file), caption="Selected Cloth", use_container_width=True)
        else:
            st.info("Please person image to proceed.")

    if person_file and cloth_file:
        # Display uploaded images
        # Generate Try-On Button
        if st.button("Generate Try-On"):
            person_image = Image.open(person_file)
            cloth_image = Image.open(cloth_file)
            
            with open('./datasets/test_pairs.txt', 'r+') as f:
                lines = f.readlines()  # Read all lines
                lines[0] = f"{person_file.name} {cloth_file.name}\n"  # Overwrite the first line
                f.seek(0)  # Go back to the start of the file
                f.writelines(lines)  # Write the modified content
            
            # Generate the try-on image
            # result_image = generate_tryon(person_image, cloth_image)
            try:
                result = subprocess.run(
                    "python test.py --name checkpoints", 
                    shell=True, capture_output=True, text=True
                )

                # Check for any errors in the subprocess output
                if result.returncode != 0:
                        print(f"Error during model execution: {result.stderr}")
            except Exception as e:
                st.error(f"Exception during model execution: {e}")

            # Access the first image from the results directory (no sorting needed)
            result_folder = './results/checkpoints/'
            result_images = glob(result_folder + '*.jpg')  # Get list of output images

            # Return the first generated image if it exists
            if result_images:
                result_image=Image.open(result_images[0])
            else:
                print("No output generated.")
            
            # Display the result
            st.image(result_image, caption="Try-On Result", use_container_width=True)
            for filename in os.listdir(result_folder):
                file_path = os.path.join(result_folder, filename)
                if os.path.isfile(file_path):  # Check if it is a file
                    os.remove(file_path)
            
            # if st.session_state.is_processing and st.button("Stop Process"):
            #     if st.session_state.process:
            #         st.session_state.process.terminate()  # Terminate the process
            #         st.session_state.process.wait()  # Ensure the process is fully stopped
            #         st.session_state.is_processing = False  # Reset the flag
            #         st.success("Process stopped.")
    else:
        st.info("Please upload both images to proceed.")


with tab2:
    st.title("About")
    st.write("""
             AI-based virtual try-on systems represent cutting-edge technology that 
aims to digitally superimpose clothing items onto images of people, creating a 
realistic visualization of how garments would look when worn. These systems 
leverage advanced techniques in computer vision, deep learning, and image 
processing to analyze and manipulate both the target person's image and the 
clothing item.  \n 
At the core of these virtual try-on systems are sophisticated processes that 
involve garment detection, body pose estimation, and realistic image 
synthesis. The system first identifies and segments the clothing from a 
database of digital garments, then aligns it with the user’s body by analyzing 
their pose and body contours. The final step involves rendering the clothing 
onto the user’s image, ensuring that it appears natural, with accurate fitting, 
fabric draping, and texture preservation. These processes work together to 
create a lifelike visualization that closely mimics how the clothing would look 
and fit in reality.   \n
Despite these challenges, image-based virtual try-on systems have wide
ranging applications across various industries. In e-commerce, customers can 
virtually try on clothes before purchasing, potentially reducing return rates and 
improving customer satisfaction. Fashion designers can use these systems to 
visualize their creations on different body types, while personal styling 
applications can assist users in putting together outfits without physically trying 
on clothes. As the technology continues to evolve, future directions include 
real-time processing for instantaneous try-on experiences, multi-view synthesis 
to generate images from multiple angles, and enhanced customization options. 
These advancements have the potential to revolutionize how consumers 
interact with fashion in the digital age, blending the convenience of online 
shopping with the experiential aspects of in-store fitting rooms.""")

with tab3:
    st.title("Contact Us")
    st.write("""
            Vaishnavi G     -9242895449\t  vaishnavig1518@gmail.com  \n
            H Chandana      -8867400520\t  hchandana009@gmail.com \n
             G Sai Ganesh    -7013227613\t  saiganeshgattu123@gmail.com   \n
             KMD Ashraf Ali  -9390071339\t  ashrafalikmd05@gmail.com  \n

             """)