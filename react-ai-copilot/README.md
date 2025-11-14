# React AI Education Copilot Frontend

A modern React + Tailwind CSS frontend for the Flask AI Education Copilot backend. This application provides an intuitive interface for generating and exploring AI-powered educational modules.

## Features

- 🎨 **Modern UI**: Clean, professional interface built with Tailwind CSS
- 📁 **File Explorer**: VS Code-style file tree navigation
- 📝 **Markdown Preview**: Beautiful markdown rendering with syntax highlighting
- ⚡ **Fast**: Built with Vite for lightning-fast development and builds
- 🔄 **Real-time**: Live updates as modules are generated
- 📦 **Download**: One-click ZIP download of generated modules

## Project Structure

```
react-ai-copilot/
├── src/
│   ├── api/
│   │   └── api.js              # Axios API client
│   ├── components/
│   │   ├── Sidebar.jsx         # Instructor prompt input
│   │   ├── FileExplorer.jsx    # File tree navigation
│   │   ├── FilePreview.jsx    # Markdown preview
│   │   ├── Header.jsx          # Header with download button
│   │   ├── Loader.jsx          # Loading spinner
│   │   └── Tabs.jsx            # Tab navigation
│   ├── utils/
│   │   └── tree.js             # File tree utilities
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # Entry point
│   └── index.css              # Global styles
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## Prerequisites

- Node.js 18+ and npm/yarn
- Flask backend running on `http://localhost:5000`

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd react-ai-copilot
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Create environment file (optional):**
   Create a `.env` file in the root directory:
   ```env
   VITE_API_URL=http://localhost:5000
   ```
   If not set, it defaults to `http://localhost:5000`

## Running the Application

1. **Start the development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

2. **Open your browser:**
   Navigate to `http://localhost:3000`

3. **Build for production:**
   ```bash
   npm run build
   # or
   yarn build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   # or
   yarn preview
   ```

## Usage

### Generating a Module

1. Enter your instructor prompt in the sidebar (e.g., "RAG module, intermediate, 5 days")
2. Click "Generate Module"
3. Wait for the module to be generated (this may take a few minutes)
4. Once generated, the file tree will appear in the File Explorer

### Exploring Files

1. Click on any file in the File Explorer to view its content
2. Navigate through folders by clicking on them
3. The selected file's content will appear in the preview pane

### Downloading a Module

1. Click the "Download ZIP" button in the header
2. The module will be downloaded as a ZIP file

## API Integration

The frontend communicates with the Flask backend through the following endpoints:

- `POST /generate-module` - Generate a new module
- `GET /download-module?module=<name>` - Download module as ZIP
- `GET /list-modules` - List all generated modules (not used in UI yet)
- `GET /` - Health check (not used in UI)

All API calls are handled in `src/api/api.js` using Axios.

## Components

### Sidebar
- Input area for instructor prompts
- Generate button with loading state
- Status indicators (success/error)
- Tips and guidelines

### FileExplorer
- VS Code-style file tree
- Expandable folders
- File selection highlighting
- Click to preview files

### FilePreview
- Markdown rendering with `react-markdown`
- Syntax highlighting for code blocks
- GitHub Flavored Markdown support
- Responsive layout

### Header
- Application title
- Module name display
- Download ZIP button

## Styling

The application uses Tailwind CSS for styling. Custom colors and utilities are defined in `tailwind.config.js`. The primary color scheme uses blue tones.

## Error Handling

- Network errors are caught and displayed to the user
- Loading states prevent duplicate requests
- User-friendly error messages
- Automatic error dismissal option

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development

### Adding New Components

1. Create component file in `src/components/`
2. Import and use in `App.jsx` or other components
3. Follow existing component patterns

### Modifying API Calls

Edit `src/api/api.js` to add new endpoints or modify existing ones.

### Styling Changes

- Modify `tailwind.config.js` for theme changes
- Add custom styles to `src/index.css`
- Use Tailwind utility classes in components

## Troubleshooting

### Backend Connection Issues

- Ensure Flask backend is running on port 5000
- Check CORS settings in Flask backend
- Verify `VITE_API_URL` in `.env` if using custom URL

### Module Generation Fails

- Check browser console for errors
- Verify backend is accessible
- Check network tab for API request/response

### Build Issues

- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`
- Check Node.js version (requires 18+)

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check the browser console for errors
2. Verify the Flask backend is running
3. Check network connectivity
4. Review the README for setup instructions

