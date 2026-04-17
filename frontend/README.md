# TA ChatBot - Frontend

Modern, responsive HTML/CSS/JavaScript frontend for the AI Teaching Assistant.

## Features

- ✨ **Beautiful UI** - Claude-inspired design with light/dark mode
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- ⚡ **Fast** - No heavy frameworks, pure vanilla JavaScript
- 🎨 **Themeable** - Light/dark mode with local storage persistence
- 🔒 **Secure** - Input validation, XSS protection, secure headers
- ♿ **Accessible** - Semantic HTML, keyboard navigation
- 📊 **Live Metrics** - Real-time usage statistics from backend
- 💬 **Session Management** - Maintains conversation context

## Architecture

```
frontend/
├── index.html         # Main HTML file
├── styles.css         # All styling (light/dark modes)
├── app.js             # Frontend logic (ChatClient class)
├── Dockerfile         # Nginx container configuration
├── nginx.conf         # Nginx web server configuration
├── .dockerignore       # Files excluded from Docker build
└── README.md          # This file
```

## File Descriptions

### `index.html`
Main HTML structure with:
- Header (logo, theme toggle, info button)
- Chat area (messages container, input)
- Sidebar (metrics, quick searches, links)
- Modal for course information
- Spinner for loading state

### `styles.css`
Comprehensive styling (1000+ lines) including:
- CSS variables for theming
- Light/dark mode support
- Flexbox layout
- Animations (slide-in, fade-in, spin)
- Responsive breakpoints (1024px, 768px, 480px)
- Custom scrollbars
- Utility classes

### `app.js`
JavaScript ChatClient class handling:
- WebSocket-like chat communication
- API calls to backend
- Message formatting and rendering
- Theme toggle and persistence
- Session management
- Auto-detect API URL
- Health checks

### `Dockerfile`
Nginx container with:
- Alpine Linux base (lightweight)
- Health checks
- Port 80 exposed
- Security headers

### `nginx.conf`
Nginx configuration featuring:
- Gzip compression (CSS, JS, etc.)
- Security headers (CSP, X-Frame-Options, etc.)
- Static asset caching (1 year)
- API proxy to backend
- CORS headers
- SPA routing
- Deny access to hidden files

## API Integration

The frontend connects to the backend API at:
```
http://localhost:8000  (local development)
https://your-domain.com  (production)
```

### API Endpoints Used

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/chat` | Send message, get response |
| GET | `/api/course-info` | Get course information |
| GET | `/api/metrics` | Get usage statistics |
| GET | `/health` | Check API health |

## Running Locally

### Option 1: Direct File Access
```bash
# Open index.html in browser
cd frontend
python -m http.server 8080

# Visit: http://localhost:8080
```

### Option 2: Docker Container
```bash
# Build image
docker build -t ta-chatbot-frontend:latest frontend/

# Run container
docker run -d \
  --name ta-chatbot-frontend \
  -p 80:80 \
  -e BACKEND_URL=http://localhost:8000 \
  ta-chatbot-frontend:latest

# Visit: http://localhost
```

### Option 3: Docker Compose (Backend + Frontend)
```bash
# Create docker-compose.yml (see example below)
docker-compose up -d

# Visit: http://localhost
```

## Customization

### Change API Base URL
In `app.js`, modify the `detectApiUrl()` method or pass URL to constructor:

```javascript
// Override API URL
window.chatClient = new ChatClient('https://api.example.com');
```

### Change Theming
Edit CSS variables in `styles.css`:

```css
:root {
    --accent: #d97757;  /* Primary color */
    --bg-primary: #fdfcfb;  /* Light background */
    /* ... more variables ... */
}
```

### Add Custom Quick Searches
Edit `index.html`, add buttons to `.quick-searches`:

```html
<button class="quick-btn" data-question="Your question here">Label</button>
```

### Modify Messages Styling
Edit `.message` and `.message-content` classes in `styles.css`

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers
- ⚠️ IE11 not supported (uses modern ES6+)

## Accessibility

- Keyboard navigation (Tab, Enter, Escape)
- Screen reader support
- High contrast in both themes
- Semantic HTML structure
- Focus indicators on interactive elements

## Performance

- **Static assets**: Cached for 1 year
- **Gzip compression**: Reduces CSS/JS size ~70%
- **No external dependencies**: Faster load time
- **Lazy loading**: Messages loaded as they arrive
- **Local storage**: Persistent theme preference

## Security

- **Content Security Policy**: Restricts script sources
- **X-Frame-Options**: Prevents clickjacking
- **X-Content-Type-Options**: Prevents MIME sniffing
- **Input validation**: Messages validated before sending
- **XSS protection**: HTML escaped in messages
- **CORS**: Controlled API access

## Docker Deployment

### Build
```bash
docker build -t ta-chatbot-frontend:latest frontend/
```

### Run
```bash
docker run -d \
  --name frontend \
  -p 80:80 \
  ta-chatbot-frontend:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      PORT: 8000
    
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      BACKEND_URL: http://backend:8000
```

Run with:
```bash
docker-compose up -d
```

## Railway Deployment

### Frontend Only
```bash
railway init
railway link  # Select backend project
railway deploy
```

### With Backend
Use `docker-compose.yml` with Railway integration:
```bash
railway init
railway variables set OPENAI_API_KEY=sk-...
railway deploy
```

## Troubleshooting

### "Cannot connect to API"
1. Check backend is running on correct port
2. Verify CORS headers from backend
3. Check API URL in browser console: `chatClient.apiBaseUrl`
4. Check browser's Network tab for failed requests

### "Health check failed"
1. Verify OpenAI API key is set
2. Check backend logs for errors
3. Test endpoint: `curl http://backend:8000/health`

### "Messages not showing"
1. Check browser console for errors (F12)
2. Verify session ID is generated: `chatClient.sessionId`
3. Test API endpoint: `curl -X POST http://backend:8000/api/chat -H "Content-Type: application/json" -d '{"message":"test"}'`

### "Theme not persisting"
1. Check localStorage is enabled
2. Clear storage if corrupted: `localStorage.clear()`

## Dependencies

This frontend has **zero npm/package dependencies**! It uses:
- Vanilla JavaScript ES6+
- Pure CSS (no preprocessor)
- Semantic HTML5

No build tools required - just serve the files!

## File Sizes

| File | Size | Gzipped |
|------|------|---------|
| index.html | ~8 KB | ~2 KB |
| styles.css | ~18 KB | ~4 KB |
| app.js | ~12 KB | ~3 KB |
| **Total** | **~38 KB** | **~9 KB** |

Very lightweight for fast loading!

## Future Enhancements

- [ ] Message search functionality
- [ ] Export conversation history
- [ ] Typing indicators
- [ ] File upload support
- [ ] Message reactions/voting
- [ ] User profiles/authentication
- [ ] Multi-language support
- [ ] PWA/offline mode
- [ ] Voice input/output
- [ ] Rich text editor

## License

Project License Here

## Support

For issues:
1. Check `/api/docs` for backend API documentation
2. Open browser DevTools (F12) for console errors
3. Test health endpoint: `/health`
4. Check logs of backend container

---

**Status**: ✅ Frontend ready for integration with backend
