document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const genreSelect = document.getElementById('genre');
    const promptInput = document.getElementById('prompt');
    const lengthSlider = document.getElementById('length');
    const lengthValue = document.getElementById('lengthValue');
    const creativitySlider = document.getElementById('creativity');
    const creativityValue = document.getElementById('creativityValue');
    const apiKeyInput = document.getElementById('apiKey');
    const generateBtn = document.getElementById('generateBtn');
    const seedOutput = document.getElementById('seedOutput');
    const textOutput = document.getElementById('textOutput');
    const evaluationOutput = document.getElementById('evaluationOutput');
    const ngramPlot = document.getElementById('ngramPlot');
    const errorOutput = document.getElementById('errorOutput');
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    // Tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(`${tabId}Tab`).classList.add('active');
        });
    });
    
    // Update slider displays
    lengthSlider.addEventListener('input', updateSliderValue);
    creativitySlider.addEventListener('input', updateSliderValue);
    
    function updateSliderValue(e) {
        const target = e.target;
        const value = target.value;
        
        if (target.id === 'length') {
            lengthValue.textContent = value;
        } else if (target.id === 'creativity') {
            creativityValue.textContent = value;
        }
    }

    // Generate button handler
    generateBtn.addEventListener('click', async function() {
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        errorOutput.classList.add('hidden');
        
        try {
            const genre = genreSelect.value;
            const prompt = promptInput.value;
            const length = parseInt(lengthSlider.value);
            const creativity = parseFloat(creativitySlider.value);
            const apiKey = apiKeyInput.value;
            
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    genre,
                    prompt,
                    length,
                    creativity,
                    api_key: apiKey
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                seedOutput.value = data.seed || "No seed generated";
                textOutput.value = data.output || "No output generated";
                evaluationOutput.textContent = JSON.stringify(data.evaluation, null, 2);
                
                if (data.plot) {
                    ngramPlot.src = `data:image/png;base64,${data.plot}`;
                    ngramPlot.style.display = 'block';
                } else {
                    ngramPlot.style.display = 'none';
                }
                
                errorOutput.classList.add('hidden');
            } else {
                throw new Error(data.error || 'Generation failed');
            }
        } catch (error) {
            errorOutput.textContent = error.message;
            errorOutput.classList.remove('hidden');
            console.error('Generation error:', error);
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate';
        }
    });
});