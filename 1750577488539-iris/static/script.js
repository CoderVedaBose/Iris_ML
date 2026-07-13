const form = document.getElementById('predictionForm');
const result = document.getElementById('result');
const resultContent = document.getElementById('resultContent');
const themeToggle = document.getElementById('themeToggle');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  result.classList.remove('hidden');
  result.classList.add('loading');
  resultContent.innerHTML = '<p>Analyzing your input...</p>';

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    result.classList.remove('loading');

    if (!response.ok) {
      throw new Error(data.error || 'Prediction failed');
    }

    resultContent.innerHTML = `
      <h3>Prediction: ${data.prediction}</h3>
      <p><strong>Confidence:</strong> ${data.confidence}%</p>
      <p>This flower is most likely <strong>${data.prediction}</strong>.</p>
      <div class="badges">
        ${data.classes
          .map((label, index) => {
            const probability = data.probabilities[index];
            return `<span>${label}: ${probability}%</span>`;
          })
          .join('')}
      </div>
    `;
  } catch (error) {
    result.classList.remove('loading');
    resultContent.innerHTML = `<p class="error">${error.message}</p>`;
  }
});

themeToggle.addEventListener('click', () => {
  document.documentElement.classList.toggle('dark');
  themeToggle.textContent = document.documentElement.classList.contains('dark') ? '🌙' : '☀️';
});
