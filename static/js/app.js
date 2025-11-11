let trendChart, emotionChart;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadAnalytics();
    initCharts();
});

function showSection(section) {
    document.getElementById('dashboard').classList.add('hidden');
    document.getElementById('analyzeSection').classList.add('hidden');
    document.getElementById('scrapeSection').classList.add('hidden');
    
    if (section === 'analyze') {
        document.getElementById('analyzeSection').classList.remove('hidden');
    } else if (section === 'scrape') {
        document.getElementById('scrapeSection').classList.remove('hidden');
    } else {
        document.getElementById('dashboard').classList.remove('hidden');
        loadAnalytics();
    }
}

async function loadAnalytics() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        // Update stats
        document.getElementById('totalReviews').textContent = data.total_reviews;
        document.getElementById('positiveCount').textContent = data.sentiment_distribution.positive;
        document.getElementById('negativeCount').textContent = data.sentiment_distribution.negative;
        
        // Update charts
        updateTrendChart(data.trend_data);
        updateEmotionChart(data.emotion_distribution);
        
        // Update bar charts
        updateSentimentBars(data.sentiment_distribution, data.total_reviews);
        updateEmotionBars(data.emotion_distribution, data.total_reviews);
        
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

function initCharts() {
    // Trend Chart
    const trendCtx = document.getElementById('trendChart').getContext('2d');
    trendChart = new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Positive',
                data: [],
                borderColor: '#4caf50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                tension: 0.4
            }, {
                label: 'Negative',
                data: [],
                borderColor: '#f44336',
                backgroundColor: 'rgba(244, 67, 54, 0.1)',
                tension: 0.4
            }, {
                label: 'Neutral',
                data: [],
                borderColor: '#9e9e9e',
                backgroundColor: 'rgba(158, 158, 158, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Emotion Chart
    const emotionCtx = document.getElementById('emotionChart').getContext('2d');
    emotionChart = new Chart(emotionCtx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#667eea',
                    '#764ba2',
                    '#f093fb',
                    '#4facfe',
                    '#43e97b',
                    '#fa709a'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                }
            }
        }
    });
}

function updateTrendChart(trendData) {
    const labels = trendData.map(d => new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    const positive = trendData.map(d => d.positive);
    const negative = trendData.map(d => d.negative);
    const neutral = trendData.map(d => d.neutral);
    
    trendChart.data.labels = labels;
    trendChart.data.datasets[0].data = positive;
    trendChart.data.datasets[1].data = negative;
    trendChart.data.datasets[2].data = neutral;
    trendChart.update();
}

function updateEmotionChart(emotionData) {
    const labels = Object.keys(emotionData);
    const values = Object.values(emotionData);
    
    emotionChart.data.labels = labels;
    emotionChart.data.datasets[0].data = values;
    emotionChart.update();
}

function updateSentimentBars(sentimentData, total) {
    const container = document.getElementById('sentimentBars');
    container.innerHTML = '';
    
    const colors = {
        positive: '#4caf50',
        negative: '#f44336',
        neutral: '#9e9e9e'
    };
    
    Object.entries(sentimentData).forEach(([sentiment, count]) => {
        const percentage = total > 0 ? (count / total * 100).toFixed(1) : 0;
        
        const barItem = document.createElement('div');
        barItem.className = 'bar-item';
        barItem.innerHTML = `
            <div class="bar-label">
                <span>${sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}</span>
                <span>${count} (${percentage}%)</span>
            </div>
            <div class="bar-container">
                <div class="bar-fill" style="width: ${percentage}%; background: ${colors[sentiment]}">
                    ${percentage}%
                </div>
            </div>
        `;
        container.appendChild(barItem);
    });
}

function updateEmotionBars(emotionData, total) {
    const container = document.getElementById('emotionBars');
    container.innerHTML = '';
    
    const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a'];
    let colorIndex = 0;
    
    Object.entries(emotionData).forEach(([emotion, count]) => {
        const percentage = total > 0 ? (count / total * 100).toFixed(1) : 0;
        
        const barItem = document.createElement('div');
        barItem.className = 'bar-item';
        barItem.innerHTML = `
            <div class="bar-label">
                <span>${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</span>
                <span>${count} (${percentage}%)</span>
            </div>
            <div class="bar-container">
                <div class="bar-fill" style="width: ${percentage}%; background: ${colors[colorIndex % colors.length]}">
                    ${percentage}%
                </div>
            </div>
        `;
        container.appendChild(barItem);
        colorIndex++;
    });
}

async function analyzeText() {
    const text = document.getElementById('analyzeText').value;
    const resultBox = document.getElementById('analyzeResult');
    
    if (!text) {
        resultBox.innerHTML = '<p style="color: red;">Please enter text to analyze</p>';
        return;
    }
    
    resultBox.innerHTML = '<p>Analyzing...</p>';
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        const result = await response.json();
        
        resultBox.innerHTML = `
            <h3>Analysis Result</h3>
            <p><strong>Sentiment:</strong> <span class="emotion-badge ${result.sentiment}">${result.sentiment}</span></p>
            <p><strong>Emotion:</strong> <span class="emotion-badge ${result.emotion}">${result.emotion}</span></p>
            <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(2)}%</p>
            <h4>All Emotions:</h4>
            ${Object.entries(result.all_emotions).map(([emotion, score]) => 
                `<span class="emotion-badge">${emotion}: ${(score * 100).toFixed(1)}%</span>`
            ).join('')}
        `;
        
        loadAnalytics();
    } catch (error) {
        resultBox.innerHTML = '<p style="color: red;">Error analyzing text</p>';
        console.error('Error:', error);
    }
}

async function scrapeReviews() {
    const source = document.getElementById('sourceSelect').value;
    const url = document.getElementById('urlInput').value;
    const resultBox = document.getElementById('scrapeResult');
    
    if (!url) {
        resultBox.innerHTML = '<p style="color: red;">⚠️ Please enter a URL</p>';
        return;
    }
    
    resultBox.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>🔍 Scraping reviews from ${source}...</p>
            <p>This may take 30-60 seconds. Please wait...</p>
        </div>
    `;
    
    try {
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ source, url })
        });
        
        const result = await response.json();
        
        if (result.error) {
            resultBox.innerHTML = `<p style="color: red;">❌ Error: ${result.error}</p>`;
            return;
        }
        
        resultBox.innerHTML = `
            <div class="success-box">
                <h3>✅ Scraping Complete!</h3>
                <p><strong>Source:</strong> ${source}</p>
                <p><strong>Total Reviews Scraped:</strong> ${result.total_reviews}</p>
                <p><strong>Successfully Analyzed:</strong> ${result.results.length}</p>
                
                <h4>Sample Reviews:</h4>
                <div class="sample-reviews">
                    ${result.results.slice(0, 3).map((r, i) => `
                        <div class="review-sample">
                            <p><strong>Review ${i+1}:</strong> ${r.original_text.substring(0, 100)}...</p>
                            <p><span class="emotion-badge ${r.sentiment}">${r.sentiment}</span> 
                               <span class="emotion-badge ${r.emotion}">${r.emotion}</span>
                               <span class="emotion-badge">Confidence: ${(r.confidence * 100).toFixed(1)}%</span>
                            </p>
                        </div>
                    `).join('')}
                </div>
                
                <p style="margin-top: 20px;">All reviews have been analyzed and added to the dashboard. Check the Dashboard tab to see the updated analytics!</p>
            </div>
        `;
        
        // Refresh dashboard
        setTimeout(() => {
            loadAnalytics();
        }, 1000);
        
    } catch (error) {
        resultBox.innerHTML = `<p style="color: red;">❌ Error scraping reviews: ${error.message}</p>`;
        console.error('Error:', error);
    }
}

async function testScraper() {
    const source = document.getElementById('sourceSelect').value;
    const resultBox = document.getElementById('scrapeResult');
    
    // Sample URLs for testing
    const testUrls = {
        'google_maps': 'https://www.google.com/maps/place/Taj+Mahal',
        'tripadvisor': 'https://www.tripadvisor.com/Hotel_Review-g304551-d306997-Reviews-The_Oberoi_Amarvilas-Agra_Agra_District_Uttar_Pradesh.html',
        'yelp': 'https://www.yelp.com/biz/gary-danko-san-francisco',
        'amazon': 'https://www.amazon.com/dp/B08N5WRWNW',
        'hotel': 'https://www.booking.com/hotel/in/the-oberoi-amarvilas.html',
        'wikipedia': 'https://en.wikipedia.org/wiki/Taj_Mahal'
    };
    
    const testUrl = testUrls[source] || testUrls['google_maps'];
    document.getElementById('urlInput').value = testUrl;
    
    resultBox.innerHTML = `<p>✅ Test URL loaded for ${source}. Click "Scrape & Analyze Reviews" to start.</p>`;
}
