import streamlit as st
import numpy as np
from PIL import Image
import cv2

def create_before_after_comparison(image1, image2, slider_position):
    """
    Create a before/after comparison where the slider position determines
    the boundary between the two images.
    
    Args:
        image1: PIL Image (left side / before)
        image2: PIL Image (right side / after)
        slider_position: float between 0 and 1 representing the boundary position
    
    Returns:
        PIL Image showing the comparison
    """
    # Convert PIL images to numpy arrays
    img1_np = np.array(image1)
    img2_np = np.array(image2)
    
    # Ensure images have the same dimensions
    height, width = min(img1_np.shape[0], img2_np.shape[0]), min(img1_np.shape[1], img2_np.shape[1])
    img1_np = img1_np[:height, :width]
    img2_np = img2_np[:height, :width]
    
    # Create the combined image
    result = np.copy(img1_np)
    
    # Calculate the boundary position in pixels
    boundary_x = int(width * slider_position)
    
    # Replace the right portion with image2
    result[:, boundary_x:] = img2_np[:, boundary_x:]
    
    # Add a vertical line at the boundary
    if boundary_x > 0 and boundary_x < width - 1:
        line_thickness = 3
        start_x = max(0, boundary_x - line_thickness//2)
        end_x = min(width, boundary_x + line_thickness//2)
        result[:, start_x:end_x] = [255, 255, 255]  # White line
    
    return Image.fromarray(result)

def main():
    st.set_page_config(page_title="Before/After Image Comparison", layout="wide")
    
    st.title("🔍 Before/After Image Comparison")
    st.markdown("Upload two images to create an interactive before/after comparison.")
    
    # Create two columns for file upload
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Before Image")
        before_file = st.file_uploader("Choose the 'before' image", type=['png', 'jpg', 'jpeg'], key="before")
    
    with col2:
        st.subheader("After Image")
        after_file = st.file_uploader("Choose the 'after' image", type=['png', 'jpg', 'jpeg'], key="after")
    
    # If both images are uploaded
    if before_file and after_file:
        # Load the images
        before_image = Image.open(before_file)
        after_image = Image.open(after_file)
        
        # Resize images to have the same dimensions (optional)
        if st.checkbox("Resize images to match", value=True):
            # Get the minimum dimensions
            min_width = min(before_image.width, after_image.width)
            min_height = min(before_image.height, after_image.height)
            
            before_image = before_image.resize((min_width, min_height))
            after_image = after_image.resize((min_width, min_height))
        
        # Create slider for controlling the boundary
        st.subheader("Comparison")
        slider_value = st.slider(
            "Drag to reveal before/after",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            help="0 = Only before image, 1 = Only after image"
        )
        
        # Create the comparison image
        comparison_image = create_before_after_comparison(before_image, after_image, slider_value)
        
        # Display the comparison
        st.image(comparison_image, caption=f"Comparison (Boundary at {slider_value:.0%})", use_container_width=True)
        
        # Show the original images side by side for reference
        with st.expander("View original images"):
            col3, col4 = st.columns(2)
            with col3:
                st.image(before_image, caption="Before", use_container_width=True)
            with col4:
                st.image(after_image, caption="After", use_container_width=True)
        
        # Add download button for the comparison image
        if st.button("Download Comparison Image"):
            # Convert PIL image to bytes
            import io
            buffer = io.BytesIO()
            comparison_image.save(buffer, format='PNG')
            st.download_button(
                label="Download PNG",
                data=buffer.getvalue(),
                file_name=f"comparison_{slider_value:.0%}.png",
                mime="image/png"
            )
    
    else:
        st.info("👆 Please upload both 'before' and 'after' images to start comparing.")
        
        # Show example with placeholder images
        st.subheader("Example")
        st.markdown("This is how the before/after comparison will look:")
        
        # Create sample images for demonstration
        if st.button("Show Demo with Sample Images"):
            # Create sample images (you can replace these with actual demo images)
            sample1 = np.zeros((300, 400, 3), dtype=np.uint8)
            sample1[:, :200] = [100, 150, 255]  # Blue left half
            sample1[:, 200:] = [255, 100, 100]  # Red right half
            cv2.putText(sample1, "BEFORE", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            sample2 = np.zeros((300, 400, 3), dtype=np.uint8)
            sample2[:, :200] = [100, 255, 100]  # Green left half
            sample2[:, 200:] = [255, 255, 100]  # Yellow right half
            cv2.putText(sample2, "AFTER", (160, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            # Convert to PIL Images
            sample_before = Image.fromarray(sample1)
            sample_after = Image.fromarray(sample2)
            
            # Create demo slider
            demo_slider = st.slider("Demo slider", 0.0, 1.0, 0.5, 0.01, key="demo")
            demo_comparison = create_before_after_comparison(sample_before, sample_after, demo_slider)
            st.image(demo_comparison, caption="Demo Comparison")

    # Add instructions
    with st.sidebar:
        st.markdown("## How to use:")
        st.markdown("""
        1. Upload a 'before' image (left side)
        2. Upload an 'after' image (right side)
        3. Use the slider to control the boundary
        4. Drag left to reveal more 'before'
        5. Drag right to reveal more 'after'
        
        Perfect for:
        - Before/after renovations
        - Disaster impact assessment
        - Progress documentation
        - Time-lapse comparisons
        """)
        
        st.markdown("## Tips:")
        st.markdown("""
        - Images work best when:
          - Same dimensions
          - Similar framing
          - Clear distinction between before/after
        - The app automatically resizes to match
        - White line shows current boundary
        """)

if __name__ == "__main__":
    main()