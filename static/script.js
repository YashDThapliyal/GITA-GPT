// Simple GITA-GPT Frontend
document.addEventListener('DOMContentLoaded', function() {
    
    const queryInput = document.getElementById('queryInput');
    const submitBtn = document.getElementById('submitBtn');
    const numVersesSlider = document.getElementById('numVerses');
    const numVersesValue = document.getElementById('numVersesValue');
    const resultsSection = document.getElementById('resultsSection');
    const loadingSection = document.getElementById('loadingSection');
    const aiResponse = document.getElementById('aiResponse');
    const versesContainer = document.getElementById('versesContainer');
    const relatedQuestions = document.getElementById('relatedQuestions');
    const toast = document.getElementById('toast');
    const sacredQuerySection = document.querySelector('.sacred-query-section');
    const responseDiv = document.getElementById('response');
    const errorDiv = document.getElementById('error');
    const copyBtn = document.getElementById('copyBtn');

    // Mouse tracking for shimmer effect
    let mouseX = 0;
    let mouseY = 0;
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        // Update shimmer position
        const shimmer = document.querySelector('.shimmer');
        if (shimmer) {
            shimmer.style.left = mouseX + 'px';
            shimmer.style.top = mouseY + 'px';
        }
    });

    // Update verse slider display
    numVersesSlider.addEventListener('input', function() {
        numVersesValue.textContent = this.value;
    });

    // Handle form submission
    submitBtn.addEventListener('click', handleSubmit);
    queryInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    });

    // Only add event listener if copyBtn exists
    if (copyBtn) {
        copyBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const aiResponse = document.getElementById('aiResponse');
            if (aiResponse) {
                const text = aiResponse.textContent || '';
                if (text.trim().length > 0) {
                    if (navigator.clipboard && navigator.clipboard.writeText) {
                        navigator.clipboard.writeText(text).then(() => {
                            showToast('Copied to clipboard! 📜', 'success');
                        }).catch((err) => {
                            showToast('Failed to copy. Please copy manually.', 'warning');
                        });
                    } else {
                        // Fallback for older browsers
                        const textarea = document.createElement('textarea');
                        textarea.value = text;
                        document.body.appendChild(textarea);
                        textarea.select();
                        try {
                            document.execCommand('copy');
                            showToast('Copied to clipboard! 📜', 'success');
                        } catch (err) {
                            showToast('Failed to copy. Please copy manually.', 'warning');
                        }
                        document.body.removeChild(textarea);
                    }
                } else {
                    showToast('Nothing to copy!', 'warning');
                }
            } else {
                showToast('No answer to copy!', 'warning');
            }
        });
    }

    async function handleSubmit() {
        const query = queryInput.value.trim();
        const numVerses = parseInt(numVersesSlider.value);

        if (!query) {
            showToast('Please enter your question', 'warning');
            return;
        }

        // Show loading
        showLoading();
        hideError();
        hideResponse();
        showToast('🔮 Sending your question to the Gita...', 'info');

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    num_verses: numVerses
                })
            });

            showToast('📖 Retrieving relevant verses...', 'info');

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(JSON.stringify(errorData));
            }

            const data = await response.json();
            showToast('✨ Generating answer...', 'info');

            displayResults(data);
            showToast('🕉️ Divine response received!', 'success');

        } catch (error) {
            try {
                // Try to parse the error message as JSON
                const errorData = JSON.parse(error.message);
                displayError(errorData);
            } catch (e) {
                // Fallback for non-JSON errors
                displayError({
                    error_type: 'unknown_error',
                    user_message: "✨ The divine wisdom is temporarily unavailable. Please try again later.",
                    retry_after: 60
                });
            }
        } finally {
            hideLoading();
        }
    }

    function displayResults(data) {
        // Display AI response
        aiResponse.innerHTML = formatText(data.ai_response);

        // Display verses
        versesContainer.innerHTML = '';
        if (data.verses && data.verses.length > 0) {
            data.verses.forEach(verse => {
                const verseElement = createVerseElement(verse);
                versesContainer.appendChild(verseElement);
            });
        } else {
            versesContainer.innerHTML = '<p class="no-verses">No relevant verses found.</p>';
        }

        // Display related questions
        relatedQuestions.innerHTML = '';
        if (data.related_questions && data.related_questions.length > 0) {
            data.related_questions.forEach(question => {
                const questionElement = createQuestionElement(question);
                relatedQuestions.appendChild(questionElement);
            });
        }

        // Show results
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function createVerseElement(verse) {
        const verseDiv = document.createElement('div');
        verseDiv.className = 'verse-item';
        // Expand/collapse logic
        const preview = verse.text.length > 200 ? verse.text.slice(0, 200) + '...' : verse.text;
        let expanded = false;
        verseDiv.innerHTML = `
            <div class="verse-header">
                <div class="verse-title">${verse.chapter}:${verse.verse}</div>
                <div class="similarity-score">${verse.similarity}%</div>
                <span class="expand-indicator">▼</span>
            </div>
            <div class="verse-text">${preview}</div>
        `;
        verseDiv.addEventListener('click', function() {
            const verseTextDiv = verseDiv.querySelector('.verse-text');
            const indicator = verseDiv.querySelector('.expand-indicator');
            if (!expanded) {
                verseTextDiv.innerText = verse.text;
                indicator.textContent = '▲';
                expanded = true;
            } else {
                verseTextDiv.innerText = preview;
                indicator.textContent = '▼';
                expanded = false;
            }
        });
        return verseDiv;
    }

    function createQuestionElement(question) {
        const questionBtn = document.createElement('button');
        questionBtn.className = 'question-btn';
        questionBtn.textContent = question;
        questionBtn.addEventListener('click', () => {
            queryInput.value = question;
            handleSubmit();
        });
        return questionBtn;
    }

    function displayError(errorData) {
        const userMessage = errorData.user_message || errorData.message || "✨ The divine wisdom is temporarily unavailable. Please try again later.";
        const retryAfter = errorData.retry_after || 0;
        
        errorDiv.innerHTML = `
            <div class="error-content">
                <div class="error-icon">${getErrorIcon(errorData.error_type)}</div>
                <div class="error-message">${userMessage}</div>
                ${retryAfter > 0 ? `<div class="retry-info">Please wait ${retryAfter} seconds before trying again.</div>` : ''}
                ${errorData.error_type === 'rate_limit' ? '<div class="retry-info">The divine wisdom is in high demand - this is a good sign! 🌟</div>' : ''}
            </div>
        `;
        errorDiv.style.display = 'block';
        
        // Auto-hide error after retry time
        if (retryAfter > 0) {
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, retryAfter * 1000);
        }
    }

    function getErrorIcon(errorType) {
        const icons = {
            'rate_limit': '🌊',
            'model_unavailable': '🕉️',
            'token_limit': '📝',
            'auth_error': '🔐',
            'network_error': '🌐',
            'unknown_error': '✨'
        };
        return icons[errorType] || '✨';
    }

    function formatText(text) {
        if (!text) return '<p>No response available.</p>';
        let html = text;
        // Section headers: turn 'Summary:', 'Detailed Answer:', 'Key Concepts:', 'Practical Takeaway:' into <h3>
        html = html.replace(/^(Summary|Detailed Answer|Key Concepts|Practical Takeaway):/gim, '<h3>$1</h3>');
        // Bullet points: lines starting with * or -
        // Convert to <ul><li>...</li></ul>
        // First, ensure all bullet points start on their own line
        html = html.replace(/\r/g, '');
        // Group consecutive bullet points into a single <ul>
        // Convert consecutive bullet points into a single <ul>
        html = html.replace(/(?:^|\n)(\*|-)\s+(.+?)(?=(?:\n(?!\*|-)|$))/gms, (match) => {
            const lines = match.trim().split('\n').map(line => line.trim());
            const listItems = lines.map(line => {
                const itemText = line.replace(/^(\*|-)\s*/, '');
                return `<li>${itemText}</li>`;
            });
            return `<ul>${listItems.join('')}</ul>`;
        });
        // Remove any stray bullet markers
        html = html.replace(/^[\*\-] /gm, '<li>$&</li>');
        // Bold
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Double newlines to paragraphs
        html = html.replace(/\n\n/g, '</p><p>');
        // Single newlines to <br> (but not inside <ul> or <ol>)
        html = html.replace(/(?!<\/?(ul|li)[^>]*>)\n/g, '<br>');
        // Wrap in <p> if not already
        if (!/^<p>/.test(html)) html = '<p>' + html + '</p>';
        // Remove <p> tags around <ul> or <h3>
        html = html.replace(/<p>(\s*)(<ul>|<h3>)/g, '$2');
        html = html.replace(/(<\/ul>|<\/h3>)(\s*)<\/p>/g, '$1');
        return html;
    }

    function setLoading(loading) {
        if (loading) {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            queryInput.disabled = true;
            loadingSection.classList.remove('hidden');
            resultsSection.classList.add('hidden');
        } else {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            queryInput.disabled = false;
            loadingSection.classList.add('hidden');
        }
    }

    function showToast(message, type = 'info') {
        toast.textContent = message;
        toast.className = `mystical-toast ${type}`;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 5000);
    }

    function showLoading() {
        setLoading(true);
        submitBtn.textContent = 'Seeking Wisdom...';
    }

    function hideLoading() {
        setLoading(false);
        submitBtn.textContent = 'Ask the Divine';
    }

    function hideError() {
        if (errorDiv) errorDiv.style.display = 'none';
    }

    function hideResponse() {
        resultsSection.classList.add('hidden');
    }

    // Utility functions
    // Make copyToClipboard available globally before any button uses it
    window.copyToClipboard = function(elementId) {
        const element = document.getElementById(elementId);
        const text = element.innerText || element.textContent;
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard! 📜', 'success');
        }).catch(() => {
            showToast('Failed to copy. Please copy manually.', 'warning');
        });
    };

}); 