# 🎨 AI Image Generator

A powerful Streamlit web application that transforms your ideas into stunning visuals using OpenAI's DALL-E 3 API.

## ✨ Features

- **🎯 OPEN AI's DALL-E 3 Integration**: High-quality AI image generation
- **📐 Customizable Dimensions**: Set custom width and height (64px - 2048px)
- **🎨 Style Options**: Choose from various art styles (Photorealistic, Digital Art, Oil Painting, etc.)
- **⚡ Quick Presets**: One-click aspect ratios (Square, Portrait, Landscape, Wide)
- **💾 Easy Download**: Download generated images in PNG format
- **🔒 Secure**: API keys handled securely (not stored)

## 🚀 Live Demo

[**🌐 Try the App Live**](https://your-app-url.streamlit.app)

## 📸 Screenshots

### Main Interface
- Clean, intuitive design
- Real-time image generation
- Professional quality outputs

### Features
- Custom dimensions with preset options
- Advanced style controls
- Instant download functionality

## 🛠️ Installation & Setup

### Option 1: Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-image-generator.git

   cd ai-image-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get OpenAI API Key**
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Keep it secure!

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8501`

### Option 2: Deploy on Streamlit Cloud

1. **Fork this repository**
2. **Visit [Streamlit Community Cloud](https://share.streamlit.io)**
3. **Connect your GitHub account**
4. **Deploy with one click!**

## 🔑 API Key Setup

### For Local Use:
1. Get your OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)
2. Enter it in the sidebar when using the app
3. Your key is not stored - enter it fresh each session for security

### For Deployed Version:
Users need to bring their own OpenAI API key - this keeps the app free and secure!

## 🎯 How to Use

### Quick Start:
1. **Enter your OpenAI API Key** in the sidebar
2. **Write a descriptive prompt** (e.g., "A futuristic cityscape at sunset with flying cars")
3. **Choose dimensions** or use quick presets
4. **Select art style** (optional)
5. **Click "Generate with DALL-E 3"**
6. **Download your masterpiece!**

### Pro Tips for Better Results:
- **Be specific**: "Golden retriever puppy playing in a sunny garden" vs "dog"
- **Add style keywords**: "digital art", "photorealistic", "oil painting"
- **Mention lighting**: "soft lighting", "dramatic shadows", "golden hour"
- **Include composition**: "close-up portrait", "wide landscape shot", "centered"
- **Add details**: colors, mood, setting, camera angle

## 🎨 Supported Features

### Image Dimensions:
- **Custom sizes**: 64px to 2048px width/height
- **Quick presets**: 
  - Square (1:1) - 512x512px
  - Portrait (3:4) - 384x512px
  - Landscape (4:3) - 512x384px
  - Wide (16:9) - 512x288px

### Art Styles:
- Photorealistic
- Digital Art
- Oil Painting
- Watercolor
- Sketch
- Anime

### Quality Options:
- Draft (fast generation)
- Standard (balanced)
- High (detailed)
- Ultra (maximum quality)

## 📋 Requirements

### System Requirements:
- Python 3.7+
- Internet connection for API calls
- Modern web browser

### Dependencies:
- `streamlit` - Web app framework
- `pillow` - Image processing
- `requests` - HTTP requests
- `openai` - OpenAI API client

## 🔧 Technical Details

### Architecture:
- **Frontend**: Streamlit (Python web framework)
- **Image Generation**: OpenAI DALL-E 3 API
- **Image Processing**: PIL (Python Imaging Library)
- **Deployment**: Streamlit Community Cloud

### API Integration:
- Supports OpenAI DALL-E 3 with automatic sizing optimization
- Handles different aspect ratios intelligently
- Error handling with helpful user messages

## 🚨 Important Notes

### API Costs:
- DALL-E 3 charges per image generated
- Standard quality: ~$0.040 per image
- Check [OpenAI Pricing](https://openai.com/pricing) for current rates

### Rate Limits:
- OpenAI has rate limits on API usage
- App includes error handling for rate limit scenarios

### Privacy:
- API keys are never stored or logged
- Images are processed temporarily and not saved on our servers
- Users download images directly to their devices

## 🛡️ Security

- API keys handled securely (input masked, not stored)
- No user data persistence
- HTTPS encryption for all communications
- Open source code for transparency

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Ideas for Contributions:
- Additional AI model integrations
- New preset dimensions
- Enhanced UI components
- Image editing features
- Batch generation capabilities

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for the incredible DALL-E 3 API
- **Streamlit** for the amazing web framework
- **Python Community** for excellent libraries

## 📞 Support

### Issues?
- Check the [Issues](https://github.com/yourusername/ai-image-generator/issues) page
- Create a new issue if needed

### Need Help?
- Read the [OpenAI Documentation](https://platform.openai.com/docs)
- Check [Streamlit Documentation](https://docs.streamlit.io)

## 🎯 Roadmap

### Upcoming Features:
- [ ] Multiple image generation in batch
- [ ] Image editing and enhancement tools
- [ ] Additional AI model support (Midjourney, Stable Diffusion)
- [ ] Image gallery with history
- [ ] Advanced prompt templates
- [ ] Social sharing features

---

## 🌟 Star this repo if you found it helpful!

**Made with ❤️ and powered by AI**

### Quick Links:
- [🌐 Live Demo](https://your-app-url.streamlit.app)
- [📚 OpenAI API](https://platform.openai.com/docs)
- [🚀 Streamlit](https://streamlit.io)
- [🐙 GitHub](https://github.com/Mahnoor-Rana)