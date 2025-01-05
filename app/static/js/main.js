// Mermaid初始化
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
    flowchart: {
        curve: 'basis'
    }
});

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 初始化弹出框
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // 问题分析表单提交
    const analysisForm = document.getElementById('analysisForm');
    if (analysisForm) {
        analysisForm.addEventListener('submit', handleAnalysisSubmit);
    }
    
    // 评分星星点击事件
    const ratingStars = document.querySelectorAll('.rating-stars i');
    ratingStars.forEach(star => {
        star.addEventListener('click', handleRatingClick);
    });
});

// 处理问题分析表单提交
async function handleAnalysisSubmit(event) {
    event.preventDefault();
    
    // 显示加载动画
    const loadingSpinner = document.querySelector('.loading-spinner');
    const submitButton = event.target.querySelector('button[type="submit"]');
    loadingSpinner.style.display = 'block';
    submitButton.disabled = true;
    
    try {
        const formData = new FormData(event.target);
        const response = await fetch('/analysis/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('分析请求失败');
        }
        
        const result = await response.json();
        displayAnalysisResult(result);
    } catch (error) {
        console.error('分析错误:', error);
        showErrorMessage('分析过程中出现错误，请稍后重试。');
    } finally {
        loadingSpinner.style.display = 'none';
        submitButton.disabled = false;
    }
}

// 显示分析结果
function displayAnalysisResult(result) {
    const resultContainer = document.getElementById('analysisResult');
    resultContainer.innerHTML = `
        <div class="analysis-result fade-in">
            <h3>分析结果</h3>
            <div class="analysis-summary">
                ${result.summary}
            </div>
            <div class="analysis-details">
                ${formatDetails(result.details)}
            </div>
            <div class="analysis-recommendations">
                <h4>建议</h4>
                <ul>
                    ${result.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        </div>
        
        <div class="visualization-container mt-4 fade-in">
            <h3>可视化分析</h3>
            <div class="mermaid">
                ${result.visualization.mermaid_code}
            </div>
        </div>
        
        <div class="feedback-form mt-4 fade-in">
            <h4>分析反馈</h4>
            <div class="rating-stars mb-3">
                ${generateRatingStars()}
            </div>
            <div class="form-group">
                <textarea class="form-control" placeholder="请输入您的反馈意见..."></textarea>
            </div>
            <button class="btn btn-primary mt-2" onclick="submitFeedback('${result.id}')">
                提交反馈
            </button>
        </div>
    `;
    
    // 重新渲染Mermaid图表
    mermaid.init(undefined, document.querySelectorAll('.mermaid'));
}

// 格式化详细分析结果
function formatDetails(details) {
    return Object.entries(details)
        .map(([key, value]) => `
            <div class="detail-item mb-3">
                <h5>${key}</h5>
                <p>${value}</p>
            </div>
        `)
        .join('');
}

// 生成评分星星
function generateRatingStars() {
    return Array(5).fill()
        .map((_, i) => `
            <i class="fas fa-star" data-rating="${i + 1}"></i>
        `)
        .join('');
}

// 处理评分点击
function handleRatingClick(event) {
    const rating = event.target.dataset.rating;
    const stars = event.target.parentElement.children;
    
    Array.from(stars).forEach((star, index) => {
        star.style.color = index < rating ? '#ffc107' : '#dee2e6';
    });
}

// 提交反馈
async function submitFeedback(analysisId) {
    const feedbackForm = document.querySelector('.feedback-form');
    const rating = feedbackForm.querySelectorAll('.rating-stars i[style*="rgb(255, 193, 7)"]').length;
    const comments = feedbackForm.querySelector('textarea').value;
    
    try {
        const response = await fetch('/analysis/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                analysis_id: analysisId,
                rating: rating,
                comments: comments
            })
        });
        
        if (!response.ok) {
            throw new Error('反馈提交失败');
        }
        
        showSuccessMessage('感谢您的反馈！');
        feedbackForm.style.display = 'none';
    } catch (error) {
        console.error('反馈错误:', error);
        showErrorMessage('反馈提交失败，请稍后重试。');
    }
}

// 显示成功消息
function showSuccessMessage(message) {
    const alertHtml = `
        <div class="alert alert-success alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.querySelector('main').insertAdjacentHTML('afterbegin', alertHtml);
}

// 显示错误消息
function showErrorMessage(message) {
    const alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.querySelector('main').insertAdjacentHTML('afterbegin', alertHtml);
} 