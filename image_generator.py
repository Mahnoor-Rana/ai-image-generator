import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
import time
import os

# Configure the page
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 10px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .image-container {
        border: 3px solid #e0e0e0;
        border-radius: 15px;
        padding: 1rem;
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def create_placeholder_image(prompt, width, height):
    """
    Create a placeholder image with the prompt text.
    In a real implementation, replace this with actual AI image generation API calls.
    """
    # Create a colorful gradient background
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Create gradient background
    for y in range(height):
        r = int(255 * (y / height))
        g = int(255 * (1 - y / height))
        b = 150
        for x in range(width):
            draw.point((x, y), fill=(r, g, b))
    
    # Add text overlay
    try:
        # Try to use a larger font size
        font_size = min(width, height) // 20
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Wrap text for better display
    words = prompt.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] < width - 40:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw text
    total_height = len(lines) * (font_size + 10)
    start_y = (height - total_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + i * (font_size + 10)
        
        # Draw shadow
        draw.text((x + 2, y + 2), line, fill='black', font=font)
        # Draw main text
        draw.text((x, y), line, fill='white', font=font)
    
    return image

def generate_image_huggingface(prompt, width, height, api_key):
    """Generate image using Hugging Face Inference API"""
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": width,
            "height": height,
            "num_inference_steps": 20
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        return image
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

def generate_image_openai(prompt, width, height, api_key):
    """Generate image using OpenAI DALL-E API"""
    try:
        # Try the new OpenAI client first (v1.0+)
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            # DALL-E 3 supports specific sizes
            size_map = {
                (1024, 1024): "1024x1024",
                (1792, 1024): "1792x1024", 
                (1024, 1792): "1024x1792"
            }
            
            # Find closest supported size
            target_size = "1024x1024"  # default
            min_diff = float('inf')
            for (w, h), size_str in size_map.items():
                diff = abs(w - width) + abs(h - height)
                if diff < min_diff:
                    min_diff = diff
                    target_size = size_str
            
            # Generate image with DALL-E 3
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=target_size,
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
        except ImportError:
            # Fallback to older OpenAI library
            import openai
            openai.api_key = api_key
            
            # DALL-E 3 supports specific sizes
            size_map = {
                (1024, 1024): "1024x1024",
                (1792, 1024): "1792x1024", 
                (1024, 1792): "1024x1792"
            }
            
            # Find closest supported size
            target_size = "1024x1024"  # default
            min_diff = float('inf')
            for (w, h), size_str in size_map.items():
                diff = abs(w - width) + abs(h - height)
                if diff < min_diff:
                    min_diff = diff
                    target_size = size_str
            
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=target_size,
                model="dall-e-3"
            )
            
            image_url = response['data'][0]['url']
        
        # Download and process the image
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            raise Exception(f"Failed to download image: {image_response.status_code}")
            
        image = Image.open(io.BytesIO(image_response.content))
        
        # Resize to requested dimensions if needed
        if image.size != (width, height):
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        
        return image
        
    except ImportError:
        raise Exception("OpenAI library not installed. Run: pip install openai")
    except Exception as e:
        error_msg = str(e)
        if "billing" in error_msg.lower():
            raise Exception("❌ OpenAI API Error: Please check your billing and credits at https://platform.openai.com/account/billing")
        elif "invalid" in error_msg.lower() and "api" in error_msg.lower():
            raise Exception("❌ Invalid API Key. Please check your OpenAI API key at https://platform.openai.com/api-keys")
        else:
            raise Exception(f"❌ OpenAI API Error: {error_msg}")

def generate_image_stability(prompt, width, height, api_key):
    """Generate image using Stability AI API"""
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    body = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "width": width,
        "height": height,
        "steps": 20,
        "samples": 1,
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        data = response.json()
        image_data = base64.b64decode(data["artifacts"][0]["base64"])
        image = Image.open(io.BytesIO(image_data))
        return image
    else:
        raise Exception(f"Stability AI Error: {response.status_code} - {response.text}")

def generate_image_api(prompt, width, height, api_provider="Demo Mode", api_key=None):
    """
    Generate image using selected API provider
    """
    if api_provider == "Demo Mode":
        # Create a simple colored rectangle instead of text overlay
        time.sleep(1)  # Simulate API delay
        image = Image.new('RGB', (width, height), color=(100, 150, 200))
        return image
    
    elif api_provider == "Hugging Face":
        if not api_key:
            raise Exception("Please provide Hugging Face API key")
        return generate_image_huggingface(prompt, width, height, api_key)
    
    elif api_provider == "OpenAI DALL-E":
        if not api_key:
            raise Exception("Please provide OpenAI API key")
        return generate_image_openai(prompt, width, height, api_key)
    
    elif api_provider == "Stability AI":
        if not api_key:
            raise Exception("Please provide Stability AI API key")
        return generate_image_stability(prompt, width, height, api_key)
    
    else:
        raise Exception("Unknown API provider")

def main():
    # App header
    st.markdown('<h1 class="main-header">🎨 AI Image Generator</h1>', unsafe_allow_html=True)
    st.markdown("Transform your ideas into stunning visuals with customizable dimensions!")
    
    # Sidebar for parameters
    st.sidebar.header("🎛️ Image Settings")
    
    # Image dimensions
    col1, col2 = st.sidebar.columns(2)
    with col1:
        width = st.number_input(
            "Width (px)", 
            min_value=64, 
            max_value=2048, 
            value=512, 
            step=64,
            help="Image width in pixels"
        )
    
    with col2:
        height = st.number_input(
            "Height (px)", 
            min_value=64, 
            max_value=2048, 
            value=512, 
            step=64,
            help="Image height in pixels"
        )
    
    # Aspect ratio presets
    st.sidebar.subheader("📐 Quick Presets")
    preset_col1, preset_col2 = st.sidebar.columns(2)
    
    with preset_col1:
        if st.button("Square\n1:1"):
            st.session_state.width = 512
            st.session_state.height = 512
            st.rerun()
        
        if st.button("Portrait\n3:4"):
            st.session_state.width = 384
            st.session_state.height = 512
            st.rerun()
    
    with preset_col2:
        if st.button("Landscape\n4:3"):
            st.session_state.width = 512
            st.session_state.height = 384
            st.rerun()
        
        if st.button("Wide\n16:9"):
            st.session_state.width = 512
            st.session_state.height = 288
            st.rerun()
    
    # API Configuration
    with st.sidebar.expander("🔑 OpenAI Settings", expanded=True):
        api_provider = "OpenAI DALL-E"  # Default to OpenAI
        
        api_key = st.text_input(
            "OpenAI API Key", 
            type="password",
            help="Enter your OpenAI API key from https://platform.openai.com/api-keys"
        )
        
        if api_key:
            st.success("✅ API Key provided!")
            # st.info("💡 Using DALL-E 3 for high-quality image generation")
        else:
            st.warning("⚠️ Please enter your OpenAI API key to generate images")
            st.info("🔗 Get your API key: https://platform.openai.com/api-keys")
    
    # Main content area
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("✏️ Image Prompt")
        
        # Text prompt input
        prompt = st.text_area(
            "Describe your image:",
            placeholder="e.g., A futuristic cityscape at sunset with flying cars and neon lights",
            height=120,
            help="Be as descriptive as possible for better results"
        )
        
        # Additional parameters
        with st.expander("🎨 Advanced Options"):
            style = st.selectbox(
                "Art Style",
                ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", "Sketch", "Anime"]
            )
            
            quality = st.select_slider(
                "Quality",
                options=["Draft", "Standard", "High", "Ultra"],
                value="Standard"
            )
            
            seed = st.number_input(
                "Seed (for reproducibility)",
                min_value=0,
                max_value=999999,
                value=42,
                help="Use the same seed to generate similar images"
            )
        
        # Generate button
        can_generate = prompt.strip() and api_key
        generate_btn = st.button(
            "🚀 Generate Image",
            disabled=not can_generate,
            help="Generate high-quality AI image " if can_generate else 
                 "Please enter a prompt and your OpenAI API key"
        )
    
    with col2:
        st.subheader("🎨 Generated Image")
        
        # Image display area
        image_placeholder = st.empty()
        
        with image_placeholder.container():
            if not hasattr(st.session_state, 'generated_image'):
                # st.info("👈 Enter your OpenAI API key and prompt, then click 'Generate different Images")
                # Show a simple placeholder
                placeholder_img = Image.new('RGB', (400, 300), color=(240, 240, 240))
                st.image(placeholder_img, use_container_width =True)
    
    # Generate image when button is clicked
    if generate_btn and prompt.strip() and api_key:
        with st.spinner("🎨 Creating your masterpiece "):
            try:
                # Add style to prompt if selected
                if style != "Photorealistic":
                    enhanced_prompt = f"{prompt}, {style.lower()} style"
                else:
                    enhanced_prompt = prompt
                
                # Generate the image
                generated_image = generate_image_api(
                    enhanced_prompt, width, height, api_provider, api_key
                )
                st.session_state.generated_image = generated_image
                st.session_state.last_prompt = prompt
                
                # Display success message
                st.success("✨ Amazing image generated")
                
            except Exception as e:
                error_message = str(e)
                st.error(f"🚫 {error_message}")
                
                # Helpful troubleshooting
                if "billing" in error_message.lower():
                    st.info("💳 Check your OpenAI account billing: https://platform.openai.com/account/billing")
                elif "api" in error_message.lower() and "key" in error_message.lower():
                    st.info("🔑 Verify your API key: https://platform.openai.com/api-keys")
    
    # Display generated image
    if hasattr(st.session_state, 'generated_image'):
        with image_placeholder.container():
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(
                st.session_state.generated_image,
                caption=f"Generated from: '{st.session_state.get('last_prompt', 'Unknown prompt')}' | Dimensions: {width}x{height}px",
                use_container_width =True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download button
            img_buffer = io.BytesIO()
            st.session_state.generated_image.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
            
            st.download_button(
                label="💾 Download Image",
                data=img_bytes,
                file_name=f"ai_generated_{width}x{height}.png",
                mime="image/png",
                use_container_width=True
            )
    
    # Footer with instructions
    st.markdown("---")
    

if __name__ == "__main__":
    main()