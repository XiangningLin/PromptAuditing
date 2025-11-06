// State
let standards = null;

// DOM Elements
const promptInput = document.getElementById('promptInput');
const auditBtn = document.getElementById('auditBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsContainer = document.getElementById('resultsContainer');
const auditReport = document.getElementById('auditReport');
const viewStandardsBtn = document.getElementById('viewStandardsBtn');
const aboutBtn = document.getElementById('aboutBtn');
const standardsModal = document.getElementById('standardsModal');
const aboutModal = document.getElementById('aboutModal');
const closeStandardsBtn = document.getElementById('closeStandardsBtn');
const closeAboutBtn = document.getElementById('closeAboutBtn');
const categoriesList = document.getElementById('categoriesList');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStandards();
    setupEventListeners();
});

function setupEventListeners() {
    // Audit button
    auditBtn.addEventListener('click', handleAudit);
    
    // Clear button
    clearBtn.addEventListener('click', handleClear);
    
    // Modals
    viewStandardsBtn.addEventListener('click', showStandardsModal);
    aboutBtn.addEventListener('click', () => aboutModal.classList.add('active'));
    closeStandardsBtn.addEventListener('click', () => standardsModal.classList.remove('active'));
    closeAboutBtn.addEventListener('click', () => aboutModal.classList.remove('active'));
    
    // Close modal on backdrop click
    standardsModal.addEventListener('click', (e) => {
        if (e.target === standardsModal) {
            standardsModal.classList.remove('active');
        }
    });
    aboutModal.addEventListener('click', (e) => {
        if (e.target === aboutModal) {
            aboutModal.classList.remove('active');
        }
    });
}

function handleClear() {
    promptInput.value = '';
    resultsContainer.style.display = 'none';
    auditReport.innerHTML = '';
    promptInput.focus();
}

async function loadStandards() {
    try {
        const response = await fetch('/api/standards');
        standards = await response.json();
        renderCategories();
    } catch (error) {
        console.error('Failed to load standards:', error);
    }
}

function renderCategories() {
    if (!standards) return;
    
    categoriesList.innerHTML = '';
    standards.categories.forEach(category => {
        const item = document.createElement('div');
        item.className = 'category-item';
        item.textContent = `${category.id}. ${category.name}`;
        item.addEventListener('click', () => {
            showCategoryDetails(category);
        });
        categoriesList.appendChild(item);
    });
}

function showCategoryDetails(category) {
    // This function is no longer used in the new UI but kept for compatibility
    console.log('Category selected:', category.name);
}

function showStandardsModal() {
    if (!standards) return;
    
    const content = standards.categories.map(category => `
        <div class="standard-category">
            <h3>${category.id}. ${category.name}</h3>
            ${category.standards.map(std => `
                <div class="standard-item">
                    <h4>${std.id} ${std.name}</h4>
                    <p><strong>Description:</strong> ${std.description}</p>
                    <p><strong>Violation Example:</strong> "${std.violation_example}"</p>
                </div>
            `).join('')}
        </div>
    `).join('');
    
    document.getElementById('standardsContent').innerHTML = content;
    standardsModal.classList.add('active');
}

async function handleAudit() {
    const prompt = promptInput.value.trim();
    if (!prompt) {
        alert('Please enter a system prompt to audit.');
        return;
    }
    
    // Disable button and show loading
    auditBtn.disabled = true;
    auditBtn.innerHTML = `
        <span>Analyzing...</span>
    `;
    
    try {
        const response = await fetch('/api/audit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Audit failed');
        }
        
        const result = await response.json();
        displayAuditReport(result);
        
        // Show results container and scroll to it
        resultsContainer.style.display = 'block';
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        auditBtn.disabled = false;
        auditBtn.innerHTML = `
            <span>Generate Audit Report</span>
        `;
    }
}

function displayAuditReport(result) {
    const status = result.overall_status ? result.overall_status.toLowerCase() : 'fail';
    const statusClass = status === 'pass' ? 'pass' : 'fail';
    
    const complianceRate = result.compliance_rate || 0;
    const totalStandards = result.total_standards || 0;
    const standardsPassed = result.standards_passed || 0;
    const violationsFound = totalStandards - standardsPassed;
    
    // Create unique IDs for this report
    const radarChartId = 'radarChart-' + Date.now();
    
    auditReport.innerHTML = `
        <div class="report-card">
            <div class="audit-header">
                <div class="audit-score">
                    <div class="score-circle-container">
                        <div class="score-circle ${statusClass}">
                            ${complianceRate}<span style="font-size: 0.6em;">%</span>
                            <div class="score-label">Compliance</div>
                        </div>
                        <div style="margin-top: 12px; text-align: center; font-size: 13px; color: var(--text-secondary);">
                            ${standardsPassed}/${totalStandards} Standards Met<br>
                            <strong style="color: ${violationsFound > 0 ? 'var(--danger-color)' : 'var(--success-color)'};">
                                ${violationsFound} Violation${violationsFound !== 1 ? 's' : ''}
                            </strong>
                        </div>
                    </div>
                    <div class="audit-summary">
                        <h3>Compliance Assessment</h3>
                        <span class="status-badge ${statusClass}">${result.overall_status || 'Unknown'}</span>
                        <p style="margin-top: 12px; font-size: 14px; color: #6b7280; line-height: 1.6;">${result.summary || 'Audit completed'}</p>
                    </div>
                </div>
            </div>
            <div class="audit-body">
                ${result.categories ? `
                    <div class="radar-chart-container">
                        <h4 style="margin-bottom: 16px; text-align: center; color: var(--text-primary); font-size: 14px; font-weight: 600;">Category Performance Overview</h4>
                        <canvas id="${radarChartId}" class="radar-chart-canvas"></canvas>
                    </div>
                ` : ''}
                
                <h4 style="margin-bottom: 16px; font-size: 14px; font-weight: 600;">Category Compliance Results</h4>
                ${result.categories ? result.categories.map(cat => {
                    const catStatus = cat.status ? cat.status.toLowerCase() : 'fail';
                    const catClass = catStatus === 'pass' ? 'pass' : 'fail';
                    const catPassed = cat.standards_passed || 0;
                    const catTotal = cat.total_standards || 0;
                    const catViolations = cat.violation_count || 0;
                    const catRate = catTotal > 0 ? Math.round((catPassed / catTotal) * 100) : 0;
                    return `
                        <div class="category-result">
                            <h4>
                                <div class="category-header">
                                    <span class="status-badge ${catClass}">${cat.status || 'Unknown'}</span>
                                    <span>${cat.name}</span>
                                </div>
                                <span class="category-score ${catClass}">${catPassed}/${catTotal}</span>
                            </h4>
                            <div class="progress-bar-container">
                                <div class="progress-bar ${catClass}" style="width: ${catRate}%"></div>
                            </div>
                            <p>${cat.explanation || 'No explanation provided'}</p>
                            ${catViolations > 0 ? `
                                <div style="margin-top: 10px; padding: 8px 12px; background: var(--danger-light); border-radius: 6px; border-left: 3px solid var(--danger-color);">
                                    <strong style="font-size: 12px; color: var(--danger-dark);">
                                        ${catViolations} Violation${catViolations !== 1 ? 's' : ''} Found:
                                    </strong>
                                </div>
                            ` : ''}
                        ${cat.violations && cat.violations.length > 0 ? `
                            <div class="violations">
                                <ul>
                                    ${cat.violations.map(v => `<li>${v}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                        </div>
                    `;
                }).join('') : '<p>No category data available</p>'}
                
                ${result.critical_issues && result.critical_issues.length > 0 ? `
                    <div class="critical-issues">
                        <h4>Critical Issues</h4>
                        <ul>
                            ${result.critical_issues.map(issue => `<li>${issue}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${result.recommendations && result.recommendations.length > 0 ? `
                    <div class="recommendations">
                        <h4>Recommendations</h4>
                        <ul>
                            ${result.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    
    // Create radar chart after element is added to DOM
    if (result.categories) {
        setTimeout(() => createRadarChart(radarChartId, result.categories), 100);
    }
}

function createRadarChart(canvasId, categories) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    const labels = categories.map(cat => cat.name);
    const scores = categories.map(cat => {
        const passed = cat.standards_passed || 0;
        const total = cat.total_standards || 1;
        return Math.round((passed / total) * 100);
    });
    
    // Determine colors based on scores
    const backgroundColors = scores.map(score => {
        if (score >= 80) return 'rgba(16, 185, 129, 0.2)';
        if (score >= 50) return 'rgba(245, 158, 11, 0.2)';
        return 'rgba(239, 68, 68, 0.2)';
    });
    
    const borderColors = scores.map(score => {
        if (score >= 80) return 'rgba(16, 185, 129, 1)';
        if (score >= 50) return 'rgba(245, 158, 11, 1)';
        return 'rgba(239, 68, 68, 1)';
    });
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Compliance Score',
                data: scores,
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 2,
                pointBackgroundColor: borderColors,
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: borderColors,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    min: 0,
                    ticks: {
                        stepSize: 20,
                        font: {
                            size: 11
                        }
                    },
                    pointLabels: {
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    angleLines: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.r + '/100';
                        }
                    }
                }
            }
        }
    });
}

// Handle textarea auto-resize
promptInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 300) + 'px';
});

