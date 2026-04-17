/**
 * TA ChatBot Frontend - Main Application
 */

class ChatClient {
    constructor(apiBaseUrl = '') {
        this.apiBaseUrl = apiBaseUrl || this.detectApiUrl();
        this.sessionId = this.generateSessionId();
        this.isDarkMode = localStorage.getItem('theme') === 'dark';
        
        this.elements = {
            messageInput: document.getElementById('message-input'),
            sendBtn: document.getElementById('send-btn'),
            messagesContainer: document.getElementById('messages'),
            themeToggle: document.getElementById('theme-toggle'),
            themeIcon: document.querySelector('.theme-icon'),
            infoBtn: document.getElementById('info-btn'),
            modal: document.getElementById('info-modal'),
            modalClose: document.getElementById('modal-close'),
            courseInfo: document.getElementById('course-info'),
            spinner: document.getElementById('loading-spinner'),
            statusIndicator: document.getElementById('status'),
        };
        
        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        this.setupTheme();
        this.setupEventListeners();
        this.checkHealth();
        this.loadMetrics();
        this.setupAutoComplete();
        
        console.log(`🚀 ChatBot initialized`);
        console.log(`📡 API Base URL: ${this.apiBaseUrl}`);
        console.log(`💾 Session ID: ${this.sessionId}`);
    }

    /**
     * Detect API base URL
     */
    detectApiUrl() {
        const url = new URL(window.location);
        
        // If running on same domain
        if (url.hostname === 'localhost' || url.hostname === '127.0.0.1') {
            return 'http://localhost:8000';
        }
        
        // If running on Railway or similar
        if (window.location.protocol === 'https:') {
            return `https://${url.hostname}`;
        }
        
        return `http://${url.hostname}:8000`;
    }

    /**
     * Setup theme toggle
     */
    setupTheme() {
        if (this.isDarkMode) {
            document.body.classList.add('dark-mode');
            this.updateThemeIcon();
        }
        
        this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    /**
     * Toggle dark/light theme
     */
    toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');
        this.updateThemeIcon();
    }

    /**
     * Update theme icon
     */
    updateThemeIcon() {
        this.elements.themeIcon.textContent = this.isDarkMode ? '☀️' : '🌙';
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Send message
        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
        this.elements.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Info modal
        this.elements.infoBtn.addEventListener('click', () => this.showCourseInfo());
        this.elements.modalClose.addEventListener('click', () => this.closeModal());
        this.elements.modal.addEventListener('click', (e) => {
            if (e.target === this.elements.modal) this.closeModal();
        });

        // Quick search buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.dataset.question;
                this.elements.messageInput.value = question;
                this.elements.messageInput.focus();
            });
        });
    }

    /**
     * Setup auto-complete and suggestions
     */
    setupAutoComplete() {
        // API docs link
        document.getElementById('api-docs-link').href = `${this.apiBaseUrl}/docs`;
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Check API health
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            
            if (response.ok) {
                this.setStatus('✅ Sẵn sàng', '#52a84b');
                return true;
            } else {
                this.setStatus('⚠️ Lỗi kết nối', '#ff9800');
                return false;
            }
        } catch (error) {
            console.error('Health check failed:', error);
            this.setStatus('❌ Không kết nối', '#d97757');
            return false;
        }
    }

    /**
     * Set status indicator
     */
    setStatus(text, color = null) {
        this.elements.statusIndicator.textContent = text;
        if (color) {
            this.elements.statusIndicator.style.color = color;
        }
    }

    /**
     * Load metrics
     */
    async loadMetrics() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/metrics`);
            if (!response.ok) return;
            
            const data = await response.json();
            const metrics = document.querySelectorAll('.metric-value');
            
            if (metrics.length >= 3) {
                metrics[0].textContent = data.total_conversations;
                metrics[1].textContent = data.total_messages;
            }
        } catch (error) {
            console.error('Error loading metrics:', error);
        }
    }

    /**
     * Send message
     */
    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        
        if (!message) {
            alert('Vui lòng nhập câu hỏi');
            return;
        }

        // Disable input while sending
        this.elements.messageInput.disabled = true;
        this.elements.sendBtn.disabled = true;
        this.showSpinner(true);

        try {
            // Add user message to UI
            this.addMessage(message, 'user');
            this.elements.messageInput.value = '';

            // Send to backend
            const response = await fetch(`${this.apiBaseUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Server error');
            }

            const data = await response.json();
            
            // Update session ID if provided
            if (data.session_id) {
                this.sessionId = data.session_id;
            }

            // Add AI response to UI
            this.addMessage(data.response, 'ai', data.type);

            // Refresh metrics
            this.loadMetrics();

        } catch (error) {
            console.error('Error:', error);
            this.addMessage(
                `❌ Lỗi: ${error.message}\n\nVui lòng kiểm tra:\n• API base URL: ${this.apiBaseUrl}\n• OpenAI API Key\n• Kết nối mạng`,
                'system'
            );
        } finally {
            this.elements.messageInput.disabled = false;
            this.elements.sendBtn.disabled = false;
            this.showSpinner(false);
            this.elements.messageInput.focus();
        }
    }

    /**
     * Add message to chat
     */
    addMessage(content, role = 'ai', type = 'normal') {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', role);

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        // Format content with markdown-like support
        content = this.formatMessage(content);
        contentDiv.innerHTML = content;

        msgDiv.appendChild(contentDiv);

        // Add timestamp
        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        timeDiv.textContent = new Date().toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit'
        });
        msgDiv.appendChild(timeDiv);

        this.elements.messagesContainer.appendChild(msgDiv);
        this.scrollToBottom();
    }

    /**
     * Format message with basic markdown support
     */
    formatMessage(content) {
        // Escape HTML
        content = content
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');

        // Convert **bold** to <strong>
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Convert *italic* to <em>
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');

        // Convert `code` to <code>
        content = content.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Convert links [text](url)
        content = content.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Convert newlines to <br>
        content = content.replace(/\n/g, '<br>');

        // Convert lists
        content = content.replace(/^• (.*?)$/gm, '<li>$1</li>');
        content = content.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

        return content;
    }

    /**
     * Scroll to bottom
     */
    scrollToBottom() {
        this.elements.messagesContainer.scrollTop = 
            this.elements.messagesContainer.scrollHeight;
    }

    /**
     * Show spinner
     */
    showSpinner(show = true) {
        if (show) {
            this.elements.spinner.classList.add('show');
        } else {
            this.elements.spinner.classList.remove('show');
        }
    }

    /**
     * Show course information
     */
    async showCourseInfo() {
        this.elements.modal.classList.add('show');

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/course-info`);
            if (!response.ok) throw new Error('Failed to load course info');

            const data = await response.json();
            
            this.elements.courseInfo.innerHTML = `
                <div class="info-section">
                    <h3>${data.course_name}</h3>
                    <p><strong>Mã khóa:</strong> ${data.course_code}</p>
                    <p><strong>Mô tả:</strong> ${data.description || 'N/A'}</p>
                </div>
            `;
        } catch (error) {
            console.error('Error loading course info:', error);
            this.elements.courseInfo.innerHTML = `
                <p class="error">❌ Không thể tải thông tin khóa học: ${error.message}</p>
            `;
        }
    }

    /**
     * Close modal
     */
    closeModal() {
        this.elements.modal.classList.remove('show');
    }
}

/**
 * Initialize app when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    window.chatClient = new ChatClient();
});
